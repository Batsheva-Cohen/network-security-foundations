import base64

from cryptography.fernet import Fernet

message = "sensitive value"

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

