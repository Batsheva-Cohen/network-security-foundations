import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

password = b"<demo_password>"
message = "sensitive value"
salt = os.urandom(16)
kdf = Argon2id(
    salt=salt,
    length=32,
    iterations=1,
    lanes=4,
    memory_cost=2**21
)
derived_key = base64.urlsafe_b64encode(kdf.derive(password))
print("derived key:", derived_key)

# הצפנה סימטרית: דורשת מפתח, והיא הפיכה רק עם אותו מפתח.
key = Fernet.generate_key()
cipher = Fernet(key)
encrypted = cipher.encrypt(message.encode())
decrypted = cipher.decrypt(encrypted).decode()

print("encrypted (ניתן לפענוח רק עם המפתח):", encrypted[:40], "...")
print("decrypted:", decrypted)

# קידוד base64: הפיך לכל אחד, בלי מפתח, ולכן אינו אבטחה.
encoded = base64.b64encode(message.encode()).decode()
print("base64 encoded:", encoded)
print("base64 decoded (ללא מפתח):", base64.b64decode(encoded).decode())



