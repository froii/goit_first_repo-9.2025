
Спосіб 1: Без встановлення (швидкий тест)
# Встановити залежності
pip install -r project-after-pycore/requirements.txt

# Запустити з pickle (за замовчуванням)
python project-after-pycore/main.py

# Або з JSON
python project-after-pycore/main.py json

# Або з CSV
python project-after-pycore/main.py csv


Спосіб 2: Встановити як пакет (рекомендовано)
# Перейти в директорію проєкту
cd project-after-pycore

# Встановити пакет
pip install -e .

# Тепер можна викликати з будь-якого місця
assistant-bot
assistant-bot json
assistant-bot csv


# Assistant Bot - Personal Contact Manager

Бот-асистент для управління контактами з підтримкою днів народження, різних форматів збереження даних та зручним командним інтерфейсом.

## Особливості

- ✅ Управління контактами (додавання, редагування, видалення)
- ✅ Збереження телефонів та днів народження
- ✅ Нагадування про найближчі дні народження
- ✅ Підтримка 3 форматів збереження: Pickle, JSON, CSV
- ✅ Автодоповнення команд
- ✅ Красиве відображення даних у таблицях
- ✅ Валідація введених даних
- ✅ Обробка помилок без закриття програми

## Структура проекту

```
project-after-pycore/
├── models/              # Моделі даних
│   ├── fields.py       # Field, Name, Phone, Birthday
│   ├── record.py       # Record
│   ├── address_book.py # AddressBook
│   └── __init__.py
├── handlers/           # Обробники команд
│   ├── command_handler.py  # CommandHandler
│   ├── decorators.py       # Декоратори для обробки помилок
│   └── __init__.py
├── ui/                 # UI компоненти
│   ├── table_renderer.py   # TableRenderer
│   ├── styles.py           # Стилі для prompt_toolkit
│   └── __init__.py
├── storage/            # Робота з файлами
│   ├── file_storage.py     # FileStorage
│   └── __init__.py
├── constants.py        # Константи
├── main.py            # Точка входу
├── requirements.txt   # Залежності
└── README.md         # Документація
```

## Принципи SOLID

- **S (Single Responsibility)**: Кожен клас має одну відповідальність
  - `PickleStorage/JSONStorage/CSVStorage` - тільки робота з файлами
  - `TableRenderer` - тільки відображення таблиць
  - `CommandHandler` - тільки обробка команд

- **O (Open/Closed)**: Легко додавати нові команди та типи збереження без зміни існуючого коду

- **L (Liskov Substitution)**: Всі Storage класи можуть замінювати StorageInterface

- **I (Interface Segregation)**: Кожен клас має мінімальний інтерфейс

- **D (Dependency Inversion)**: Залежності передаються через конструктор, використовується абстракція StorageInterface

## Патерни проектування

- **Strategy Pattern**: Різні стратегії збереження (Pickle, JSON, CSV)
- **Factory Pattern**: StorageFactory створює потрібний тип збереження

## Встановлення

### Варіант 1: Встановлення як Python-пакет (рекомендовано)

```bash
# Клонувати репозиторій
git clone https://github.com/yourusername/assistant-bot.git
cd assistant-bot

# Встановити пакет
pip install -e .

# Тепер можна викликати з будь-якого місця
assistant-bot
assistant-bot json
```

### Варіант 2: Запуск без встановлення

```bash
# Встановити залежності
pip install -r requirements.txt

# Запустити
python main.py
```

### Вимоги

- Python 3.8 або вище
- pip (менеджер пакетів Python)

## Запуск

```bash
# За замовчуванням (pickle)
python main.py

# З вибором формату збереження
python main.py json    # JSON формат
python main.py csv     # CSV формат
python main.py pickle  # Pickle формат
```

## Команди

### Управління контактами
- `add [name] [phone]` - Додати новий контакт або телефон до існуючого
- `delete [name]` або `remove [name]` - Видалити контакт
- `edit-name [old] [new]` або `rename [old] [new]` - Перейменувати контакт
- `all` або `list` - Показати всі контакти

### Управління телефонами
- `phone [name]` - Показати телефони контакту
- `change [name] [old] [new]` - Змінити телефон
- `delete-phone [name] [phone]` - Видалити телефон з контакту

### Дні народження
- `add-birthday [name] [DD.MM.YYYY]` або `add-b [name] [DD.MM.YYYY]` - Додати день народження
- `show-birthday [name]` - Показати день народження контакту
- `birthdays` - Показати найближчі дні народження (7 днів)

### Інше
- `hello` або `hi` - Привітання
- `help` - Показати всі команди
- `exit` або `close` - Вийти з програми

## Приклади використання

```bash
# Додати контакт
> add John 1234567890
Contact added.

# Додати ще один телефон
> add John 0987654321
Contact updated.

# Додати день народження
> add-birthday John 15.03.1990
Birthday for John added successfully.

# Показати всі контакти
> all
# Відобразиться таблиця з контактами

# Перейменувати контакт
> rename John JohnDoe
Contact name changed from John to JohnDoe.

# Видалити телефон
> delete-phone JohnDoe 1234567890
Phone 1234567890 removed from contact JohnDoe.

# Видалити контакт
> delete JohnDoe
Contact JohnDoe deleted successfully.
```

## Валідація даних

- **Телефон**: повинен містити рівно 10 цифр
- **День народження**: формат DD.MM.YYYY, не може бути в майбутньому, вік не більше 100 років
- **Ім'я**: обов'язкове поле

## Обробка помилок

Програма коректно обробляє всі помилки:
- Некоректний формат телефону
- Неправильна дата народження
- Відсутній контакт
- Дублювання імен при перейменуванні
- Помилки читання/запису файлів

Програма не закривається при помилках, а виводить зрозуміле повідомлення.
