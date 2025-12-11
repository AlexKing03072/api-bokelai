from pydantic import BaseModel, ConfigDict, Field
#from datetime import datetime


class BookCreate(BaseModel):
    """書籍建立模型"""
    #title, author, publisher, price, publish_date, isbn, cover_url
    #model_config = ConfigDict(from_attributes=True)

    title: str | None = Field(None, title="書名", max_length=200)
    author: str | None = Field(None, title="作者", max_length=100)
    publisher: str | None = Field(None, title="出版社", max_length=100)
    price: int | None = Field(None, title="價格", gt=0)  # gt:greater than 有給的話必須 > 0
    publish_date: str | None = Field(None, title="出版日期", max_length=10)
    isbn: str | None = Field(None, title="ISBN", max_length=20)
    cover_url: str | None = Field(None, title="封面圖片 URL", max_length=200)
class BookResponse(BaseModel):
    """API 回傳的書籍模型"""
    id: int
    title: str
    author: str
    publisher: str | None
    price: int
    publish_date: str | None
    isbn: str | None
    cover_url: str | None
    created_at: str

    model_config = ConfigDict(from_attributes=True)
