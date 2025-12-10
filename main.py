from fastapi import FastAPI, HTTPException
from models import BookCreate
import database as db

app = FastAPI(title="博客來 AI 書籍管理 API", version="1.0.0")
# 根路由

@app.get("/")
def root():
    """API 根路由"""
    return {"message": "AI Books API"}


@app.post("/posts", response_model=PostResponse, status_code=201)