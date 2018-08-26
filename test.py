import redis
from core.internal.settings.sites import Sites, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


if __name__ == "__main__":
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    sites = Sites()




    engine = create_engine("postgresql://postgres:neverever@localhost:6379/aineko")
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()
    session = DBSession()

    # Insert a Person in the person table
    sites.url = "http://vg.no"
    session.add(sites)
    session.commit()

