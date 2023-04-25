"""
The `database` module contains functions and classes related to database
configuration and interaction.

This module provides an `engine` object for connecting to a database, as
well as a `Base` object for defining database models using SQLAlchemy.
It also contains functions for creating database tables and interacting
with the database.

Example usage:

    # create a connection to the database
    engine = create_engine('postgresql://user:password@localhost/mydatabase')

    # create a base model for database models
    Base = declarative_base()
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

# PostgreSQL database URL from environment variable
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://app_user:app_password@db:5432/app_db"
)

# SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# databases
database = Database(DATABASE_URL)
