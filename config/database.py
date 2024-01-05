from sqlmodel import create_engine, SQLModel, Session

from config.settings import settings

engine = create_engine(settings.postgres_url, pool_pre_ping=True)

SQLModel.metadata.create_all(engine)


async def get_database():
    database: Session = Session(engine)
    try:
        yield database
        database.commit()
    except Exception as e:
        database.rollback()
    finally:
        database.close()