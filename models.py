from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State, StatesGroup
from pydantic import BaseModel, Field


# ---------------- FSM: створення фільму ----------------
class FilmForm(StatesGroup):
    """Форма для створення нового фільму."""

    name = State()
    description = State()
    rating = State()
    genre = State()
    actors = State()
    poster = State()


# ---------------- CallbackData ----------------
class FilmCallback(CallbackData, prefix="film", sep=":"):
    """Callback для кнопок вибору фільму."""

    id: int
    name: str


# ---------------- Pydantic-модель ----------------
class Film(BaseModel):
    """Модель фільму (структура даних, яку ми зберігаємо у JSON)."""

    name: str = Field(..., description="Назва фільму")
    description: str = Field(..., description="Опис фільму")
    rating: float = Field(..., description="Рейтинг (0–10)")
    genre: str = Field(..., description="Жанр фільму")
    actors: list[str] = Field(default_factory=list, description="Список акторів")
    poster: str = Field(..., description="Посилання на постер фільму")


# ---------------- FSM: інші стани ----------------
class MovieState(StatesGroup):
    """Стани для пошуку, фільтрації, редагування та видалення фільмів."""

    search_q = State()
    filter_q = State()
    delete_q = State()
    edit_q = State()
    edit_description = State()