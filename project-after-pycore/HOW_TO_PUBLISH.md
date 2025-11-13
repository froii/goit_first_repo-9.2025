# PyPI Publishing Guide

## Встановлення
```bash
pip install build twine
```

## TestPyPI
```bash
# 1. Реєстрація
https://test.pypi.org/account/register/

# 2. Отримати токен (показується лише 1 раз!)
https://test.pypi.org/manage/account/token/
# Add API token → Name: assistant-bot → Scope: Entire account → Create token
# Формат токену: pypi-AgEIcHlQIi1d...

# 3. Опціонально: створити ~/.pypirc (C:\Users\ВашеІм'я\.pypirc)
[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-ВАШ_ТОКЕН_ТУТ

# 4. Збірка
cd project-after-pycore
rm -rf dist/ build/ *.egg-info
python -m build
twine check dist/*

# Публікація
twine upload --repository testpypi dist/*
# Якщо немає .pypirc, введіть вручну:
# Username: __token__
# Password: pypi-ВАШ_ТОКЕН (не відображається під час вводу)

# Встановлення
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple assistant-bot-froii
assistant-bot
```

## PyPI
```bash
# 1. Реєстрація
https://pypi.org/account/register/

# 2. Отримати токен
https://pypi.org/manage/account/token/
# Add API token → Name: assistant-bot → Scope: Entire account → Create token

# 3. Опціонально: додати в ~/.pypirc
[pypi]
username = __token__
password = pypi-ВАШ_PYPI_ТОКЕН

# 4. Публікація
twine upload dist/*

# Встановлення
pip install assistant-bot-froii
```

## Оновлення версії
```bash
# 1. Змінити version в pyproject.toml і setup.py: 1.0.0 → 1.0.1
# 2. Пересобрати
rm -rf dist/ build/ *.egg-info
python -m build
twine upload dist/*
```

## Помилки
- **403 Forbidden** → назва зайнята, змінити в pyproject.toml і setup.py
- **File already exists** → змінити версію
- **Invalid authentication** → username: `__token__`, password: `pypi-...`

## Versioning
- `1.0.0 → 1.0.1` — bugfix
- `1.0.1 → 1.1.0` — нова функція
- `1.1.0 → 2.0.0` — breaking changes
