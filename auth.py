from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from schemas import UserRegister, UserLogin
from models import TblUser, TblUserLog
from database import SessionLocal
from datetime import datetime, timedelta
from pathlib import Path
import hashlib, os, secrets, jwt

router = APIRouter()
security = HTTPBearer()

# ---- stable machine-generated secret key (created once) ----
SECRET_FILE = Path(".secret_key")
if "SECRET_KEY" in os.environ:
    SECRET_KEY = os.environ["SECRET_KEY"]
elif SECRET_FILE.exists():
    SECRET_KEY = SECRET_FILE.read_text().strip()
else:
    SECRET_KEY = secrets.token_hex(32)
    SECRET_FILE.write_text(SECRET_KEY)

ALGORITHM = "HS256"

# ---- DB dependency ----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- password helpers ----
def generate_salt():
    return os.urandom(16).hex()

def hash_password_with_salt(password: str, salt: str):
    return hashlib.sha256((password + salt).encode()).hexdigest()

# ---- JWT helpers ----
def create_jwt_token(user_id: int, username: str):
    payload = {
        "sub": str(user_id),  # 👈 MUST be string for PyJWT 2.x
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        username = payload.get("username")

        # convert sub back to int
        try:
            user_id = int(sub)
        except (TypeError, ValueError):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid token payload")

        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid token payload")

        return {"id": user_id, "username": username}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        # catches InvalidSubjectError, DecodeError, etc.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# ---- routes ----
@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(TblUser).filter(TblUser.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    salt = generate_salt()
    new_user = TblUser(
        username=user.username,
        email=user.email,
        password_hash=hash_password_with_salt(user.password, salt),
        password_salt=salt,
        role="user",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(TblUser).filter(TblUser.username == credentials.username).first()
    if not user or user.password_hash != hash_password_with_salt(credentials.password, user.password_salt):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_jwt_token(user_id=user.id, username=user.username)

    now = datetime.now()
    db.add(TblUserLog(username=user.username, date=now.date(), time=now.time()))
    db.commit()

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "username": user.username, "email": user.email, "role": user.role},
    }

