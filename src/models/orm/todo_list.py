from typing import Optional

from beanie import Document


class ToDoListItemDocument(Document):
    name: str
    description: Optional[str]
