import sqlite3
import time
import os

def seed():
    db_path = os.path.join(os.getcwd(), "hackathon.db")
    conn = sqlite3.connect(db_path)
    curr = conn.cursor()

    curr.execute("DROP TABLE IF EXISTS alerts")
    curr.execute('''CREATE TABLE alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        risk_level TEXT,
        risk_score INTEGER,
        reasons TEXT,
        label TEXT,
        public_ai_pastes INTEGER,
        personal_cloud_uploads INTEGER,
        risky_domain_visits INTEGER,
        unknown_domain_ratio REAL,
        off_hours_flag INTEGER,
        new_device_flag INTEGER,
        new_geo_flag INTEGER,
        activity_burst INTEGER,
        ts REAL
    )''')

    # Seeding R1 through R10 scenarios
    data = [
        ("EMP_01", "CRITICAL", 98, "R1", "confidential", 5, 0, 0, 0.1, 0, 0, 0, 10, time.time()),
        ("EMP_02", "CRITICAL", 95, "R2", "confidential", 0, 3, 0, 0.05, 0, 0, 0, 5, time.time() - 200),
        ("EMP_03", "HIGH", 88, "R3", "confidential", 0, 0, 12, 0.2, 0, 0, 0, 8, time.time() - 500),
        ("EMP_04", "MEDIUM", 65, "R4", "internal", 2, 0, 0, 0.1, 0, 0, 0, 15, time.time() - 900),
        ("EMP_05", "MEDIUM", 62, "R5", "internal", 0, 1, 0, 0.05, 0, 0, 0, 4, time.time() - 1200),
        ("EMP_06", "MEDIUM", 70, "R6", "public", 0, 0, 0, 0.6, 0, 0, 0, 20, time.time() - 1500),
        ("EMP_07", "MEDIUM", 68, "R7", "public", 0, 0, 5, 0.1, 0, 0, 0, 5, time.time() - 2000),
        ("EMP_08", "MEDIUM", 72, "R8", "internal", 0, 0, 0, 0.1, 1, 0, 0, 45, time.time() - 2500),
        ("EMP_09", "LOW", 45, "R9", "public", 0, 0, 0, 0.05, 0, 1, 0, 5, time.time() - 3000),
        ("EMP_10", "LOW", 42, "R10", "public", 0, 0, 0, 0.05, 0, 0, 1, 5, time.time() - 3500)
    ]

    curr.executemany('''INSERT INTO alerts 
        (user_id, risk_level, risk_score, reasons, label, public_ai_pastes, personal_cloud_uploads, 
         risky_domain_visits, unknown_domain_ratio, off_hours_flag, new_device_flag, new_geo_flag, activity_burst, ts) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', data)
    
    conn.commit()
    conn.close()
    print("✅ R1-R10 Threat Database Initialized.")

if __name__ == "__main__":
    seed()