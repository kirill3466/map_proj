import secrets

import bcrypt
import string


def hash_password(password: str):
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


def generate_password():
    alphanumeric = string.ascii_letters + string.digits
    while True:
        password = "".join(secrets.choice(alphanumeric) for i in range(10))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3
        ):
            break
    return password


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
