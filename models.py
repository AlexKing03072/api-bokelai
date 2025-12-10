from pydantic import BaseModel, ConfigDict, Field

class BookCreate(BaseModel):
    """書籍建立模型"""
    #title, author, publisher, price, publish_date, isbn, cover_url
    #model_config = ConfigDict(from_attributes=True)

    title: str = Field(..., title="書名", max_length=200)
    author: str = Field(..., title="作者", max_length=100)
    publisher: str | None = Field(None, title="出版社", max_length=100)
    price: int = Field(..., title="價格", ge=0)#ge=0 表示價格不能為負數
    publish_date: str | None = Field(None, title="出版日期", max_length=10)
    isbn: str | None = Field(None, title="ISBN", max_length=20)
    cover_url: str | None = Field(None, title="封面圖片 URL", max_length=200)