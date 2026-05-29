from flask import session

from database import close_db, get_db


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None

    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            "SELECT user_id, username, email, role, created_at FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        close_db(db)