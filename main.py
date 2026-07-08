from scripts import decode_jwt
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

def main() -> None:
    secret_key = os.environ.get("MY_SECRET_KEY")
    if not secret_key:
        raise ValueError("MY_SECRET_KEY is missing")
    token = decode_jwt.create_token(secret_key)
    print("MY TOKEN IS: {token}")
    try:
        header, payload = decode_jwt.decode_token_parts(token)
        print("Decoded Content:")
        print("Header: ", header)
        print("Payload:", payload)
    except ValueError as e:
        print(f"Structure Error: {e}")


    print("verified payload:", jwt.decode(token, os.environ.get("MY_SECRET_KEY"), algorithms=["HS256"]))

    try:
        jwt.decode(token, "wrong-secret", algorithms=["HS256"])
        print("שגיאה: טוקן מזויף התקבל")
    except jwt.InvalidSignatureError:
        print("מפתח שגוי -> אימות נכשל, כצפוי")
    
    try:
        decode_jwt.verify_token(token, "wrong_secret")
    except jwt.exceptions.InvalidSignatureError:
        print("Success: Caught expected with wrong secret!")

if __name__ == "__main__":
    main()