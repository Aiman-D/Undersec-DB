import requests, random

users = ["aiman_admin", "staff_01", "dev_user"]
reasons = ["R1_SENSITIVE_PASTE", "R2_OFF_HOURS", "R3_UNAUTHORIZED_UPLOAD"]

for i in range(15):
    score = random.randint(20, 99)
    r_choice = random.choice(reasons) if score > 50 else ""
    requests.post("http://127.0.0.1:8000/ingest", params={
        "user_id": random.choice(users),
        "score": score,
        "pastes": random.randint(0, 20),
        "reasons": r_choice
    })
print("DB Seeded.")