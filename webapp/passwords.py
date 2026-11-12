"""Password hashing for the single-user login (stdlib scrypt; no extra dependencies).

Create the hash on YOUR computer and put only the hash in the Modal secret:

    python -m webapp.passwords

It asks for the password twice (nothing is echoed) and prints a line like
    scrypt$16384$8$1$<salt>$<hash>
"""
from __future__ import annotations

import base64
import getpass
import hashlib
import hmac
import os
import sys

N, R, P, DKLEN = 2 ** 14, 8, 1, 32


def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode().rstrip("=")


def _unb64(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def hash_password(password: str) -> str:
    if len(password) < 12:
        raise ValueError("use at least 12 characters")
    salt = os.urandom(16)
    dk = hashlib.scrypt(password.encode(), salt=salt, n=N, r=R, p=P, dklen=DKLEN)
    return f"scrypt${N}${R}${P}${_b64(salt)}${_b64(dk)}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algo, n, r, p, salt, dk = stored.split("$")
        if algo != "scrypt":
            return False
        calc = hashlib.scrypt(password.encode(), salt=_unb64(salt), n=int(n), r=int(r), p=int(p), dklen=len(_unb64(dk)))
        return hmac.compare_digest(calc, _unb64(dk))
    except (ValueError, TypeError):
        return False


def main() -> int:
    pw = getpass.getpass("New PACK AI password (12+ characters): ")
    if pw != getpass.getpass("Repeat password: "):
        print("passwords do not match", file=sys.stderr)
        return 1
    try:
        print(hash_password(pw))
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
