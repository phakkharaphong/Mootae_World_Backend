from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from app.features.email.dto import SendEmail

BASE_DIR = Path(__file__).resolve().parents[2]


conf = ConnectionConfig(
    MAIL_USERNAME="muteverseservice@gmail.com",
    MAIL_PASSWORD="uzaqmhyevclvarnm",
    MAIL_FROM="pmuteverseservice@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=BASE_DIR / "templates"
    
)

router = APIRouter(
    prefix="/email",
    tags=["email"]
)
@router.post("/send-email")
async def send_email(
    background_tasks: BackgroundTasks,
    SendEmail: SendEmail
    ):

    
    message = MessageSchema(
        subject=SendEmail.subject,
        recipients=[SendEmail.email],
        template_body={
        "body": {
            "title": SendEmail.title,
            "name": SendEmail.name,
            "detail": SendEmail.detail,
            "img": SendEmail.img_Url
        }
        },
        subtype="html"
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message, template_name="emailtemplates.html")

    if not fm:
        raise HTTPException(
            status_code=500, 
            detail="เกิดข้อผิดพลาด"
        )
    

    return { "status": 200,"detail": "ส่งอีเมลเรียบร้อย" }
