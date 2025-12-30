from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.database import Base, engine
from app.features.attachment.router import router as attachment_router
from app.features.blog.router import router as blog_router
from app.features.blog_homepage.router import router as blog_homepage_router
from app.features.category.router import router as category_router
from app.features.footer_website.router import router as footer_website_router
from app.features.location.router import router as location_router
from app.features.order.router import router as order_router
from app.features.order_payment.router import router as order_payment_router
from app.features.order_type.router import router as order_type_router
from app.features.promotion.router import router as promotion_router
from app.features.slide_activity.router import router as slide_activity_router
from app.features.slide_news.router import router as slide_news_router
from app.features.user.router import router as user_router
from app.features.auth.router import router as auth_router
from app.features.wallpaper_collection.router import (
    router as wallpaper_collection_router,
)
from app.features.wallpaper.router import router as wallpaper_router
from app.features.email.router import router as email_router
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mootae World API Doccument",
    description="This is a API Docuemtn Project Mootae World API.",
    version="1.0.0",
    contact={
        "name": "API Support",
        "url": "http://example.com/contact",
        "email": "phakkharaphong.c@kkumail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    root_path="/muteverse",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user_router)
api_router.include_router(auth_router)
api_router.include_router(attachment_router)
api_router.include_router(email_router)
api_router.include_router(blog_router)
api_router.include_router(blog_homepage_router)
api_router.include_router(category_router)
api_router.include_router(footer_website_router)
api_router.include_router(location_router)
api_router.include_router(order_router)
api_router.include_router(order_payment_router)
api_router.include_router(order_type_router)
api_router.include_router(promotion_router)
api_router.include_router(slide_activity_router)
api_router.include_router(slide_news_router)
api_router.include_router(wallpaper_router)
api_router.include_router(wallpaper_collection_router)

app.include_router(api_router)
