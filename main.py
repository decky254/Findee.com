from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db import SessionLocal, engine
from models import Base, Link
from ai import analyze_query, generate_did_you_know

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Link Hub API")

# ✅ FIX: CORS (prevents frontend errors)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# 🏠 ROOT ENDPOINT (FIXES YOUR 404 ISSUE)
# -----------------------------
@app.get("/")
def home():
    return {
        "status": "AI Link Hub is running 🚀",
        "docs": "/docs",
        "endpoint": "/search (POST)"
    }

# -----------------------------
# REQUEST MODEL
# -----------------------------
class Query(BaseModel):
    text: str
    location: str = "Kenya"

# -----------------------------
# SEARCH ENDPOINT (AI POWERED)
# -----------------------------
@app.post("/search")
def search(query: Query):

    # 🧠 AI interpretation
    ai_result = analyze_query(query.text, query.location)

    db = SessionLocal()

    # 📊 Filter database using AI output
    results = db.query(Link).filter(
        Link.category == ai_result["category"],
        Link.subcategory == ai_result["subcategory"]
    ).all()

    db.close()

    # 💡 AI "Did you know" system
    did_you_know = generate_did_you_know(ai_result["category"])

    return {
        "ai_analysis": ai_result,
        "results": [
            {
                "title": r.title,
                "url": r.url,
                "category": r.category,
                "subcategory": r.subcategory
            }
            for r in results
        ],
        "did_you_know": did_you_know
    }
