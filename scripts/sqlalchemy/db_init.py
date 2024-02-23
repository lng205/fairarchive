from table import Base, Thread, Comment, ImgPath, ReplyComment
from sqlalchemy import create_engine
engine = create_engine('sqlite:///data.db')
Base.metadata.create_all(engine)