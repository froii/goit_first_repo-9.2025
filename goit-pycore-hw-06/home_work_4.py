# from datetime import datetime, timedelta  

# DATE_FORMAT = '%Y.%m.%d'

# def get_upcoming_birthdays(users: list[dict[str, str]]) -> list[dict[str, str]]:
#     today = datetime.today().date()
#     birthdays = []

#     for user in users:
#         birthday = datetime.strptime(user["birthday"], DATE_FORMAT).date()
#         birthday_this_year = birthday.replace(year=today.year)
        
#         if birthday_this_year < today:
#             birthday_this_year = birthday_this_year.replace(year=today.year + 1)

#         if birthday_this_year >= today and birthday_this_year < today + timedelta(days=7):
#             if birthday_this_year.weekday() in (5, 6):
#                 birthday_this_year += timedelta(days=(7 - birthday_this_year.weekday()))

#             birthdays.append({
#                 "name": user["name"],
#                 "congratulation_date": birthday_this_year.strftime(DATE_FORMAT)
#             })

#     return birthdays
    

# users = [
#     {"name": "John Doe", "birthday": "1985.01.23"},
#     {"name": "Jane Smith", "birthday": "1990.01.27"},
#     {"name": "Олег Коваль", "birthday": "1988.10.13"},        # понеділок
#     {"name": "Ірина Шевченко", "birthday": "1992.10.15"},     # середа
#     {"name": "Марія Іванова", "birthday": "1995.10.17"},      # п'ятниця
#     {"name": "Петро Сидоренко", "birthday": "1983.10.18"},    # субота - переноситься на понеділок )( +2 дні ) {'name': 'Петро Сидоренко', 'congratulation_date': '2025.10.20'}
#     {"name": "Анна Коваленко", "birthday": "1991.09.30"},
#     {"name": "Сергій Бондар", "birthday": "1987.11.18"}
# ]

# upcoming_birthdays = get_upcoming_birthdays(users)
# print("Список привітань на цьому тижні:", upcoming_birthdays) 





# Завдання 2

# Для реалізації нового функціоналу також додайте функції обробники з наступними командами:

# add-birthday - додаємо до контакту день народження в форматі DD.MM.YYYY
# show-birthday - показуємо день народження контакту
# birthdays - повертає список користувачів, яких потрібно привітати по днях на наступному тижні
# @input_error
# def add_birthday(args, book):
#     # реалізація

# @input_error
# def show_birthday(args, book):
#     # реалізація

# @input_error
# def birthdays(args, book):
#     # реалізація



# Тож в фіналі наш бот повинен підтримувати наступний список команд:

# add [ім'я] [телефон]: Додати або новий контакт з іменем та телефонним номером, або телефонний номер к контакту який вже існує.
# change [ім'я] [старий телефон] [новий телефон]: Змінити телефонний номер для вказаного контакту.
# phone [ім'я]: Показати телефонні номери для вказаного контакту.
# all: Показати всі контакти в адресній книзі.
# add-birthday [ім'я] [дата народження]: Додати дату народження для вказаного контакту.
# show-birthday [ім'я]: Показати дату народження для вказаного контакту.
# birthdays: Показати дні народження, які відбудуться протягом наступного тижня.
# hello: Отримати вітання від бота.
# close або exit: Закрити програму.


# def main():
#     book = AddressBook()
#     print("Welcome to the assistant bot!")
#     while True:
#         user_input = input("Enter a command: ")
#         command, *args = parse_input(user_input)

#         if command in ["close", "exit"]:
#             print("Good bye!")
#             break

#         elif command == "hello":
#             print("How can I help you?")

#         elif command == "add":
#             # реалізація

#         elif command == "change":
#             # реалізація

#         elif command == "phone":
#             # реалізація

#         elif command == "all":
#             # реалізація

#         elif command == "add-birthday":
#             # реалізація

#         elif command == "show-birthday":
#             # реалізація

#         elif command == "birthdays":
#             # реалізація

#         else:
#             print("Invalid command.")



# Для прикладу розглянемо реалізацію команди add [ім'я] [телефон]. В функції main ми повинні додати обробку цієї команди, в відповідне місце:

#          elif command == "add":
#             print(add_contact(args, book))



# Сама реалізація функції add_contact може виглядати наступним чином:

# @input_error
# def add_contact(args, book: AddressBook):
#     name, phone, *_ = args
#     record = book.find(name)
#     message = "Contact updated."
#     if record is None:
#         record = Record(name)
#         book.add_record(record)
#         message = "Contact added."
#     if phone:
#         record.add_phone(phone)
#     return message



# Наша функція add_contact має два призначення - додавання нового контакту або оновлення телефону для контакту, що вже існує в адресній книзі.

# Параметри функції це список аргументів args та сама адресна книга book.

# Спочатку функція розпаковує список args, отримуючи ім'я name і телефон phone з перших двох елементів списку. Решта аргументів ігнорується завдяки використанню *_. Далі метод find об'єкта book виконує пошук запису з іменем name. Якщо запис з таким іменем існує, метод повертає цей запис, інакше повертається None.
# Якщо запис не знайдено, то це новий контакт і функція створює новий об'єкт Record з іменем name і додає його до book викликом методу add_record. Після додавання нового запису змінній message присвоюється повідомлення "Contact added." успішності операції.
# Далі незалежно від того, чи був запис знайдений або створений новий, до цього запису додається телефонний номер за допомогою методу add_phone, якщо він був наданий. На завершення функція повертає повідомлення про результат своєї роботи: "Contact updated.", якщо контакт був оновлений, або "Contact added.", якщо контакт був доданий. Для перехоплення помилок вводу та виведення відповідного повідомлення про помилку використовуємо декоратор @input_error.


# Критерії оцінювання:

# 1. Реалізувати всі вказані команди до бота

# 2. Всі дані повинні виводитися у зрозумілому та зручному для користувача форматі

# 3. Всі помилки, такі як неправильний ввід чи відсутність контакту, повинні оброблятися інформативно з відповідним повідомленням для користувача

# 4. Валідація даних:

# Дата народження має бути у форматі DD.MM.YYYY.
# Телефонний номер має складатися з 10 цифр.
# 5. Програма повинна закриватися коректно після виконання команд close або exit