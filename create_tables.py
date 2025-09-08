from database import engine, Base
from models import TblUser, TblUserLog  # assuming the models are in models.py

# Create all tables
Base.metadata.create_all(bind=engine)
