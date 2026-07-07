"""פירוק JWT לרכיביו, והדגמה שה-payload מקודד base64 ולא מוצפן."""
import base64
import jwt

def create_token(secret_key: str) -> str:
    return jwt.encode(
        {"sub": "dana", "role": "qa", "exp": 9999999999},
        secret_key,
        algorithm="HS256",
    )

def verify_token(token: str, secret_key: str) -> dict:
    return jwt.decode(token, secret_key, algorithms=["HS256"])

def b64url_decode(segment: str) -> bytes:
    padding = "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(segment + padding)





