from flask import Flask, render_template, request
import sqlite3
import json


app = Flask(__name__)
DATABASE = '../data.db'
posts_per_page = 20


conn = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
# Convert the returned data to a dictionary, for json formatting
conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
cursor = conn.cursor()


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * posts_per_page
    posts = cursor.execute("SELECT * FROM posts ORDER BY p_time DESC LIMIT ? OFFSET ?", (posts_per_page, start)).fetchall()
    for post in posts:
        if post['img_paths']:
            post['img_paths'] = json.loads(post['img_paths'])

    total_posts = cursor.execute("SELECT COUNT(*) as total FROM posts").fetchone()['total']
    total_pages = (total_posts + posts_per_page - 1) // posts_per_page

    return render_template('index.html', posts=posts, page=page, total_pages=total_pages)


@app.route('/thread/<int:thread_id>')
def view_comments(thread_id):
    post = cursor.execute("SELECT * FROM posts WHERE thread_id = ?", (thread_id,)).fetchall()[0]
    if post['img_paths']:
        post['img_paths'] = json.loads(post['img_paths'])

    comments = cursor.execute("SELECT * FROM comments WHERE thread_id = ?", (thread_id,)).fetchall()
    
    # Mapping id with comment
    comment_id_dict = {comment['comment_id']: comment for comment in comments}

    # Organize comments into a nested structure
    for comment in comments:
        if comment['root_comment_id'] != 0:
            # Get the root_comment
            root_comment = comment_id_dict[comment['root_comment_id']]

            if comment['reply_comment_id'] != 0 and comment['reply_comment_id'] != comment['root_comment_id']:
                # Store the nickname of the reply_to comment
                comment['reply_to'] = comment_id_dict[comment['reply_comment_id']]['nickname']

            # Add the comment to the replies of the root comment
            if 'replies' not in root_comment:
                root_comment['replies'] = []
            root_comment['replies'].append(comment)

    root_comments = [comment for comment in comments if comment['root_comment_id'] == 0]

    return render_template('comments.html', post=post, comments=root_comments)


@app.route('/search')
def search_results():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * posts_per_page
    query = request.args.get('query')
    posts = cursor.execute("SELECT * FROM posts WHERE title LIKE ? LIMIT ? OFFSET ?",
                           ('%' + query + '%', posts_per_page, start)).fetchall()
    
    total_posts = cursor.execute("SELECT COUNT(*) as total FROM posts WHERE title LIKE ?", ('%' + query + '%', )).fetchone()['total']
    total_pages = (total_posts + posts_per_page - 1) // posts_per_page

    for post in posts:
        if post['img_paths']:
            post['img_paths'] = json.loads(post['img_paths'])
    return render_template('search_results.html', posts=posts, page=page, total_pages=total_pages, query=query)


if __name__ == '__main__':
    app.run(debug=True)
