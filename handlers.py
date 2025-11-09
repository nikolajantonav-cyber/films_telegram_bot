from aiogram import Router, F, html
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from helpers import add_film, get_film, delete_film
from keyboards import build_keyboard_for_films, films_action_keyboard
from models import Film, FilmCallback, FilmForm, MovieState
router = Router(name=__name__)


# ---------------- Команди ----------------

@router.message(CommandStart())
async def handle_cmd_start(message: Message) -> None:
    await message.answer(
        f"👋 Hello {html.bold(message.from_user.full_name)}!",
        reply_markup=films_action_keyboard
    )


@router.message(Command("films"))
async def handle_get_films(message: Message) -> None:
    await message.answer("🎬 List of films:", reply_markup=build_keyboard_for_films())


@router.message(Command("create_film"))
async def handle_film_creation(message: Message, state: FSMContext) -> None:
    await state.set_state(FilmForm.name)
    await message.answer("✍️ Enter film name:", reply_markup=ReplyKeyboardRemove())


# ---------------- FSM: створення фільму ----------------

@router.message(FilmForm.name)
async def handle_film_name_state(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(FilmForm.description)
    await message.answer("📄 Enter film description:")


@router.message(FilmForm.description)
async def handle_film_description_state(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(FilmForm.rating)
    await message.answer("⭐ Enter film rating:")


@router.message(FilmForm.rating)
async def handle_film_rating_state(message: Message, state: FSMContext) -> None:
    await state.update_data(rating=message.text)
    await state.set_state(FilmForm.genre)
    await message.answer("🎭 Enter film genre:")


@router.message(FilmForm.genre)
async def handle_film_genre_state(message: Message, state: FSMContext) -> None:
    await state.update_data(genre=message.text)
    await state.set_state(FilmForm.actors)
    await message.answer("🧑‍🎤 Enter film actors (comma separated):")


@router.message(FilmForm.actors)
async def handle_film_actors_state(message: Message, state: FSMContext) -> None:
    await state.update_data(actors=message.text.split(", "))
    await state.set_state(FilmForm.poster)
    await message.answer("🖼️ Enter film poster URL:")


@router.message(FilmForm.poster)
async def handle_film_poster_state(message: Message, state: FSMContext) -> None:
    await state.update_data(poster=message.text)
    film_data = await state.get_data()

    film = Film(**film_data)
    add_film(film.model_dump(), "films.json")
    await state.clear()

    await message.answer(f"✅ Film <b>{film.name}</b> has been added!", reply_markup=films_action_keyboard)


# ---------------- Callbacks ----------------

@router.callback_query(FilmCallback.filter())
async def handle_films_callback(callback: CallbackQuery, callback_data: FilmCallback) -> None:
    await callback.answer()
    film_id = callback_data.id
    film_data = get_film("films.json", film_id)

    if not film_data:
        await callback.message.answer("❌ Film not found!")
        return

    film = Film(**film_data)
    text = (
        f"🎬 <b>{film.name}</b>\n\n"
        f"📝 {film.description}\n\n"
        f"⭐ Rating: {film.rating}\n"
        f"🎭 Genre: {film.genre}\n"
        f"🧑‍🎤 Actors: {', '.join(film.actors)}"
    )
    await callback.message.answer_photo(photo=film.poster, caption=text)


# ---------------- Видалення фільму ----------------

@router.message(F.text.contains("Delete"))
async def handle_delete_film_request(message: Message, state: FSMContext) -> None:
    await state.set_state(MovieState.delete_q)
    await message.answer("❌ Enter the name of the film to delete:", reply_markup=ReplyKeyboardRemove())


@router.message(MovieState.delete_q)
async def handle_delete_film_process(message: Message, state: FSMContext) -> None:
    await state.update_data(delete_q=message.text)
    data = await state.get_data()

    result = delete_film(name=data["delete_q"].lower())
    if result is None:
        await message.answer(f"⚠️ Film <b>{data['delete_q']}</b> does not exist!")
    else:
        await message.answer(f"🗑️ Film <b>{data['delete_q']}</b> has been deleted!")

    await state.clear()


# ---------------- Ехо ----------------

@router.message()
async def handle_echo(message: Message) -> None:
    await message.copy_to(message.chat.id)