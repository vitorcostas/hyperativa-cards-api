import hashlib


def encrypt_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def validate_password(decrypted_password, encrypted_password):
    hashed_password = encrypt_password(decrypted_password)
    return hashed_password == encrypted_password
