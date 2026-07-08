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

def decode_token_parts(token: str) -> tuple[dict, dict]:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT structure: A JWT must consist of exactly 3 parts separated by dots.")
    
    header_b64, payload_b64, _ = parts
    
    header = b64url_decode(header_b64)
    payload = b64url_decode(payload_b64)
    
    return header, payload



