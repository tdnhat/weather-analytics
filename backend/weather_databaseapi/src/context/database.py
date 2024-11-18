import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

# Create database URL - use mysql+mysqldb:// instead of mysql://
DATABASE_URL = f"mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

ssl_args = {
    'ssl': {
        'sslmode': 'REQUIRED',
        'ca': '/app/ca.pem'
    }
}

engine = create_engine(
                DATABASE_URL,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10
            )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()