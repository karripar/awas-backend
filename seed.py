"""
Seed script to populate the database with test users and posts
Run this after creating the database: python seed.py
"""

from database import get_db, close_db, init_db
from utils import simple_hash, generate_id
import sqlite3

SEED_DATA = {
    "users": [
        {
            "username": "admin_7f3a91",
            "email": "admin@awas.local",
            "password": "admin123",
            "role": "admin",
        },
        {
            "username": "joel",
            "email": "joel@awas.local",
            "password": "demo123",
            "role": "user",
        },
        {
            "username": "samu",
            "email": "samu@awas.local",
            "password": "demo123",
            "role": "user",
        },
        {
            "username": "karri",
            "email": "karri@awas.local",
            "password": "demo123",
            "role": "user",
        },
    ]
}


def seed_database():
    """Seed the database with test data"""
    init_db()

    db = get_db()
    cursor = db.cursor()

    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        print("Database already has users. Skipping seed.")
        close_db(db)
        return

    print("Seeding database with test users...")

    user_ids = {}

    # Insert users
    for user in SEED_DATA["users"]:
        user_id = generate_id()
        user_ids[user["username"]] = user_id

        try:
            cursor.execute(
                """
                INSERT INTO users (user_id, username, email, password, role)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    user_id,
                    user["username"],
                    user["email"],
                    simple_hash(user["password"]),
                    user["role"],
                ),
            )
            print(f"  Created user: {user['username']}")
        except sqlite3.IntegrityError:
            print(f"  User already exists: {user['username']}")

    # Insert posts
    posts = [
        {
            "username": "joel",
            "title": "Assignment scope",
            "text": "Review login, feed browsing, and admin actions for the demo.",
            "private": False,
        },
        {
            "username": "samu",
            "title": "Private notes",
            "text": "This entry should only be visible to trusted users in the real app.",
            "private": True,
        },
        {
            "username": "admin_7f3a91",
            "title": "Review checklist",
            "text": "The report should mention the attack surface and the intended weak points.",
            "private": False,
        },
    ]

    print("\nSeeding database with test posts...")

    for post in posts:
        if post["username"] in user_ids:
            post_id = generate_id()
            try:
                cursor.execute(
                    """
                    INSERT INTO posts (post_id, user_id, title, text, private)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        post_id,
                        user_ids[post["username"]],
                        post["title"],
                        post["text"],
                        int(post["private"]),
                    ),
                )
                print(f"  Created post: {post['title']}")
            except Exception as e:
                print(f"  Failed to create post: {e}")

    db.commit()
    close_db(db)
    print("\nDatabase seeding complete.")


if __name__ == "__main__":
    seed_database()
