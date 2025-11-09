import json
import os


def get_films(file_path: str) -> list[dict]:
    """Отримуємо всі фільми із файлу в форматі списку словників."""
    if not os.path.exists(file_path):
        # Якщо файл не існує, створюємо порожній список
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)
        return []

    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Якщо файл пошкоджений або порожній
        return []


def get_film(file_path: str, film_id: int) -> dict | None:
    """Отримаємо один фільм за його ID (індекс у списку)."""
    films = get_films(file_path)
    if 0 <= film_id < len(films):
        return films[film_id]
    return None


def add_film(film: dict, file_path: str) -> None:
    """Додаємо фільм у файл (створюємо, якщо не існує)."""
    films = get_films(file_path)
    films.append(film)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(films, f, ensure_ascii=False, indent=4)


def delete_film(name: str, file_path: str = "films.json") -> dict | None:
    """Видаляємо фільм за назвою (регістр не має значення)."""
    films = get_films(file_path)
    film_to_delete = None

    for index, film in enumerate(films):
        if film.get("name", "").lower() == name.lower():
            film_to_delete = films.pop(index)
            break

    if film_to_delete is not None:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(films, f, ensure_ascii=False, indent=4)

    return film_to_delete