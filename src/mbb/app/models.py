from pydantic import BaseModel


class BookmarkItem(BaseModel):
    isin: str
