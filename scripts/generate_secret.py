import secrets

# Generate a cryptographically secure secret key
secret_key = secrets.token_urlsafe(50)
print(secret_key)
