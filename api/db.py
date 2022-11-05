from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql://jeopardy:jeopardypassword@localhost/jeopardy")
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
