from fastapi import FastAPI, Depends
from app.db.database import init_db
from app.model.user import User

app = FastAPI()

async def ensure_db():
    await init_db()


@app.get("/")
def root():
    return {"message": "FastAPI 정상 작동 중 ✅"}

@app.get("/users")
async def list_users(_=Depends(ensure_db)):
    users = await User.all()
    return users
