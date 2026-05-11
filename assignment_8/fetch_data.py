import requests

USERS_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_URL = "https://jsonplaceholder.typicode.com/posts"

users_response = requests.get(USERS_URL)
posts_response = requests.get(POSTS_URL)

print("Status Users:", users_response.status_code)
print("Status Posts:", posts_response.status_code)

if users_response.status_code == 200 and posts_response.status_code == 200:
    users = users_response.json()
    posts = posts_response.json()
else:
    print("Error fetch")
    exit()

print("\nJumlah Users:", len(users))
print("Jumlah Posts:", len(posts))

print("\n## 3 Users")
print([f"{user['name']} - {user['email']}" for user in users[:3]])

print("\n## 5 Posts")

print([post['title'] for post in posts[:5]]) 

posts_per_user = {}

for post in posts:
    user_id = post["userId"]
    posts_per_user[user_id] = posts_per_user.get(user_id, 0) + 1

print("\n## Post / User")
print(posts_per_user)


user_summary = []

for user in users:
    uid = user["id"]
    summary = {
        "id": uid,
        "nama": user["name"],
        "email": user["email"],
        "kota": user["address"]["city"],
        "jumlah_post": posts_per_user.get(uid, 0)
    }
    user_summary.append(summary)


user_summary_sorted = sorted(
    user_summary, key=lambda x: x["jumlah_post"], reverse=True
)

print("\##nPodium Most Posts")
for i, user in enumerate(user_summary_sorted[:3], start=1):
    print(f"{i}. {user['nama']} ({user['kota']}) — {user['jumlah_post']} post")
