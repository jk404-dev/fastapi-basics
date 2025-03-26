import bcrypt

def hash(password: str) -> str:
    # Convert the password to bytes and generate salt
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    # Hash the password
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Return the hash as string
    return hashed.decode('utf-8')

def verify(plain_password: str, hashed_password: str) -> bool:
    # Convert passwords to bytes
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    # Verify and return result
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)


