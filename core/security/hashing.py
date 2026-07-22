import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Usamos bcrypt nativo para esquivar el bug extraño de passlib con la version 4.0+
    # bcrypt.checkpw requiere que ambos argumentos sean bytes
    password_bytes = plain_password.encode('utf-8')
    hash_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hash_bytes)

def get_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(password_bytes, salt)
    return hash_bytes.decode('utf-8')
