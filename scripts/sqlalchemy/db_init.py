from table import Base, Threads, Comments, ImgPaths
from sqlalchemy import create_engine
engine = create_engine('sqlite:///data.db')
Base.metadata.create_all(engine)