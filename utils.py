import hashlib
import uuid

def simple_hash(password):
    """
    Simple hashing - intentionally weak for demo purposes
    VULNERABILITY: MD5 is broken and should never be used
    """
    return hashlib.md5(password.encode()).hexdigest()

def generate_id():
    """Generate a unique ID"""
    return str(uuid.uuid4())

def sanitize_string(value):
    """Basic string sanitization :DDDDD"""
    return value.strip() if value else ''
