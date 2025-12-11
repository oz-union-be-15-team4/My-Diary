from fastapi import FastAPI, Depends, Request, APIRouter
from fastapi.responses import RedirectResponse
from app.db.database import init_db, close_db
from app.models.user import User
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers.user import router as user_router
from app.routers.question import router as question_router
from app.routers.quote import router as quote_router
from app.routers.diary import router as diary_router
from app.routers.user import get_current_user
from app.scripts.insert_question import seed_questions
from app.scripts.scrape_quotes import run_quote_scraper
from app.services.auth import verify_token
import asyncio

app = FastAPI()

templates = Jinja2Templates(directory="app/frontend")

@app.on_event("startup")
async def on_startup():

    await init_db()

    asyncio.create_task(seed_questions())
    asyncio.create_task(run_quote_scraper())
    print("명언 스크래핑 완료!")

@app.on_event("shutdown")
async def shutdown():
    await close_db()

api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(user_router)
api_v1.include_router(question_router)
api_v1.include_router(quote_router)
api_v1.include_router(diary_router)

app.include_router(api_v1)

@app.middleware("http")
async def auth_redirect_middleware(request: Request, call_next):
    path = request.url.path
    token = request.cookies.get("access_token")

    if path == "/" and token:
        payload = verify_token(token)
        if payload:
            return RedirectResponse(url="/dashboard", status_code=302)

    if path.startswith("/dashboard") and not token:
        return RedirectResponse(url="/", status_code=302)

    # 계속 진행
    response = await call_next(request)
    return response


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("index.html", context)

@app.get("/bookmarks", response_class=HTMLResponse)
def bookmarks(
        request: Request,
        current_user: User = Depends(get_current_user)
        ):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("page/bookmarks.html", context)

@app.get("/dashboard", response_class=HTMLResponse)
def bookmarks(
        request: Request,
        current_user: User = Depends(get_current_user)
        ):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("page/dashboard.html", context)

@app.get("/diaries", response_class=HTMLResponse)
def bookmarks(
        request: Request,
        current_user: User = Depends(get_current_user)
        ):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("page/diaries.html", context)

@app.get("/diaries/{diary_id}", response_class=HTMLResponse)
def bookmarks_detail(
        request: Request,
        diary_id: int,
        current_user: User = Depends(get_current_user)
        ):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("page/diaries_detail.html", context)
