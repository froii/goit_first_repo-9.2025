
from pathlib import Path


def get_cats_info(path: str | Path) -> list[dict[str, str]]:
    try:
        with open(path, 'r', encoding='utf-8') as cat_file:
            cats = []
            for line in cat_file:
                try:
                    id, name, age = line.strip().split(',')
                    cats.append({"id": id, "name": name, "age": age})
                except ValueError:
                    print(f"Skipping invalid line: {line.strip()}")
                    continue

            return cats
        
    except (FileNotFoundError, OSError):
        print(f"Error opening/reading file {path}")
        return []

# Функція має точно обробляти дані та повертати правильний список словників.
# Повинна бути належна обробка винятків і помилок.
# Код має бути чистим, добре структурованим і зрозумілим.

cats_path = Path(__file__).resolve().parent / "path/to/cats_file.txt"
cats_info = get_cats_info(cats_path)
print(cats_info)

# Очікуваний результат:
# [
#     {"id": "60b90c1c13067a15887e1ae1", "name": "Tayson", "age": "3"},
#     {"id": "60b90c2413067a15887e1ae2", "name": "Vika", "age": "1"},
#     {"id": "60b90c2e13067a15887e1ae3", "name": "Barsik", "age": "2"},
#     {"id": "60b90c3b13067a15887e1ae4", "name": "Simon", "age": "12"},
#     {"id": "60b90c4613067a15887e1ae5", "name": "Tessi", "age": "5"},
# ]
