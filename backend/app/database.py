from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Grabbing db connection string from env variable
DATABASE_URL = os.environ["DATABASE_URL"]

# SQLAlchemy object that manages db connection
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, # finds stale connections before using them
    pool_size=10, # number of connections
    max_overflow=20, # extra connections for heavy load
    echo=False, # disable SQL query logging
)

# Factory to create db sessions
SessionLocal = sessionmaker(
    autocommit=False, # turned off so I can manually call session.commit() for control over transactions
    autoflush=False, # turned off so I control when changes are sent to the db
    bind=engine # connects session to engine
)