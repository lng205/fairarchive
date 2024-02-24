from app import app, db
from app.models import Thread, Comment
from flask import render_template, request
from sqlalchemy import select, func


posts_per_page = 20

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * posts_per_page

    stmt = select(Thread).order_by(Thread.p_time.desc()).limit(posts_per_page).offset(start)
    posts = db.session.scalars(stmt)

    total_posts = db.session.scalar(select(func.count()).select_from(Thread))
    total_pages = (total_posts + posts_per_page - 1) // posts_per_page

    return render_template('index.html', posts=posts, page=page, total_pages=total_pages)


@app.route('/thread/<int:thread_id>')
def view_comments(thread_id):
    post = db.session.scalar(select(Thread).where(Thread.thread_id == thread_id))
    comments = db.session.scalars(select(Comment).where(Comment.thread_id == thread_id))

    return render_template('comments.html', post=post, comments=comments)


@app.route('/search')
def search_results():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * posts_per_page
    query = request.args.get('query')
    stmt = select(Thread).where(Thread.title.like(f'%{query}%')).limit(posts_per_page).offset(start)
    posts = db.session.scalars(stmt)

    total_posts = db.session.scalar(select(func.count()).where(Thread.title.like(f'%{query}%')))
    total_pages = (total_posts + posts_per_page - 1) // posts_per_page

    return render_template('search_results.html', posts=posts, page=page, total_pages=total_pages, query=query)
