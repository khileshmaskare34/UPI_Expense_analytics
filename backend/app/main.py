from fastapi import FastAPI
from app.db.session import SessionLocal
from app.db.init_db import init_db
from app.routers import auth
from app.routers import transactions
from app.routers import category
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="UPI Expense Analytics API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create DB tables when server starts
@app.on_event("startup")
def startup_event():
    init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Backend working !"}

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(category.router)

# start commend - uvicorn app.main:app --reload