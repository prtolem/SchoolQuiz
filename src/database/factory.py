from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


def create_session_factory(dsn: str) -> async_sessionmaker:
    engine = create_async_engine(dsn)
    session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_maker
