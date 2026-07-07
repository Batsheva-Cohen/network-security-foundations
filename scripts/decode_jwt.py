"""פירוק JWT לרכיביו, והדגמה שה-payload מקודד base64 ולא מוצפן."""
import base64
import json
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

#SECRET = os.environ.get("MY_SECRET_KEY")
# במערכת אמת השרת מנפיק את הטוקן לאחר התחברות מוצלחת. כאן יוצרים אותו מקומית.
def creat_token(SECRET):
    token = jwt.encode(
    {"sub": "dana", "role": "qa", "exp": 9999999999},
    SECRET,
    algorithm="HS256",)
    return token

# JWT בנוי משלושה חלקים מופרדים בנקודה.
token = creat_token(os.environ.get("MY_SECRET_KEY"))
parts = token.split(".")
if len(parts) != 3:
    raise ValueError("Invalid JWT structure: A JWT must consist of exactly 3 parts separated by dots.")
print("מספר חלקים:", len(parts), "(header.payload.signature)")
header_b64, payload_b64, _signature_b64 = parts


def b64url_decode(segment: str) -> bytes:
    padding = "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(segment + padding)


# ה-header וה-payload הם base64, ולכן קריאים לכל אחד בלי מפתח. הם אינם מוצפנים.
print("header:", json.loads(b64url_decode(header_b64)))
print("payload:", json.loads(b64url_decode(payload_b64)))

# המפתח מגן על ה-signature, שמבטיח שהתוכן לא שונה. אימות עם המפתח הנכון מצליח.
print("verified payload:", jwt.decode(token, os.environ.get("MY_SECRET_KEY"), algorithms=["HS256"]))

# אימות עם מפתח שגוי נכשל, וזה מה שמונע זיוף טוקנים.
try:
    jwt.decode(token, "wrong-secret", algorithms=["HS256"])
    print("שגיאה: טוקן מזויף התקבל")
except jwt.InvalidSignatureError:
    print("מפתח שגוי -> אימות נכשל, כצפוי")




