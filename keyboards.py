from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from helpers import get_films
from models import FilmCallback


# Основна клавіатура дій
films_action_keyboard = ReplyKeyboardMarkup(
    input_field_placeholder="Select an action...",
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🔍 Search"),
            KeyboardButton(text="📂 Filter"),
            KeyboardButton(text="🗑 Delete"),
        ]
    ],
)


# Клавіатура зі списком фільмів
def build_keyboard_for_films() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    films = get_films("films.json")

    # Якщо немає фільмів — повертаємо повідомлення
    if not films:
        builder.add(
            InlineKeyboardButton(
                text="❌ No films found", callback_data="no_films"
            )
        )
        return builder.as_markup()

    for index, film_data in enumerate(films):
        callback_data = FilmCallback(id=index, name=film_data["name"])
        builder.add(
            InlineKeyboardButton(
                text=callback_data.name,
                callback_data=callback_data.pack()
            )
        )

    # Відображати по 1 фільму в рядку
    builder.adjust(1)
    return builder.as_markup()