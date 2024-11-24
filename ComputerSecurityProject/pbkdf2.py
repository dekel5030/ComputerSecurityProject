from hashlib import pbkdf2_hmac
import os
salt = os.urandom(16)
print(salt)

def hash(password,salt):
    our_app_iters = 500_000  # Application specific, read above.
    dk = pbkdf2_hmac('sha256', bytes(password, 'utf-8'), salt * 2, our_app_iters)
    return dk.hex()




password = 'a123'
hashed_password = hash(password)
print(hashed_password)
password2 = 'a123'
hashed_password = hash(password)
print(hashed_password)
