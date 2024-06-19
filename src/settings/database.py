import contextlib
from typing import Any, AsyncIterator, Dict

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncConnection, AsyncSession
from sqlalchemy.orm import declarative_base

from src.settings.config import DATABASE_URL, IS_DEBUG
from src.settings.logger import logger

Base = declarative_base()


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: Dict[str, Any] = {}):
        """
        Initializes the DatabaseSessionManager with the given database URL and engine arguments.
        """
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    async def close(self):
        """
        Closes the database engine and sessionmaker.
        """
        if self._engine is None:
            logger.error("Attempted to close a non-initialized Database Session Manager.")
            raise Exception("Database Session Manager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None
        logger.info("Database engine and sessionmaker have been closed.")

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """
        Provides an asynchronous context manager for database connections.
        """
        if self._engine is None:
            logger.error("Attempted to connect using a non-initialized Database Session Manager.")
            raise Exception("Database Session Manager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception as ex:
                logger.error(f"Exception occurred during database connection: {ex}")
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """
        Provides an asynchronous context manager for database sessions.
        """
        if self._sessionmaker is None:
            logger.error("Attempted to use session with a non-initialized Database Session Manager.")
            raise Exception("Database Session Manager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
            await session.commit()
        except Exception as e:
            logger.error(f"Exception occurred during session: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(DATABASE_URL, engine_kwargs={"echo": IS_DEBUG})


async def get_db_session():
    """
    Dependency function to provide a database session for FastAPI endpoints.
    """
    async with sessionmanager.session() as session:
        yield session
