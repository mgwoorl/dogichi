from database import DBSession

def session():
    session = DBSession()
    try:
        yield session
    finally:
        session.close()
