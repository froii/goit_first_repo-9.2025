# PyPI Publishing Guide

## Встановлення
```bash
pip install build twine
```

## TestPyPI
```bash
# Реєстрація
https://test.pypi.org/account/register/
# Токен (показується 1 раз!)
https://test.pypi.org/manage/account/token/
# Формат: pypi-AgEIcHl...

# Опціонально: ~/.pypirc (C:\Users\ВашеІм'я\.pypirc)
[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-ВАШ_ТОКЕН

# Збірка
cd project-after-pycore
rm -rf dist/ build/ *.egg-info
python -m build
twine check dist/*

# Публікація
twine upload --repository testpypi dist/*
# Username: __token__
# Password: pypi-ТОКЕН (не відображається)

# Встановлення
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple assistant-bot-froii
assistant-bot
```

## PyPI
```bash
# Реєстрація
https://pypi.org/account/register/
# Токен
https://pypi.org/manage/account/token/

# Опціонально: ~/.pypirc
[pypi]
username = __token__
password = pypi-ВАШ_PYPI_ТОКЕН

# Публікація
twine upload dist/*

# Встановлення
pip install assistant-bot-froii
```

## Запуск проєкту
```bash
# З PyPI (після pip install assistant-bot-froii)
assistant-bot           # pickle (за замовчуванням)
assistant-bot json      # JSON формат
assistant-bot csv       # CSV формат

# З TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple assistant-bot-froii
assistant-bot

# Локально (без встановлення)
cd project-after-pycore
python main.py          # pickle
python main.py json     # JSON
python main.py csv      # CSV
```

## Оновлення
```bash
# Змінити version в pyproject.toml і setup.py: 1.0.0 → 1.0.1
rm -rf dist/ build/ *.egg-info
python -m build
twine check dist/*
twine upload --repository testpypi dist/*  # TestPyPI
twine upload dist/*                        # PyPI
pip install --upgrade assistant-bot-froii
```

## Помилки
- **403 Forbidden** → назва зайнята
- **File already exists** → змінити версію
- **Invalid authentication** → username: `__token__`, password: `pypi-...`

## Versioning
- `1.0.0 → 1.0.1` — bugfix
- `1.0.1 → 1.1.0` — нова функція
- `1.1.0 → 2.0.0` — breaking changes
