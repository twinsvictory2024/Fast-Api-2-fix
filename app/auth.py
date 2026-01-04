import bcrypt


def hash_password(password: str) -> str:
    password = password.encode("utf-8")
    password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
    return password_hash.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    password = password.encode("utf-8")
    password_hash = password_hash.encode("utf-8")
    return bcrypt.checkpw(password, password_hash)