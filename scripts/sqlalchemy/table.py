from typing import Optional

from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class Threads(Base):
    __tablename__ = "threads"

    thread_id: Mapped[int] = mapped_column(primary_key=True)
    cate_id: Mapped[int]
    title: Mapped[str]
    content: Mapped[str]
    c_count: Mapped[int]
    view_count: Mapped[int]
    l_count: Mapped[int]
    finish_status: Mapped[int]
    headimgurl: Mapped[str]
    nickname: Mapped[str]
    p_time: Mapped[int]
    contact_person: Mapped[Optional[str]]
    contact_phone: Mapped[Optional[str]]
    contact_qq: Mapped[Optional[str]]
    contact_wx: Mapped[Optional[str]]
    short_url: Mapped[Optional[str]]
    
    def __repr__(self) -> str:
        return f"Thread(thread_id={self.thread_id}, title={self.title})"


class ImgPaths(Base):
    __tablename__ = "img_paths"

    img_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    thread_id = mapped_column(ForeignKey("threads.thread_id"))
    img_path: Mapped[str]

    def __repr__(self) -> str:
        return f"ImgPaths(img_id={self.img_id}, thread_id={self.thread_id})"


class Comments(Base):
    __tablename__ = "comments"

    comment_id: Mapped[int] = mapped_column(primary_key=True)
    thread_id = mapped_column(ForeignKey("threads.thread_id"))
    reply_comment_id: Mapped[int]
    root_comment_id = mapped_column(ForeignKey("comments.comment_id"))
    content: Mapped[str]
    post_time: Mapped[int]
    like_num: Mapped[int]
    dislike_num: Mapped[int]
    is_author: Mapped[bool]
    headimgurl: Mapped[str]
    nickname: Mapped[str]


    def __repr__(self) -> str:
        return f"Comment(comment_id={self.comment_id}, thread_id={self.thread_id})"

    # post = relationship("Post", back_populates="comment")
