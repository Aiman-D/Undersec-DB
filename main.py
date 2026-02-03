from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DB_PATH = os.path.join(os.getcwd(), "hackathon.db")

@app.get("/alerts")
def get_alerts(token: str = None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    curr = conn.cursor()
    
    try:
        curr.execute("SELECT * FROM alerts ORDER BY ts DESC")
        rows = [dict(r) for r in curr.fetchall()]
    except:
        rows = []
    finally:
        conn.close()

    # Clean up the 'reasons' string into a list for the tags
    for r in rows:
        r['reasons'] = r['reasons'].split(',')
    
    return {"client": "SYSTEM_ARCHITECT", "alerts": rows}