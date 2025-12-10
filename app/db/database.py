# app/db/database.py
import os
from tortoise import Tortoise
from dotenv import load_dotenv

load_dotenv()

DB_URL = (
    f"postgres://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

async def init_db():
    print("DB INIT 시작")
    await Tortoise.init(
        db_url=DB_URL,
        modules={
            "models": ["app.models.user",
                       "app.models.bookmark",
                       "app.models.diary",
                       "app.models.question",
                       "app.models.quote",
                       ]
        },
    )
    await Tortoise.generate_schemas()
    print("DB INIT 완료")

async def close_db():
    await Tortoise.close_connections()