from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

USERS_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_URL = "https://jsonplaceholder.typicode.com/posts"

users = requests.get(USERS_URL).json()
posts = requests.get(POSTS_URL).json()

posts_per_user = {}
for post in posts:
    uid = post["userId"]
    posts_per_user[uid] = posts_per_user.get(uid, 0) + 1

user_summary = []
for user in users:
    uid = user["id"]
    user_summary.append({
        "id": uid,
        "nama": user["name"],
        "email": user["email"],
        "kota": user["address"]["city"],
        "jumlah_post": posts_per_user.get(uid, 0)
    })


@app.get("test")
def root() :
    print("YOU SHALL NOT PASS!")
    return "BABABOEY"

@app.get("/users")
def get_users(kota: str = None):
    if kota:
        return [u for u in user_summary if u["kota"] == kota]
    return user_summary


@app.get("/users/{user_id}/posts")
def get_user_posts(user_id: int):

    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User tidak ditemukan"
        )

    user_posts = [
        post["title"] for post in posts if post["userId"] == user_id
    ]

    return {
        "user_id": user_id,
        "nama": user["name"],
        "posts": user_posts
    }
