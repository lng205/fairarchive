from scripts.update import update_ids, update_posts
from app import app


with app.app_context():
    update_ids()
    update_posts()