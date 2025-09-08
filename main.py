import logging
from fastapi import FastAPI
from sqlalchemy.orm import Session
from database import SessionLocal
from models import TblUser
from auth import router as auth_router 
from customer import router as customer_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/test-db")
def test_database_connection():
    try:
        db: Session = next(get_db())
        user_count = db.query(TblUser).count()
        return {"success": True, "user_count": user_count}
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return {"success": False, "error": str(e)}


# app.include_router(auth_router,customer_router, prefix="/api", tags=["Authentication"])
# app.include_router(auth_router, prefix="/api", tags=["Authentication"])
# app.include_router(customer_router, prefix="/api", tags=["Customer"])

app.include_router(auth_router, prefix="/api", tags=["Auth"])
app.include_router(customer_router, prefix="/api", tags=["Customers"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular's dev server
    allow_credentials=True,
    allow_methods=["*"],  # or ["GET", "POST", "OPTIONS"]
    allow_headers=["*"],
)
