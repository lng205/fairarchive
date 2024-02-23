from flask import Flask, render_template, request
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session
from db_init import Thread, ImgPath, Comment, ReplyComment

session = Session((create_engine("sqlite:///data.db")))
app = Flask(__name__)

posts_per_page = 20

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * posts_per_page

    stmt = select(Thread).order_by(Thread.p_time.desc()).limit(posts_per_page).offset(start)
    posts = session.scalars(stmt)

    total_posts = session.scalar(select(func.count()).select_from(Thread))
    total_pages = (total_posts + posts_per_page - 1) // posts_per_page

    return render_template('index.html', posts=posts, page=page, total_pages=total_pages)


@app.route('/thread/<int:thread_id>')
def view_comments(thread_id):
    post = session.scalar(select(Thread).where(Thread.thread_id == thread_id))
    comments = session.scalars(select(Comment).where(Comment.thread_id == thread_id))

    return render_template('comments.html', post=post, comments=comments)


@app.route('/search')
def search_results():
    pass
    # page = request.args.get('page', 1, type=int)
    # start = (page - 1) * posts_per_page
    # query = request.args.get('query')
    # posts = cursor.execute("SELECT * FROM posts WHERE title LIKE ? LIMIT ? OFFSET ?",
    #                        ('%' + query + '%', posts_per_page, start)).fetchall()
    
    # total_posts = cursor.execute("SELECT COUNT(*) as total FROM posts WHERE title LIKE ?", ('%' + query + '%', )).fetchone()['total']
    # total_pages = (total_posts + posts_per_page - 1) // posts_per_page

    # for post in posts:
    #     if post['img_paths']:
    #         post['img_paths'] = json.loads(post['img_paths'])
    # return render_template('search_results.html', posts=posts, page=page, total_pages=total_pages, query=query)


if __name__ == '__main__':
    app.run(debug=True)
