from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import aiosqlite

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для теста, для продакшена укажите домен фронта
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = "madjikfly.db"

@app.get("/api/user_info")
async def user_info(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        # Баланс
        async with db.execute("SELECT balance FROM users WHERE user_id=?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            balance = row[0] if row else 0
        # Аккаунты
        async with db.execute("SELECT insta_username FROM insta_accounts WHERE user_id=?", (user_id,)) as cursor:
            accounts = [r[0] for r in await cursor.fetchall()]
    return {"balance": balance, "accounts": accounts}   