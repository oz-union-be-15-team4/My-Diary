from fastapi import FastAPI, Depends, Request, APIRouter
from app.db.database import init_db, close_db
from app.model.user import User
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers.user import router as user_router
from app.routers.user import get_current_user

app = FastAPI()

templates = Jinja2Templates(directory="app/frontend")

@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(user_router)

app.include_router(api_v1)


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
    return templates.TemplateResponse("bookmarks.html", context)
