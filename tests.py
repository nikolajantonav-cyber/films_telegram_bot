import os
import json
import pytest
import helpers


@pytest.fixture
def temp_films_file(tmp_path):
    """Створює тимчасовий файл з тестовими фільмами."""
    data = [
        {
            "name": "Harry Potter and the Philosopher's Stone",
            "description": "The first Harry Potter film.",
            "rating": 9.0,
            "genre": "Fantasy",
            "actors": ["Daniel Radcliffe", "Emma Watson"],
            "poster": "https://example.com/harry.jpg"
        },
        {
            "name": "Inception",
            "description": "A sci-fi movie about dreams.",
            "rating": 8.8,
            "genre": "Sci-Fi",
            "actors": ["Leonardo DiCaprio"],
            "poster": "https://example.com/inception.jpg"
        }
    ]
    file_path = tmp_path / "films.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return str(file_path)


def test_get_films(temp_films_file):
    films = helpers.get_films(temp_films_file)
    assert isinstance(films, list)
    assert len(films) == 2


def test_get_films_creates_file(tmp_path):
    path = tmp_path / "empty.json"
    films = helpers.get_films(str(path))
    assert isinstance(films, list)
    assert films == []


def test_get_film_valid(temp_films_file):
    film = helpers.get_film(temp_films_file, 0)
    assert film["name"] == "Harry Potter and the Philosopher's Stone"


def test_get_film_invalid_index(temp_films_file):
    film = helpers.get_film(temp_films_file, 10)
    assert film is None


def test_add_film(temp_films_file):
    new_film = {
        "name": "Matrix",
        "description": "Simulation movie",
        "rating": 8.5,
        "genre": "Sci-Fi",
        "actors": ["Keanu Reeves"],
        "poster": "https://example.com/matrix.jpg"
    }
    helpers.add_film(new_film, temp_films_file)
    films = helpers.get_films(temp_films_file)
    assert len(films) == 3
    assert films[-1]["name"] == "Matrix"


def test_delete_film(temp_films_file):
    deleted = helpers.delete_film("Inception", temp_films_file)
    assert deleted is not None
    assert deleted["name"] == "Inception"
    films = helpers.get_films(temp_films_file)
    assert len(films) == 1