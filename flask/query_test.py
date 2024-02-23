from flask import Flask, render_template, request
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session
from db_init import Thread, ImgPath, Comment, ReplyComment

session = Session((create_engine("sqlite:///data.db")))

posts_per_page = 20
page = 1
start = (page - 1) * posts_per_page

stmt = select(Thread).order_by(Thread.p_time.desc()).limit(posts_per_page).offset(start)
posts = session.scalars(stmt)

for post in posts:
    print(post.img_paths)