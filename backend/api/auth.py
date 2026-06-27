from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import bcrypt

# -----------------------------
# CONFIG
# -----------------------------

SECRET_KEY = "CHANGE_THIS_TO_ENV_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()


# -----------------------------
# FAKE DATABASE (replace with real DB later)
# -----------------------------

fake_users_db = {}


# -----------------------------
# REQUEST MODELS
# -----------------------------

class UserRegister(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


# -----------------------------
# SECURITY FUNCTIONS
# -----------------------------

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        **data,
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# -----------------------------
# REGISTER
# -----------------------------

@router.post("/auth/register")
def register(user: UserRegister):
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)

    fake_users_db[user.email] = {
        "email": user.email,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    }

    token = create_access_token({"sub": user.email})

    return {
        "message": "User registered successfully",
        "access_token": token,
        "token_type": "bearer"
    }


# -----------------------------
# LOGIN
# -----------------------------

@router.post("/auth/login")
def login(user: UserLogin):
    db_user = fake_users_db.get(user.email)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }


# -----------------------------
# TOKEN VALIDATION
# -----------------------------

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# -----------------------------
# PROTECTED TEST ROUTE
# -----------------------------

@router.get("/auth/me")
def get_me(token: str):
    user_email = verify_token(token)

    return {
        "email": user_email,
        "status": "authenticated",
        "system": "A.I.M secure session active"
    }
