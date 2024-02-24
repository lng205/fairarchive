from scripts.update import update_ids, update_posts
from app import app


def main():
    with app.app_context():
        update_ids()
        update_posts()


if __name__ == "__main__":
    main()
