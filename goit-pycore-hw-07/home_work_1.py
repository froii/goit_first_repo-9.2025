import re
from collections import UserDict
from datetime import datetime, timedelta

DATE_FORMAT = "%d.%m.%Y"


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


# Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Номер телефону повинен містити рівно 10 цифр")
        super().__init__(value)

    def validate(self, phone):
        return phone.isdigit() and len(phone) == 10


class Birthday(Field):
    def __init__(self, value):
        if self.validate(value):
            # та перетворіть рядок на об'єкт datetime
            date = datetime.strptime(value, DATE_FORMAT)
            super().__init__(date)

    # Додайте перевірку коректності даних
    # def validate(self, date):
    #     return re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{4}", date) is not None

    def validate(self, date):
        # 1. Перевірка базового формату (DD.MM.YYYY)
        if not re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{4}", date):
            return False

        try:
            # 2. Перевірка чи дата реально існує (не 31.02.2024 наприклад)
            parsed_date = datetime.strptime(date, DATE_FORMAT)

            # 3. Перевірка що рік в розумних межах (не в майбутньому, не занадто давно)
            current_year = datetime.now().year
            if parsed_date.year > current_year:
                raise ValueError("Дата народження не може бути в майбутньому")

            # Перевірка мінімального року (наприклад, не раніше 1900)
            if parsed_date.year < 1900:
                raise ValueError("Дата народження занадто давня (раніше 1900 року)")

            # 4. Перевірка максимального віку (наприклад, не більше 150 років)
            age = current_year - parsed_date.year
            if age > 150:
                raise ValueError("Вік не може перевищувати 150 років")

            # 5. Перевірка що день і місяць в допустимих межах
            if not (1 <= parsed_date.day <= 31):
                raise ValueError("День має бути від 1 до 31")
            if not (1 <= parsed_date.month <= 12):
                raise ValueError("Місяць має бути від 1 до 12")

            return True

        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


# Record: Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
# Додавання телефонів
# Видалення телефонів
# Редагування телефонів
# Пошук телефону


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)
        if not phone_obj:
            raise ValueError(f"Phone {old_phone} does not exist.")

        index = self.phones.index(phone_obj)
        self.phones[index] = Phone(new_phone)

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    # Це поле не обов'язкове, але може бути тільки одне. - це значить що воно не мутабельне чи просто одне і оновлюється?
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = "; ".join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


# AddressBook: Клас для зберігання та управління записами.
# Додавання записів
# Пошук записів за іменем
# Видалення записів за іменем


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    # Додайте та адаптуйте до класу AddressBook нашу функцію з четвертого домашнього завдання, тиждень 3, get_upcoming_birthdays,
    # яка для контактів адресної книги повертає список користувачів, яких потрібно привітати по днях на наступному тижні.
    def get_upcoming_birthdays(self) -> list[dict[str, str]]:
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        birthdays = []

        for user_data in self.data.values():
            if not user_data.birthday or not user_data.birthday.value:
                continue

            birthday = user_data.birthday.value.date()
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if birthday_this_year >= today and birthday_this_year < next_week:
                if birthday_this_year.weekday() in (5, 6):
                    birthday_this_year += timedelta(
                        days=(7 - birthday_this_year.weekday())
                    )

                birthdays.append(
                    {
                        "name": user_data.name.value,
                        "congratulation_date": birthday_this_year.strftime(DATE_FORMAT),
                    }
                )

        return birthdays


# Опис задачі:
# Розробіть систему для управління адресною книгою.

if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")

    print("\nПісля видалення Jane:")
    for name, record in book.data.items():
        print(record)

    # --- Додаткові тести: 10 користувачів ---
    # 8 з днями народження (3 на наступному тижні, 5 поза), 2 без дати
    today = datetime.today().date()

    def format_date(days_offset):
        return (today + timedelta(days=days_offset)).strftime(DATE_FORMAT)

    # Створюємо 10 записів
    test_data = [
        ("User1", format_date(2)),  # наступний тиждень
        ("User2", format_date(4)),  # наступний тиждень
        ("User3", None),  # без дня народження
        ("User4", format_date(10)),  # поза тижнем
        ("User5", format_date(-5)),  # минулий
        ("User6", format_date(20)),  # поза тижнем
        ("User7", None),  # без дня народження
        ("User8", format_date(30)),  # поза тижнем
        # Знайдемо вихідний день в межах 1-6 днів для перевірки переносу на понеділок
        (
            "User9",
            format_date(
                next(
                    (
                        d
                        for d in range(1, 7)
                        if (today + timedelta(days=d)).weekday() in (5, 6)
                    ),
                    6,
                )
            ),
        ),
        ("User10", format_date(100)),  # поза тижнем
    ]

    for name, bday in test_data:
        rec = Record(name)
        if bday:
            rec.add_birthday(bday)
        book.add_record(rec)

    # Викликаємо get_upcoming_birthdays
    upcoming = book.get_upcoming_birthdays()

    print("\n=== Тестування get_upcoming_birthdays ===")
    print(f"Знайдено {len(upcoming)} днів народження на наступному тижні:")
    for item in upcoming:
        print(f"  - {item['name']}: {item['congratulation_date']}")

    # Перевірка: має бути рівно 3 з доданих тестових записів
    test_names = {name for name, _ in test_data}
    upcoming_test_names = [u["name"] for u in upcoming if u["name"] in test_names]

    assert len(upcoming_test_names) == 3, (
        f"Очікувалось 3 записи на наступному тижні, отримано {len(upcoming_test_names)}: {upcoming_test_names}"
    )

    # Перевірка переносу з вихідного на понеділок
    for item in upcoming:
        cong_date = datetime.strptime(item["congratulation_date"], DATE_FORMAT).date()
        # Дата привітання не може бути на вихідних
        assert cong_date.weekday() not in (5, 6), (
            f"{item['name']}: дата привітання {item['congratulation_date']} припадає на вихідний!"
        )

    print("\n✓ Всі тести пройдено успішно!")
