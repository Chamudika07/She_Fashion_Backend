from passlib.context import CryptContext



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto" , bcrypt__truncate_error=False)

# Function to password hashing
def hash(password: str) -> str:
    password = str(password).strip()

    # bcrypt limit check
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password must be 72 characters or less")

    return pwd_context.hash(password)

# Function to verify password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)





