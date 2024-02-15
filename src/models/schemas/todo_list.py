from typing import List, Optional

from pydantic import BaseModel


class TodDoListItemSchema(BaseModel):
    name: str
    description: Optional[str]


class ToDoListSchema(BaseModel):
    items: List[TodDoListItemSchema]
