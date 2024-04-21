from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class SaveArticle(BaseModel):
#     def save_article(title: str, content:str, tag:str, user_id: int):
    title: str
    content: str
    tag: str
    user_id: int
