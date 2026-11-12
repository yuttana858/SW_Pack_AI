"""Identity for the web app.

Four modes:
  proxy   Service mode for SWIS and other front ends that already signed the user in (Azure SSO).
          The endpoint sits behind Modal proxy auth; each request must also carry the PACK AI service
          key (X-Service-Key) and the user context headers X-User-Id, X-User-Name, X-User-Email,
          X-User-Plants and X-User-Roles (comma-separated).
  github  "Sign in with GitHub": server-side OAuth, organization membership required, team ->
          role/plant mapping, then a server-issued session token (webapp/github_auth.py).
  oidc  Verify the bearer JWT (RS256/ES256) from the company identity provider against its JWKS,
        check issuer, audience and expiry, then map group claims to roles and plants
        (webapp/auth.yaml, see auth.example.yaml). Provider-agnostic.
  dev   HS256 tokens signed with a local secret for named personas, so the app runs before an
        identity provider is chosen. Refused when SWPACK_ENV=production.

Plants are never taken from the request body: the UI may *choose* among the plants the identity
grants (X-SWPack-Plant header), and anything else is rejected.
"""
from __future__ import annotations

import os
import secrets
import time
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import jwt
import yaml

ROOT = Path(__file__).resolve().parent.parent
ROLE_RANK = {"viewer": 0, "engineer": 1, "plant-admin": 2, "steward": 2}

DEV_PERSONAS = {
    "engineer-a": {"name": "Alex Engineer", "email": "alex@example.test", "roles": ["engineer"], "plants": ["example"]},
    "steward": {"name": "Sam Steward", "email": "sam@example.test", "roles": ["engineer", "steward"], "plants": ["example"]},
    "viewer": {"name": "Val Viewer", "email": "val@example.test", "roles": ["viewer"], "plants": []},
    "plant-admin": {"name": "Pat Admin", "email": "pat@example.test", "roles": ["engineer", "plant-admin"], "plants": ["example"]},
}


class AuthError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status


@dataclass(frozen=True)
class Identity:
    sub: str
    name: str
    email: str
    roles: frozenset[str] = field(default_factory=frozenset)
    plants: tuple[str, ...] = ()

    def has(self, role: str) -> bool:
        return role in self.roles or (role == "viewer")

    @property
    def can_propose(self) -> bool:
        return bool(self.roles & {"engineer", "steward", "plant-admin"})

    def public(self) -> dict:
        return {"sub": self.sub, "name": self.name, "email": self.email, "roles": sorted(self.roles), "plants": list(self.plants)}


@dataclass
class AuthConfig:
    mode: str = "dev"
    oidc: dict = field(default_factory=dict)
    claims: dict = field(default_factory=lambda: {"name": "name", "email": "email", "groups": "groups"})
    role_groups: dict = field(default_factory=dict)
    plant_groups: dict = field(default_factory=dict)
    dev_secret: str = ""
    github: dict = field(default_factory=dict)      # org, member_role, team_roles, team_plants
    session_secret: str = ""
    public_url: str = ""
    service_key: str = ""

    @classmethod
    def load(cls) -> "AuthConfig":
        path = Path(os.environ.get("SWPACK_AUTH_CONFIG", ROOT / "webapp" / "auth.yaml"))
        raw = yaml.safe_load(path.read_text()) if path.exists() else {}
        cfg = cls(**{k: v for k, v in (raw or {}).items() if k in cls.__dataclass_fields__})
        cfg.mode = os.environ.get("SWPACK_AUTH_MODE", cfg.mode)
        if cfg.mode == "dev":
            if os.environ.get("SWPACK_ENV") == "production":
                raise RuntimeError("dev authentication is not allowed when SWPACK_ENV=production")
            cfg.dev_secret = os.environ.get("SWPACK_DEV_SECRET") or secrets.token_urlsafe(32)
        elif cfg.mode == "github":
            g = cfg.github = {"member_role": "engineer", "team_roles": {}, "team_plants": {}, "allowed_users": [],
                              "user_roles": {}, "user_plants": {}, **(cfg.github or {})}
            g["org"] = os.environ.get("SWPACK_GITHUB_ORG", g.get("org") or "").strip()
            extra = [u.strip() for u in os.environ.get("SWPACK_GITHUB_USERS", "").split(",") if u.strip()]
            g["allowed_users"] = sorted({*(g.get("allowed_users") or []), *extra}, key=str.lower)
            g["client_id"] = os.environ.get("GITHUB_CLIENT_ID", "")
            g["client_secret"] = os.environ.get("GITHUB_CLIENT_SECRET", "")
            cfg.session_secret = os.environ.get("SWPACK_SESSION_SECRET", "")
            cfg.public_url = os.environ.get("SWPACK_PUBLIC_URL", cfg.public_url).rstrip("/")
            missing = [n for n, v in (("SWPACK_GITHUB_ORG or allowed_users", g["org"] or g["allowed_users"]),
                                      ("GITHUB_CLIENT_ID", g["client_id"]),
                                      ("GITHUB_CLIENT_SECRET", g["client_secret"]), ("SWPACK_PUBLIC_URL", cfg.public_url)) if not v]
            if missing:
                raise RuntimeError(f"github sign-in needs: {', '.join(missing)}")
            if len(cfg.session_secret) < 32:
                raise RuntimeError("SWPACK_SESSION_SECRET must be at least 32 characters")
        elif cfg.mode == "proxy":
            cfg.service_key = os.environ.get("PACKAI_SERVICE_KEY", "")
            if len(cfg.service_key) < 32:
                raise RuntimeError("proxy mode needs PACKAI_SERVICE_KEY (at least 32 characters)")
        elif cfg.mode != "oidc":
            raise RuntimeError(f"unknown auth mode {cfg.mode!r}")
        return cfg


class Authenticator:
    def __init__(self, cfg: AuthConfig, jwk_client: jwt.PyJWKClient | None = None):
        self.cfg = cfg
        self._jwks = jwk_client

    # ---- dev ---------------------------------------------------------------------
    def issue_dev_token(self, persona: str, ttl_s: int = 8 * 3600) -> str:
        if self.cfg.mode != "dev":
            raise AuthError(404, "dev login is disabled")
        p = DEV_PERSONAS.get(persona)
        if not p:
            raise AuthError(400, f"unknown persona; choose one of {sorted(DEV_PERSONAS)}")
        now = int(time.time())
        return jwt.encode({"sub": f"dev:{persona}", "iat": now, "exp": now + ttl_s, "iss": "swpack-dev", **p},
                          self.cfg.dev_secret, algorithm="HS256")

    # ---- oidc --------------------------------------------------------------------
    @lru_cache(maxsize=1)
    def _discovered_jwks_url(self) -> str:
        import httpx  # noqa: PLC0415
        o = self.cfg.oidc
        if o.get("jwks_url"):
            return o["jwks_url"]
        doc = httpx.get(o["issuer"].rstrip("/") + "/.well-known/openid-configuration", timeout=10).json()
        return doc["jwks_uri"]

    def _jwk_client(self) -> jwt.PyJWKClient:
        if self._jwks is None:
            self._jwks = jwt.PyJWKClient(self._discovered_jwks_url(), cache_keys=True, lifespan=3600)
        return self._jwks

    def _map_claims(self, claims: dict) -> Identity:
        c = self.cfg.claims
        groups = claims.get(c.get("groups", "groups")) or []
        groups = [groups] if isinstance(groups, str) else list(groups)
        roles = {"viewer"} | {self.cfg.role_groups[g] for g in groups if g in self.cfg.role_groups}
        plants = sorted({self.cfg.plant_groups[g] for g in groups if g in self.cfg.plant_groups})
        return Identity(sub=claims["sub"], name=claims.get(c.get("name", "name"), ""), email=claims.get(c.get("email", "email"), ""),
                        roles=frozenset(roles), plants=tuple(plants))

    # ---- entry point ---------------------------------------------------------------
    def authenticate_request(self, headers) -> Identity:
        """Authenticate from request headers (all modes)."""
        if self.cfg.mode != "proxy":
            return self.authenticate(headers.get("authorization"))
        key = headers.get("x-service-key") or ""
        if not secrets.compare_digest(key.encode(), self.cfg.service_key.encode()):
            raise AuthError(401, "missing or invalid X-Service-Key")
        uid = (headers.get("x-user-id") or "").strip()
        if not uid:
            raise AuthError(400, "X-User-Id header is required (the signed-in user's stable id)")
        split = lambda v: tuple(x.strip() for x in (v or "").split(",") if x.strip())  # noqa: E731
        roles = frozenset({"viewer"} | {r.lower() for r in split(headers.get("x-user-roles"))} & set(ROLE_RANK))
        return Identity(sub=f"user:{uid}", name=(headers.get("x-user-name") or uid).strip(),
                        email=(headers.get("x-user-email") or "").strip(), roles=roles,
                        plants=tuple(sorted(set(split(headers.get("x-user-plants"))))))

    def authenticate(self, authorization: str | None) -> Identity:
        if not authorization or not authorization.lower().startswith("bearer "):
            raise AuthError(401, "sign in required")
        token = authorization.split(" ", 1)[1].strip()
        try:
            if self.cfg.mode in ("dev", "github"):
                secret, iss = (self.cfg.dev_secret, "swpack-dev") if self.cfg.mode == "dev" else (self.cfg.session_secret, "swpack-github")
                claims = jwt.decode(token, secret, algorithms=["HS256"], issuer=iss, options={"require": ["exp", "sub"]})
                return Identity(sub=claims["sub"], name=claims.get("name", ""), email=claims.get("email", ""),
                                roles=frozenset({"viewer", *claims.get("roles", [])}), plants=tuple(claims.get("plants", [])))
            key = self._jwk_client().get_signing_key_from_jwt(token).key
            claims = jwt.decode(token, key, algorithms=["RS256", "ES256", "PS256"], audience=self.cfg.oidc["audience"],
                                issuer=self.cfg.oidc["issuer"], options={"require": ["exp", "iss", "aud", "sub"]})
        except jwt.ExpiredSignatureError as e:
            raise AuthError(401, "session expired; sign in again") from e
        except jwt.PyJWTError as e:
            raise AuthError(401, f"invalid token: {e}") from e
        return self._map_claims(claims)

    @staticmethod
    def choose_plant(identity: Identity, requested: str | None) -> str | None:
        if requested:
            if requested not in identity.plants:
                raise AuthError(403, f"you are not assigned to plant {requested!r}")
            return requested
        return identity.plants[0] if identity.plants else None

    def public_config(self) -> dict:
        if self.cfg.mode == "dev":
            return {"mode": "dev", "personas": {k: {"name": v["name"], "roles": v["roles"]} for k, v in DEV_PERSONAS.items()}}
        if self.cfg.mode == "proxy":
            return {"mode": "proxy"}
        if self.cfg.mode == "github":
            return {"mode": "github", "login_url": "/auth/github/login", "org": self.cfg.github["org"] or None}
        o = self.cfg.oidc
        return {"mode": "oidc", "authority": o["issuer"], "client_id": o["client_id"], "scopes": o.get("scopes", "openid profile email")}
