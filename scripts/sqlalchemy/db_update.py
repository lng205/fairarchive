import time, json
from post import Post
from datetime import datetime, timezone

from table import Threads, ImgPaths, Comments
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data.db')
Session = sessionmaker(engine)

timestamp_47h_ago = int(datetime.now(timezone.utc).timestamp()) - 47 * 60 * 60
timestamp_48h_ago = timestamp_47h_ago - 60 * 60


def main():
    update_ids()
    # update_posts()


def update_ids() -> None:
    """Update post IDs"""
    earlist_p_time = timestamp_47h_ago
    with Session() as session:
        while True:
            response = Post.get_ids(earlist_p_time)
            post_list = response.json()['data']['list']

            for post_data in post_list:
                # Query for an existing post
                stmt = select(Threads).where(Threads.thread_id == post_data['thread_id'])
                post = session.scalars(stmt).first()
                if post:
                    # Update existing post
                    post.c_count = post_data['c_count']
                    post.view_count = post_data['view_count']
                    post.l_count = post_data['l_count']
                    post.finish_status = post_data['finish_status']
                else:
                    # Insert new post
                    new_post = Threads(
                        thread_id=post_data['thread_id'],
                        cate_id=post_data['cate_id'],
                        title=post_data['title'],
                        content=post_data['content'],
                        c_count=post_data['c_count'],
                        view_count=post_data['view_count'],
                        l_count=post_data['l_count'],
                        finish_status=post_data['finish_status'],
                        headimgurl=post_data['headimgurl'],
                        nickname=post_data['nickname'],
                        p_time=post_data['p_time']
                    )
                    session.add(new_post)

                    # Insert img paths
                    for img_path in post_data['img_paths']:
                        new_img_path = ImgPaths(
                            thread_id=post_data['thread_id'],
                            img_path=img_path
                        )
                        session.add(new_img_path)

            try:
                earlist_p_time = post_list[-1]['p_time']
            except Exception:
                break
        session.commit()


def update_posts():

    stmt = select(Threads).where(timestamp_47h_ago > Threads.p_time > timestamp_48h_ago)

    with Session() as session:
        threads = session.scalars(stmt).all()
        for thread in threads:
            post = Post(str(thread.thread_id))

            # Update post info
            info = post.info.json()['data']['detail']
            if not thread.contact_person:
                thread.contact_person = info['contact_person']
                thread.contact_phone = info['contact_phone']
                thread.contact_qq = info['contact_qq']
                thread.contact_wx = info['contact_wx']
                thread.short_url = info['short_url']
                session.add(thread)

            # Upcert comments
            comment = post.get_comment().json()['data']['list']
            for c in comment:
                stmt = select(Comments).where(Comments.comment_id == c['comment_id'])
                comment = session.scalars(stmt).first()
                if comment:
                    comment.like_num = c['like_num']
                    comment.dislike_num = c['dislike_num']
                else:
                    new_comment = Comments(
                        thread_id=thread.thread_id,
                        comment_id=c['comment_id'],
                        reply_comment_id=c['reply_comment_id'],
                        root_comment_id=c['root_comment_id'],
                        content=c['content'],
                        post_time=c['post_time'],
                        like_num=c['like_num'],
                        dislike_num=c['dislike_num'],
                        is_author=c['is_author'],
                        headimgurl=c['headimgurl'],
                        nickname=c['nickname']
                    )
                    session.add(new_comment)
                for r in c['reply_list']:
                    stmt = select(Comments).where(Comments.comment_id == r['comment_id'])
                    reply = session.scalars(stmt).first()
                    if reply:
                        reply.like_num = r['like_num']
                        reply.dislike_num = r['dislike_num']
                    else:
                        new_reply = Comments(
                            thread_id=thread.thread_id,
                            comment_id=r['comment_id'],
                            reply_comment_id=r['reply_comment_id'],
                            root_comment_id=r['root_comment_id'],
                            content=r['content'],
                            post_time=r['post_time'],
                            like_num=r['like_num'],
                            dislike_num=r['dislike_num'],
                            is_author=r['is_author'],
                            headimgurl=r['headimgurl'],
                            nickname=r['nickname']
                        )
                        session.add(new_reply)

            # # Update post info
            # info = post.info.json()['data']['detail']
            # thread.contact_person = info['contact_person']
            # thread.contact_phone = info['contact_phone']
            # thread.contact_qq = info['contact_qq']
            # thread.contact_wx = info['contact_wx']
            # thread.short_url = info['short_url']
            # session.add(thread)

            # # Update comments
            # comment = post.get_comment().json()['data']['list']
            # for c in comment:
            #     new_comment = Comments(
            #         thread_id=thread.thread_id,
            #         comment_id=c['comment_id'],
            #         reply_comment_id=c['reply_comment_id'],
            #         root_comment_id=c['root_comment_id'],
            #         content=c['content'],
            #         post_time=c['post_time'],
            #         like_num=c['like_num'],
            #         dislike_num=c['dislike_num'],
            #         is_author=c['is_author'],
            #         headimgurl=c['headimgurl'],
            #         nickname=c['nickname']
            #     )
            #     session.add(new_comment)
            #     for r in c['reply_list']:
            #         new_reply = Comments(
            #             thread_id=thread.thread_id,
            #             comment_id=r['comment_id'],
            #             reply_comment_id=r['reply_comment_id'],
            #             root_comment_id=r['root_comment_id'],
            #             content=r['content'],
            #             post_time=r['post_time'],
            #             like_num=r['like_num'],
            #             dislike_num=r['dislike_num'],
            #             is_author=r['is_author'],
            #             headimgurl=r['headimgurl'],
            #             nickname=r['nickname']
            #         )
            #         session.add(new_reply)

        session.commit()

    # def update_comment(session, thread):
    #     comment = post.get_comment().json()['data']['list']
    #     for c in comment:
    #         new_comment = Comments(
    #             thread_id=thread.thread_id,
    #             comment_id=c['comment_id'],
    #             reply_comment_id=c['reply_comment_id'],
    #             root_comment_id=c['root_comment_id'],
    #             content=c['content'],
    #             post_time=c['post_time'],
    #             like_num=c['like_num'],
    #             dislike_num=c['dislike_num'],
    #             is_author=c['is_author'],
    #             headimgurl=c['headimgurl'],
    #             nickname=c['nickname']
    #         )
    #         session.add(new_comment)
    #         for r in c['reply_list']:
    #             new_reply = Comments(
    #                 thread_id=thread.thread_id,
    #                 comment_id=r['comment_id'],
    #                 reply_comment_id=r['reply_comment_id'],
    #                 root_comment_id=r['root_comment_id'],
    #                 content=r['content'],
    #                 post_time=r['post_time'],
    #                 like_num=r['like_num'],
    #                 dislike_num=r['dislike_num'],
    #                 is_author=r['is_author'],
    #                 headimgurl=r['headimgurl'],
    #                 nickname=r['nickname']
    #             )
    #             session.add(new_reply)
    #     session.commit()


if __name__ == '__main__':
    main()


# from post import Post
# import sqlite3, time, json
# from datetime import datetime, timezone


# def main():
#     conn = sqlite3.connect(r'data.db')
#     cursor = conn.cursor()
#     update_id(cursor)
#     update_post(cursor)
#     conn.commit()
#     conn.close()


# def update_id(cursor):
#     """
#     Try to get all the available posts(within 48 hours) and upsert them.
#     """
#     earlist_p_time = '0'
#     while True:
#         response = Post.get_ids(earlist_p_time)
#         post_list = response.json()['data']['list']
#         for post in post_list:
#             cursor.execute('''
#                 INSERT INTO posts (thread_id, cate_id, img_paths, title, content, c_count, view_count, l_count, finish_status, headimgurl, nickname, p_time)
#                 values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#                 ON CONFLICT(thread_id) DO UPDATE SET
#                 cate_id = excluded.cate_id,
#                 img_paths = excluded.img_paths,
#                 title = excluded.title,
#                 content = excluded.content,
#                 c_count = excluded.c_count,
#                 view_count = excluded.view_count,
#                 l_count = excluded.l_count,
#                 finish_status = excluded.finish_status,
#                 headimgurl = excluded.headimgurl,
#                 nickname = excluded.nickname,
#                 p_time = excluded.p_time
#             ''', (
#                 int(post['thread_id']), int(post['cate_id']), json.dumps(post['img_paths']),
#                 post['title'], post['content'], int(post['c_count']), 
#                 int(post['view_count']), int(post['l_count']), int(post['finish_status']), 
#                 post['headimgurl'], post['nickname'], int(post['p_time'])
#             ))
#         try:
#             earlist_p_time = post_list[-1]['p_time']
#         except Exception as e:
#             print(f'Error: {e}')
#             break
#         time.sleep(1)


# def update_post(cursor):
#     """
#     Update post info
#     """
#     # Read IDs from posts table for posts in the last 48 hours
#     timestamp_48_hours_ago = int(datetime.now(timezone.utc).timestamp()) - 48 * 60 * 60
#     cursor.execute(f'SELECT thread_id FROM posts WHERE p_time > {timestamp_48_hours_ago}')
#     values = cursor.fetchall()

#     for value in values:
#         try:
#             post = update_info(cursor, value[0])
#             update_comment(cursor, post)
#         except Exception as e:
#             print(f'Error: {e}')
#             continue
#         time.sleep(1)


# def update_info(cursor, thread_id):
#     post = Post(str(thread_id))
#     info = post.info.json()['data']['detail']
#     cursor.execute('''
#         UPDATE posts
#         SET contact_person = ?, contact_phone = ?, contact_qq = ?, contact_wx = ?, short_url = ?
#         WHERE thread_id = ?
#     ''', (
#         info['contact_person'], info['contact_phone'], info['contact_qq'], info['contact_wx'], info['short_url'],
#         thread_id
#     ))
#     return post


# def update_comment(cursor, post):
#     comment = post.get_comment().json()['data']['list']
#     for c in comment:
#         cursor.execute('''
#             INSERT INTO comments (thread_id, comment_id, reply_comment_id, root_comment_id, content, post_time, like_num, dislike_num, is_author, headimgurl, nickname)
#             values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             ON CONFLICT(comment_id) DO UPDATE SET
#             thread_id = excluded.thread_id,
#             reply_comment_id = excluded.reply_comment_id,
#             root_comment_id = excluded.root_comment_id,
#             content = excluded.content,
#             post_time = excluded.post_time,
#             like_num = excluded.like_num,
#             dislike_num = excluded.dislike_num,
#             is_author = excluded.is_author,
#             headimgurl = excluded.headimgurl,
#             nickname = excluded.nickname
#         ''', (
#             int(post.thread_id), int(c['comment_id']), int(c['reply_comment_id']), int(c['root_comment_id']), c['content'], 
#             int(c['post_time']), int(c['like_num']), int(c['dislike_num']), int(c['is_author']), c['headimgurl'], c['nickname']
#         ))
#         for r in c['reply_list']:
#             cursor.execute('''
#                 INSERT INTO comments (thread_id, comment_id, reply_comment_id, root_comment_id, content, post_time, like_num, dislike_num, is_author, headimgurl, nickname)
#                 values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#                 ON CONFLICT(comment_id) DO UPDATE SET
#                 thread_id = excluded.thread_id,
#                 reply_comment_id = excluded.reply_comment_id,
#                 root_comment_id = excluded.root_comment_id,
#                 content = excluded.content,
#                 post_time = excluded.post_time,
#                 like_num = excluded.like_num,
#                 dislike_num = excluded.dislike_num,
#                 is_author = excluded.is_author,
#                 headimgurl = excluded.headimgurl,
#                 nickname = excluded.nickname
#             ''', (
#                 int(post.thread_id), int(r['comment_id']), int(r['reply_comment_id']), int(r['root_comment_id']), r['content'], 
#                 int(r['post_time']), int(r['like_num']), int(r['dislike_num']), int(r['is_author']), r['headimgurl'], r['nickname']
#             ))


# if __name__ == '__main__':
#     main()