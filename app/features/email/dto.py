from typing import List, Literal
from pydantic import BaseModel


class MessageSchema (BaseModel):
    subject: str
    body: str
    subtype: Literal["plain", "html"]