from app.models import Thread, ImgPath, Comment, ReplyComment
from .post import Post
from sqlalchemy import select  # db.select don't have linting support in VSCode


def upcert_id(post_data: dict, session) -> None:
    """Insert post IDs or update stats"""
    thread = session.scalar(
        select(Thread).where(Thread.thread_id == post_data["thread_id"])
    )
    if thread:
        thread.c_count = post_data["c_count"]
        thread.view_count = post_data["view_count"]
        thread.l_count = post_data["l_count"]
        thread.finish_status = post_data["finish_status"]
    else:
        session.add(
            Thread(
                thread_id=post_data["thread_id"],
                cate_id=post_data["cate_id"],
                title=post_data["title"],
                content=post_data["content"],
                c_count=post_data["c_count"],
                view_count=post_data["view_count"],
                l_count=post_data["l_count"],
                finish_status=post_data["finish_status"],
                headimgurl=post_data["headimgurl"],
                nickname=post_data["nickname"],
                p_time=post_data["p_time"],
            )
        )

        for img_path in post_data["img_paths"]:
            session.add(ImgPath(thread_id=post_data["thread_id"], img_path=img_path))


def upcert_post(thread_id: str, session) -> None:
    """Insert post info and comments or update stats"""
    post = Post(thread_id)

    # Add post info
    info = post.info.json()["data"]["detail"]
    thread = session.scalar(select(Thread).where(Thread.thread_id == thread_id))
    if not thread.contact_person:
        thread.contact_person = info["contact_person"]
        thread.contact_phone = info["contact_phone"]
        thread.contact_qq = info["contact_qq"]
        thread.contact_wx = info["contact_wx"]
    
    # Add comments
    comment = post.get_comment().json()["data"]["list"]
    for c in comment:
        comment = session.scalar(select(Comment).where(Comment.comment_id == c["comment_id"]))
        if comment:
            comment.like_num = c["like_num"]
            comment.dislike_num = c["dislike_num"]
        else:
            session.add(
                Comment(
                    thread_id=thread_id,
                    comment_id=c["comment_id"],
                    content=c["content"],
                    post_time=c["post_time"],
                    like_num=c["like_num"],
                    dislike_num=c["dislike_num"],
                    is_author=c["is_author"],
                    headimgurl=c["headimgurl"],
                    nickname=c["nickname"],
                )
            )
        for r in c["reply_list"]:
            reply = session.scalar(select(ReplyComment).where(ReplyComment.reply_comment_id == r["reply_comment_id"]))
            if reply:
                reply.like_num = r["like_num"]
                reply.dislike_num = r["dislike_num"]
            else:
                session.add(
                    ReplyComment(
                        comment_id=r["comment_id"],
                        reply_comment_id=r["reply_comment_id"],
                        root_comment_id=r["root_comment_id"],
                        content=r["content"],
                        post_time=r["post_time"],
                        like_num=r["like_num"],
                        dislike_num=r["dislike_num"],
                        is_author=r["is_author"],
                        headimgurl=r["headimgurl"],
                        nickname=r["nickname"],
                        reply_nickname=r["reply_nickname"],
                    )
                )