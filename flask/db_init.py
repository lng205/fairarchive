from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import create_engine, ForeignKey
from typing import Optional, List


class Base(DeclarativeBase):
  pass


class Thread(Base):
    __tablename__ = "thread"

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

    comments: Mapped[List["Comment"]] = relationship(back_populates="thread")
    img_paths: Mapped[List["ImgPath"]] = relationship(back_populates="thread")
    
    def __repr__(self) -> str:
        return f"Thread(thread_id={self.thread_id}, title={self.title})"


class ImgPath(Base):
    __tablename__ = "img_path"

    img_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    thread_id = mapped_column(ForeignKey("thread.thread_id"))
    img_path: Mapped[str]

    thread: Mapped["Thread"] = relationship(back_populates="img_paths")

    def __repr__(self) -> str:
        return f"ImgPath(img_id={self.img_id}, thread_id={self.thread_id})"


class Comment(Base):
    __tablename__ = "comment"

    comment_id: Mapped[int] = mapped_column(primary_key=True)
    thread_id = mapped_column(ForeignKey("thread.thread_id"))
    content: Mapped[str]
    post_time: Mapped[int]
    like_num: Mapped[int]
    dislike_num: Mapped[int]
    is_author: Mapped[bool]
    headimgurl: Mapped[str]
    nickname: Mapped[str]

    thread: Mapped["Thread"] = relationship(back_populates="comments")
    reply_comments: Mapped[List["ReplyComment"]] = relationship(back_populates="comment")

    def __repr__(self) -> str:
        return f"Comment(comment_id={self.comment_id}, thread_id={self.thread_id})"


class ReplyComment(Base):
    __tablename__ = "reply_comment"

    comment_id: Mapped[int] = mapped_column(primary_key=True)
    reply_comment_id = mapped_column(ForeignKey("reply_comment.comment_id"))
    root_comment_id = mapped_column(ForeignKey("comment.comment_id"))
    content: Mapped[str]
    post_time: Mapped[int]
    like_num: Mapped[int]
    dislike_num: Mapped[int]
    is_author: Mapped[bool]
    headimgurl: Mapped[str]
    nickname: Mapped[str]
    reply_nickname: Mapped[str]

    comment: Mapped["Comment"] = relationship(back_populates="reply_comments")

    def __repr__(self) -> str:
        return f"ReplyComment(comment_id={self.comment_id}, reply_comment_id={self.reply_comment_id})"


if __name__ == "__main__":
    Base.metadata.create_all(create_engine('sqlite:///data.db'))