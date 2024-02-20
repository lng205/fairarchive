from post import Post
import sqlite3, time, json
from datetime import datetime, timezone


def main():
    conn = sqlite3.connect(r'data.db')
    cursor = conn.cursor()
    update_id(cursor)
    update_post(cursor)
    conn.commit()
    conn.close()


def update_id(cursor):
    """
    Try to get all the available posts(within 48 hours) and upsert them.
    """
    earlist_p_time = '0'
    while True:
        response = Post.get_ids(earlist_p_time)
        post_list = response.json()['data']['list']
        for post in post_list:
            cursor.execute('''
                INSERT INTO posts (thread_id, cate_id, img_paths, title, content, c_count, view_count, l_count, finish_status, headimgurl, nickname, p_time)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(thread_id) DO UPDATE SET
                cate_id = excluded.cate_id,
                img_paths = excluded.img_paths,
                title = excluded.title,
                content = excluded.content,
                c_count = excluded.c_count,
                view_count = excluded.view_count,
                l_count = excluded.l_count,
                finish_status = excluded.finish_status,
                headimgurl = excluded.headimgurl,
                nickname = excluded.nickname,
                p_time = excluded.p_time
            ''', (
                int(post['thread_id']), int(post['cate_id']), json.dumps(post['img_paths']),
                post['title'], post['content'], int(post['c_count']), 
                int(post['view_count']), int(post['l_count']), int(post['finish_status']), 
                post['headimgurl'], post['nickname'], int(post['p_time'])
            ))
        try:
            earlist_p_time = post_list[-1]['p_time']
        except Exception as e:
            print(f'Error: {e}')
            break
        time.sleep(1)


def update_post(cursor):
    """
    Update post info
    """
    # Read IDs from posts table for posts in the last 48 hours
    timestamp_48_hours_ago = int(datetime.now(timezone.utc).timestamp()) - 48 * 60 * 60
    cursor.execute(f'SELECT thread_id FROM posts WHERE p_time > {timestamp_48_hours_ago}')
    values = cursor.fetchall()

    for value in values:
        try:
            post = update_info(cursor, value[0])
            update_comment(cursor, post)
        except Exception as e:
            print(f'Error: {e}')
            continue
        time.sleep(1)


def update_info(cursor, thread_id):
    post = Post(str(thread_id))
    info = post.info.json()['data']['detail']
    cursor.execute('''
        UPDATE posts
        SET contact_person = ?, contact_phone = ?, contact_qq = ?, contact_wx = ?, short_url = ?
        WHERE thread_id = ?
    ''', (
        info['contact_person'], info['contact_phone'], info['contact_qq'], info['contact_wx'], info['short_url'],
        thread_id
    ))
    return post


def update_comment(cursor, post):
    comment = post.get_comment().json()['data']['list']
    for c in comment:
        cursor.execute('''
            INSERT INTO comments (thread_id, comment_id, reply_comment_id, root_comment_id, content, post_time, like_num, dislike_num, is_author, headimgurl, nickname)
            values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(comment_id) DO UPDATE SET
            thread_id = excluded.thread_id,
            reply_comment_id = excluded.reply_comment_id,
            root_comment_id = excluded.root_comment_id,
            content = excluded.content,
            post_time = excluded.post_time,
            like_num = excluded.like_num,
            dislike_num = excluded.dislike_num,
            is_author = excluded.is_author,
            headimgurl = excluded.headimgurl,
            nickname = excluded.nickname
        ''', (
            int(post.thread_id), int(c['comment_id']), int(c['reply_comment_id']), int(c['root_comment_id']), c['content'], 
            int(c['post_time']), int(c['like_num']), int(c['dislike_num']), int(c['is_author']), c['headimgurl'], c['nickname']
        ))
        for r in c['reply_list']:
            cursor.execute('''
                INSERT INTO comments (thread_id, comment_id, reply_comment_id, root_comment_id, content, post_time, like_num, dislike_num, is_author, headimgurl, nickname)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(comment_id) DO UPDATE SET
                thread_id = excluded.thread_id,
                reply_comment_id = excluded.reply_comment_id,
                root_comment_id = excluded.root_comment_id,
                content = excluded.content,
                post_time = excluded.post_time,
                like_num = excluded.like_num,
                dislike_num = excluded.dislike_num,
                is_author = excluded.is_author,
                headimgurl = excluded.headimgurl,
                nickname = excluded.nickname
            ''', (
                int(post.thread_id), int(r['comment_id']), int(r['reply_comment_id']), int(r['root_comment_id']), r['content'], 
                int(r['post_time']), int(r['like_num']), int(r['dislike_num']), int(r['is_author']), r['headimgurl'], r['nickname']
            ))


if __name__ == '__main__':
    main()