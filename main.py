from scripts import decode_jwt
import json
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

def main() -> None:
    secret_key = os.environ.get("MY_SECRET_KEY")
    token = decode_jwt.create_token(secret_key)
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT structure: A JWT must consist of exactly 3 parts separated by dots.")
    print("parts count:", len(parts))

    header_b64, payload_b64, _signature_b64 = parts
    print("header:", json.loads(decode_jwt.b64url_decode(header_b64)))
    print("payload:", json.loads(decode_jwt.b64url_decode(payload_b64)))

    print("verified payload:", jwt.decode(token, os.environ.get("MY_SECRET_KEY"), algorithms=["HS256"]))

    try:
        jwt.decode(token, "wrong-secret", algorithms=["HS256"])
        print("שגיאה: טוקן מזויף התקבל")
    except jwt.InvalidSignatureError:
        print("מפתח שגוי -> אימות נכשל, כצפוי")

if __name__ == "__main__":
    main()