from typing import List, Literal
from pydantic import BaseModel


class MessageSchema (BaseModel):
    subject: str
    body: str
    subtype: Literal["plain", "html"]

class SendEmail(BaseModel):
    subject: str
    email: str
    title: str
    name: str
    img_Url: str
    detail: str