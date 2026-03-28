from fastapi import FastAPI
from database import Base, engine
from routers import users, transactions, admin

app = FastAPI(title="Income Expense API")

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(admin.router)

@app.get("/")
def home():
    return {"message": "Income Expense API is running"}
