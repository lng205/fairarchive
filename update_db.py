from scripts.upsert import upcert_id, upcert_post, Post
from app import app, db
from datetime import datetime, timezone

timestamp_95h_ago = int(datetime.now(timezone.utc).timestamp()) - 95 * 3600

with app.app_context():
    earlest_p_time = str(timestamp_95h_ago)
    while True:
        response = Post.get_ids(earlest_p_time)
        post_list = response.json()["data"]["list"]

        for post in post_list:
            upcert_id(post, db.session)
            upcert_post(post["thread_id"], db.session)

        try:
            earlest_p_time = post_list[-1]["p_time"]
        except Exception:
            break

    db.session.commit()