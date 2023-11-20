from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def get_engine(config: dict[str, str]) -> Engine:
    user = config["user"]
    password = config["password"]
    host = config["host"]
    port = config["port"]
    database = config["database"]

    DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    return create_engine(DATABASE_URL)


def get_session(config: dict[str, str]) -> sessionmaker:
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine(config))
