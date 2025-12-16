import hashlib

def hash_access_code(code: str) -> str:
    """
    Hashes the access code using SHA-256.
    """
    return hashlib.sha256(code.encode()).hexdigest()
