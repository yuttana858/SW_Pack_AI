"""GitHub sign-in (OAuth App) for the web app.

GitHub OAuth does not issue OIDC identity tokens, so the server completes the OAuth code exchange
itself, checks the user is an ACTIVE member of the company GitHub organization, reads their team
memberships, and issues its own short-lived session token (HS256, signed with SWPACK_SESSION_SECRET).
The GitHub access token is used only during the callback and is never stored or sent to the browser.

Scopes requested: read:user, user:email, read:org (all read-only).
Login CSRF protection: the `state` is a signed, 10-minute token whose nonce must match an HttpOnly
cookie set on the same browser when login started.
"""
from __future__ import annotations

import secrets
import time
from urllib.parse import urlencode

import httpx
import jwt

AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
API = "https://api.github.com"
SESSION_ISSUER = "swpack-github"
STATE_TTL_S, SESSION_TTL_S = 600, 8 * 3600
SCOPES = "read:user user:email read:org"


class GitHubLoginError(Exception):
    pass


def start_login(client_id: str, secret: str, redirect_uri: str) -> tuple[str, str]:
    """Return (authorize URL, nonce for the HttpOnly cookie)."""
    nonce = secrets.token_urlsafe(24)
    state = jwt.encode({"n": nonce, "exp": int(time.time()) + STATE_TTL_S, "iss": "swpack-oauth-state"}, secret, algorithm="HS256")
    q = {"client_id": client_id, "redirect_uri": redirect_uri, "scope": SCOPES, "state": state, "allow_signup": "false"}
    return f"{AUTHORIZE_URL}?{urlencode(q)}", nonce


def complete_login(*, code: str, state: str, cookie_nonce: str | None, client_id: str, client_secret: str,
                   secret: str, redirect_uri: str, org: str, member_role: str, team_roles: dict, team_plants: dict,
                   http: httpx.Client | None = None) -> str:
    """Finish the OAuth flow and return a session token. Raises GitHubLoginError on any failure."""
    try:
        st = jwt.decode(state, secret, algorithms=["HS256"], issuer="swpack-oauth-state", options={"require": ["exp"]})
    except jwt.PyJWTError as e:
        raise GitHubLoginError("sign-in expired or was tampered with; please try again") from e
    if not cookie_nonce or not secrets.compare_digest(st["n"], cookie_nonce):
        raise GitHubLoginError("sign-in was started in a different browser session; please try again")

    http = http or httpx.Client(timeout=15)
    tok = http.post(TOKEN_URL, headers={"Accept": "application/json"},
                    data={"client_id": client_id, "client_secret": client_secret, "code": code, "redirect_uri": redirect_uri}).json()
    access = tok.get("access_token")
    if not access:
        raise GitHubLoginError(f"GitHub did not issue a token ({tok.get('error', 'unknown error')})")
    h = {"Authorization": f"Bearer {access}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}

    user = http.get(f"{API}/user", headers=h).json()
    if "id" not in user:
        raise GitHubLoginError("could not read your GitHub profile")
    m = http.get(f"{API}/user/memberships/orgs/{org}", headers=h)
    if m.status_code != 200 or m.json().get("state") != "active":
        raise GitHubLoginError(f"you are not an active member of the {org} GitHub organization")

    teams = []
    page = 1
    while True:
        r = http.get(f"{API}/user/teams", headers=h, params={"per_page": 100, "page": page})
        batch = r.json() if r.status_code == 200 else []
        teams += [t["slug"] for t in batch if t.get("organization", {}).get("login", "").lower() == org.lower()]
        if len(batch) < 100:
            break
        page += 1

    roles = {"viewer", member_role} | {team_roles[t] for t in teams if t in team_roles}
    plants = sorted({team_plants[t] for t in teams if t in team_plants})
    now = int(time.time())
    return jwt.encode({"iss": SESSION_ISSUER, "sub": f"github:{user['id']}", "iat": now, "exp": now + SESSION_TTL_S,
                       "name": user.get("name") or user.get("login", ""), "email": user.get("email") or f"{user.get('login')}@github",
                       "login": user.get("login"), "roles": sorted(roles), "plants": plants, "teams": teams}, secret, algorithm="HS256")
