from aiogram import Router, types
from aiogram.filters import Command

router = Router()

# /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("👋 Привіт! Я — твій бот. Використай /films або /create_film, щоб почати.")


# /films
@router.message(Command("films"))
async def cmd_films(message: types.Message):
    await message.answer("🎬 Ось список фільмів:\n1️⃣ Inception\n2️⃣ Interstellar\n3️⃣ The Matrix")


# /create_film
@router.message(Command("create_film"))
async def cmd_create_film(message: types.Message):
    await message.answer("✍️ Введи назву фільму, який хочеш додати:")