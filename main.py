from fastapi import FastAPI, HTTPException, Query, Path
from models import BookCreate, BookResponse
import database as db

# 1. 建立應用程式物件
app = FastAPI(title="博客來 AI 書籍管理 API",description="這是一個用於管理博客來書籍的 API", version="1.1.0")

# 2. 定義路由 (Route) 與 HTTP 方法 (GET)
# 當使用者連線到網站首頁 "/" 時，執行下方的函式
@app.get("/")
def root() -> dict[str, str]:
    """API 根路由"""
    # 3. 回傳資料 (FastAPI 會自動轉成 JSON 格式)
    return {"message": "AI Books API"}


@app.get("/books", response_model=list[BookResponse])
def get_all_books(
    skip: int = Query(0, ge=0, description="跳過前 N 筆"),
    limit: int = Query(5, ge=1, le=100, description="取得 N 筆"),# 預設5筆，最大100筆
)-> list[BookResponse]:
    """取得所有書籍（支援分頁）"""
    return db.get_all_books(skip, limit)


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int = Path(..., ge=1, description="書籍 ID")) -> BookResponse:
    """根據 ID 取得單一書籍"""
    book = db.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="書籍未找到")
    return book


@app.post(
        "/books",
        response_model=BookResponse,
        status_code=201 # 狀態碼預設是200，需自行設定狀態碼為 201。
)
def create_book(book: BookCreate) -> BookResponse:
    """建立新書籍"""
    try:
        book_data = book.model_dump()
        book_id = db.create_book(**book_data)
        if book_id is None:
            raise ValueError("Failed to create book.")
        new_book = db.get_book_by_id(book_id)
        return new_book
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"新增書籍時發生錯誤：{str(e)}")


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(
    book: BookCreate,
    book_id: int = Path(..., ge=1, description="書籍 ID"),
)-> BookResponse:
    """更新書籍"""
    try:
        book_data = book.model_dump()
        success = db.update_book(book_id, **book_data)
        if not success:
            raise HTTPException(status_code=404, detail="書籍未找到，無法更新")
        return db.get_book_by_id(book_id)
    except HTTPException:
    # 保留原本的 HTTP 狀態碼與訊息
        raise

    except Exception as e:
    # 「預期外」的錯誤，再轉成 500
        raise HTTPException(status_code=500, detail="更新書籍時發生錯誤")


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int = Path(..., ge=1, description="書籍 ID")) -> None:
    """刪除書籍"""
    try:
        success = db.delete_book(book_id)
        if not success:
            raise HTTPException(status_code=404, detail="書籍未找到，無法刪除")
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail="刪除書籍時發生錯誤")