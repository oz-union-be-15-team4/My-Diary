from fastapi import FastAPI, Depends, Request
from app.db.database import init_db
from app.model.user import User
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="app/front")

async def ensure_db():
    await init_db()


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("index.html", context)

@app.get("/users")
async def list_users(_=Depends(ensure_db)):
    users = await User.all()
    return users
