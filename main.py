from fastapi import FastAPI
from db import SessionLocal, engine
from models import Base, Link
from ai import analyze_query, generate_did_you_know
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI()

class Query(BaseModel):
    text: str
    location: str = "Kenya"


# Seed fallback data (you can expand later)
SEED = [
    {"title": "Remote Dev Jobs Group", "url": "https://t.me/example1", "category": "Jobs", "subcategory": "Remote", "location": "Kenya"},
    {"title": "Nairobi Business Network", "url": "https://chat.whatsapp.com/example2", "category": "Business", "subcategory": "Networking", "location": "Kenya"},
    {"title": "Forex Signals Group", "url": "https://t.me/example3", "category": "Trading", "subcategory": "Forex", "location": "Global"}
]


@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    if db.query(Link).first() is None:
        for item in SEED:
            db.add(Link(**item))
        db.commit()
    db.close()


@app.post("/search")
def search(query: Query):

    ai = analyze_query(query.text, query.location)

    db = SessionLocal()

    results = db.query(Link).filter(
        Link.category == ai["category"],
        Link.subcategory == ai["subcategory"]
    ).all()

    db.close()

    did_you_know = generate_did_you_know(ai["category"])

    return {
        "ai_analysis": ai,
        "results": [
            {"title": r.title, "url": r.url} for r in results
        ],
        "did_you_know": did_you_know
  }
