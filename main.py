import time, uuid, random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# DB CONFIG
DATABASE_URL = "sqlite:///./hackathon.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- TABLES ---
class Window(Base):
    __tablename__ = "windows"
    window_id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    risk_score = Column(Integer)
    risk_level = Column(String)
    recommended_action = Column(String)
    window_start_ts = Column(Integer)
    
    features = relationship("WindowFeature", back_populates="window", uselist=False)
    reasons = relationship("Reason", back_populates="window")

class WindowFeature(Base):
    __tablename__ = "window_features"
    window_id = Column(String, ForeignKey("windows.window_id"), primary_key=True)
    public_ai_paste_count = Column(Integer, default=0)
    window = relationship("Window", back_populates="features")

class Reason(Base):
    __tablename__ = "reasons"
    reason_id = Column(String, primary_key=True)
    window_id = Column(String, ForeignKey("windows.window_id"))
    code = Column(String)
    window = relationship("Window", back_populates="reasons")

Base.metadata.create_all(bind=engine)

# API
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/ingest")
def ingest(user_id: str, score: int, pastes: int = 0, reasons: str = ""):
    db = SessionLocal()
    wid = str(uuid.uuid4())
    level = "LOW"
    if score >= 90: level = "CRITICAL"
    elif score >= 70: level = "HIGH"
    
    try:
        win = Window(window_id=wid, user_id=user_id, risk_score=score, 
                     risk_level=level, window_start_ts=int(time.time()))
        db.add(win)
        db.add(WindowFeature(window_id=wid, public_ai_paste_count=pastes))
        if reasons:
            for c in reasons.split(","):
                db.add(Reason(reason_id=str(uuid.uuid4()), window_id=wid, code=c))
        db.commit()
        return {"status": "success"}
    finally:
        db.close()

@app.get("/alerts")
def get_alerts():
    db = SessionLocal()
    results = db.query(Window).order_by(Window.window_start_ts.desc()).all()
    output = []
    for r in results:
        output.append({
            "user_id": r.user_id,
            "risk_score": r.risk_score,
            "risk_level": r.risk_level,
            "reasons": [re.code for re in r.reasons],
            "pastes": r.features.public_ai_paste_count if r.features else 0,
            "ts": r.window_start_ts
        })
    db.close()
    return output