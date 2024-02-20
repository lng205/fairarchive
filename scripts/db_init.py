import sqlite3

def main():
    database = r'data.db'
    # create_post_table(database)
    create_comment_table(database)
    # add_columns_to_posts(database)


def create_post_table(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            thread_id INTEGER PRIMARY KEY,
            cate_id INTEGER,
            img_paths TEXT,
            title TEXT,
            content TEXT,
            c_count INTEGER,
            view_count INTEGER,
            l_count INTEGER,
            finish_status INTEGER,
            headimgurl TEXT,
            nickname TEXT,
            p_time INTEGER
        )
    ''')
    conn.commit()
    conn.close()


def add_columns_to_posts(database):
    """
    Add columns to posts table
    """

    columns_to_add = [
        'contact_person TEXT',
        'contact_phone TEXT',
        'contact_qq TEXT',
        'contact_wx TEXT',
        'short_url TEXT'
    ]

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    for column in columns_to_add:
        cursor.execute(f'''
                    ALTER TABLE posts
                    ADD COLUMN {column}
                    ''')
    conn.commit()
    conn.close()


def create_comment_table(database):
    """
    Create table for post comments
    Primary key: thread_id
    Columns: thread_id, comment_id, content, c_time, headimgurl, nickname
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE comments (
            thread_id INT,
            comment_id INT PRIMARY KEY,
            reply_comment_id INT,
            root_comment_id INT,
            content TEXT,
            post_time INT,
            like_num INT,
            dislike_num INT,
            is_author BOOLEAN,
            headimgurl TEXT,
            nickname TEXT,
            FOREIGN KEY (thread_id) REFERENCES posts (thread_id)
            FOREIGN KEY (reply_comment_id) REFERENCES comments (comment_id),
            FOREIGN KEY (root_comment_id) REFERENCES comments (comment_id)
        )
    ''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()