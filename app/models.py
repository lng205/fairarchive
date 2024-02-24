from app import db
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import Optional, List


class Thread(db.Model):
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


class ImgPath(db.Model):
    img_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    thread_id = mapped_column(ForeignKey("thread.thread_id"))
    img_path: Mapped[str]

    thread: Mapped["Thread"] = relationship(back_populates="img_paths")


class Comment(db.Model):
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


class ReplyComment(db.Model):
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