# Тестування Assistant Bot

## Ручне тестування

### 1. Тест додавання контакту

```bash
> add John 1234567890
Contact added.

> add John 0987654321
Contact updated.

> phone John
Phone numbers for John: 1234567890, 0987654321
```

### 2. Тест валідації телефону

```bash
> add Alice 123
ValueError: Number must be 10 digits long and contain only digits. Current length: 3

> add Alice 12345abcde
ValueError: Number must be 10 digits long and contain only digits. Current length: 10
```

### 3. Тест днів народження

```bash
> add-birthday John 15.03.1990
Birthday for John added successfully.

> add-birthday Alice 32.13.2000
ValueError: Invalid date format. Use DD.MM.YYYY

> add-birthday Bob 01.01.2030
ValueError: Birth date cannot be in the future

> show-birthday John
John's birthday: 15.03.1990

> birthdays
# Показує контакти з днями народження в найближчі 7 днів
```

### 4. Тест редагування

```bash
> change John 1234567890 1111111111
Phone number for John changed from 1234567890 to 1111111111.

> rename John JohnDoe
Contact name changed from John to JohnDoe.

> rename JohnDoe Alice
Error: Contact Alice already exists.
```

### 5. Тест видалення

```bash
> delete-phone JohnDoe 1111111111
Phone 1111111111 removed from contact JohnDoe.

> delete JohnDoe
Contact JohnDoe deleted successfully.

> delete NonExistent
Error: Contact not found.
```

### 6. Тест збереження даних

```bash
# Додати контакти
> add Test1 1234567890
> add Test2 0987654321

# Вийти
> exit
Good bye!

# Запустити знову
python main.py

# Перевірити, що дані збереглися
> all
# Повинні відобразитися Test1 та Test2
```

### 7. Тест різних форматів збереження

```bash
# JSON
python main.py json
> add John 1234567890
> exit
# Перевірити файл files/addressbook.json

# CSV
python main.py csv
> add Alice 0987654321
> exit
# Перевірити файл files/addressbook.csv

# Pickle (за замовчуванням)
python main.py
> add Bob 5555555555
> exit
# Перевірити файл files/addressbook.pkl
```

### 8. Тест обробки помилок

```bash
> add
Error: Please provide contact name and phone number.

> change John
Error: Please provide contact name, old phone, and new phone.

> phone
Error: Please provide contact name.

> invalid_command
Invalid command.

# Програма не повинна закриватися при жодній з цих помилок
```

### 9. Тест автодоповнення

```bash
# Натиснути Tab після введення "ad"
> ad[Tab]
# Повинно показати: add, add-birthday, add-b

# Натиснути Tab після введення "del"
> del[Tab]
# Повинно показати: delete, delete-phone
```

### 10. Тест відображення таблиць

```bash
> add John 1234567890
> add Alice 0987654321
> add-birthday John 15.03.1990
> all

# Повинна відобразитися красива таблиця з колонками:
# Name | Phones | Birthday
```

## Перевірка PEP 8

```bash
# Встановити flake8
pip install flake8

# Перевірити код
flake8 . --max-line-length=100 --exclude=venv,__pycache__
```

## Перевірка типів (опціонально)

```bash
# Встановити mypy
pip install mypy

# Перевірити типи
mypy . --ignore-missing-imports
```

## Результати тестування

- ✅ Всі команди працюють коректно
- ✅ Валідація даних працює
- ✅ Помилки обробляються без закриття програми
- ✅ Дані зберігаються та завантажуються
- ✅ Підтримка різних форматів збереження
- ✅ Автодоповнення працює
- ✅ Таблиці відображаються коректно
- ✅ Код відповідає PEP 8
