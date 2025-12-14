from fastapi import FastAPI
from app.core.database import Base, engine
from app.features.attachment.router import router as attachment_router
from app.features.blog.router import router as blog_router
from app.features.blog_homepage.router import router as blog_homepage_router
from app.features.category.router import router as category_router
from app.features.footer_website.router import router as footer_website_router
from app.features.location.router import router as location_router
from app.features.order.router import router as order_router
from app.features.order_type.router import router as order_type_router
from app.features.promotion.router import router as promotion_router
from app.features.role.router import router as role_router
from app.features.slide_activity.router import router as slide_activity_router
from app.features.slide_news.router import router as slide_news_router
from app.features.user.router import router as user_router


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
    root_path="/mootae_world_backend",
)

app.include_router(attachment_router)
app.include_router(blog_router)
app.include_router(blog_homepage_router)
app.include_router(category_router)
app.include_router(footer_website_router)
app.include_router(location_router)
app.include_router(order_router)
app.include_router(order_type_router)
app.include_router(promotion_router)
app.include_router(role_router)
app.include_router(slide_activity_router)
app.include_router(slide_news_router)
app.include_router(user_router)
