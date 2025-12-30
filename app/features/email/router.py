from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

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
    subject: str,
    email: str,
    title: str, 
    name: str, 
    img_Url: str, 
    detail: str
    ):

    
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        template_body={
        "body": {
            "title": title,
            "name": name,
            "detail": detail,
            "img": img_Url
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
