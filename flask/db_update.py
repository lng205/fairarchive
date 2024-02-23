from post import Post
from datetime import datetime, timezone

from db_init import Thread, ImgPath, Comment, ReplyComment
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(create_engine("sqlite:///data.db"))

# For testing
timestamp_95h_ago = int(datetime.now(timezone.utc).timestamp()) - 90 * 3600
timestamp_96h_ago = timestamp_95h_ago - 6 * 3600
# timestamp_95h_ago = int(datetime.now(timezone.utc).timestamp()) - 95 * 3600
# timestamp_96h_ago = timestamp_95h_ago - 3600


def main():
    update_ids()
    update_posts()


def update_ids() -> None:
    """Update post IDs"""
    earlist_p_time = str(timestamp_95h_ago)
    with Session() as session:
        while True:
            response = Post.get_ids(earlist_p_time)
            post_list = response.json()["data"]["list"]

            for post_data in post_list:
                # Insert new post
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

                # Insert img paths
                for img_path in post_data["img_paths"]:
                    session.add(
                        ImgPath(thread_id=post_data["thread_id"], img_path=img_path)
                    )

            try:
                earlist_p_time = post_list[-1]["p_time"]
            except Exception:
                break
        session.commit()


def update_posts():
    stmt = (
        select(Thread)
        .where(Thread.p_time > timestamp_96h_ago)
        .where(Thread.p_time < timestamp_95h_ago)
    )

    with Session() as session:
        threads = session.scalars(stmt).all()
        for thread in threads:
            post = Post(str(thread.thread_id))

            # Add post info
            info = post.info.json()["data"]["detail"]
            thread.contact_person = info["contact_person"]
            thread.contact_phone = info["contact_phone"]
            thread.contact_qq = info["contact_qq"]
            thread.contact_wx = info["contact_wx"]
            session.add(thread)

            comment = post.get_comment().json()["data"]["list"]
            for c in comment:
                # Insert comment
                session.add(
                    Comment(
                        thread_id=thread.thread_id,
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
                    # Insert reply
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

        session.commit()


if __name__ == "__main__":
    main()
