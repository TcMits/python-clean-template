from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_engine(database_url: str, pool_size: int) -> Engine:
    return create_engine(url=database_url, pool_size=pool_size, pool_pre_ping=True)
