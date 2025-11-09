from datetime import datetime, timedelta

from home_work_2 import (
    DATE_FORMAT,
    AddressBook,
    add_birthday,
    add_contact,
    birthdays,
    change_contact,
    main,
    show_all,
    show_birthday,
    show_phone,
)


def run_tests():
    """Запуск всіх тестів для бота"""
    print("=== Running tests ===\n")

    book = AddressBook()

    # Тест 1: Додавання контактів
    print("Test 1: Adding contacts")
    print(add_contact(["John", "1234567890"], book))
    print(add_contact(["Jane", "9876543210"], book))
    print(add_contact(["John", "5555555555"], book))  # Додаємо другий телефон
    assert len(book.data) == 2
    assert len(book.find("John").phones) == 2
    print("✓ Test 1 passed\n")

    # Тест 2: Зміна телефону
    print("Test 2: Changing phone")
    print(change_contact(["John", "1234567890", "1112223333"], book))
    assert book.find("John").find_phone("1112223333") is not None
    print("✓ Test 2 passed\n")

    # Тест 3: Показ телефону
    print("Test 3: Show phone")
    print(show_phone(["John"], book))
    print("✓ Test 3 passed\n")

    # Тест 4: Показ всіх контактів
    print("Test 4: Show all contacts")
    print(show_all(book))
    print("✓ Test 4 passed\n")

    # Тест 5: Додавання днів народження
    print("Test 5: Adding birthdays")
    today = datetime.today().date()

    def format_date(days_offset):
        return (today + timedelta(days=days_offset)).strftime(DATE_FORMAT)

    print(add_birthday(["John", format_date(2)], book))
    print(add_birthday(["Jane", format_date(4)], book))

    # Додаємо більше тестових контактів
    test_data = [
        ("Alice", "1111111111", format_date(1)),  # наступний тиждень
        ("Bob", "2222222222", None),  # без дня народження
        ("Charlie", "3333333333", format_date(10)),  # поза тижнем
        ("David", "4444444444", format_date(-5)),  # минулий
        ("Eve", "5555555556", format_date(20)),  # поза тижнем
        ("Frank", "6666666666", None),  # без дня народження
        ("Grace", "7777777777", format_date(30)),  # поза тижнем
        (
            "Henry",
            "8888888888",
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
        ),  # вихідний день
        ("Ivy", "9999999999", format_date(100)),  # поза тижнем
    ]

    for name, phone, bday in test_data:
        add_contact([name, phone], book)
        if bday:
            add_birthday([name, bday], book)

    assert len(book.data) == 11  # 2 початкових + 9 нових
    print("✓ Test 5 passed\n")

    # Тест 6: Показ дня народження
    print("Test 6: Show birthday")
    print(show_birthday(["John"], book))
    print(show_birthday(["Bob"], book))  # Без дня народження
    print("✓ Test 6 passed\n")

    # Тест 7: Найближчі дні народження
    print("Test 7: Upcoming birthdays")
    print(birthdays([], book))
    upcoming = book.get_upcoming_birthdays()

    # Має бути 4 днів народження на наступному тижні (John, Jane, Alice, Henry)
    assert len(upcoming) >= 3, (
        f"Expected at least 3 upcoming birthdays, got {len(upcoming)}"
    )

    # Перевірка переносу з вихідного на понеділок
    for item in upcoming:
        cong_date = datetime.strptime(item["congratulation_date"], DATE_FORMAT).date()
        assert cong_date.weekday() not in (5, 6), (
            f"{item['name']}: congratulation date {item['congratulation_date']} falls on weekend!"
        )
    print("✓ Test 7 passed\n")

    # Тест 8: Обробка помилок
    print("Test 8: Error handling")
    print(add_contact(["Test"], book))  # Недостатньо аргументів
    print(
        change_contact(["NonExistent", "1111111111", "2222222222"], book)
    )  # Контакт не існує
    print(add_birthday(["John", "invalid-date"], book))  # Неправильний формат дати
    print(add_contact(["ErrorTest", "123"], book))  # Неправильний формат телефону
    print("✓ Test 8 passed\n")

    # Тест 9: Видалення контакту
    print("Test 9: Delete contact")
    book.delete("Jane")
    assert book.find("Jane") is None
    assert len(book.data) == 10
    print("✓ Test 9 passed\n")

    # Тест 10: Порожня адресна книга
    print("Test 10: Empty address book")
    empty_book = AddressBook()
    print(show_all(empty_book))
    print(birthdays([], empty_book))
    print("✓ Test 10 passed\n")

    print("=== All tests passed! ===\n")


if __name__ == "__main__":
    run_tests()

    # Запуск основної програми
    main()
