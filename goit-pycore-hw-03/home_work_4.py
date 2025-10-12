from datetime import datetime, timedelta  

DATE_FORMAT = '%Y.%m.%d'

def get_upcoming_birthdays(users: list[dict[str, str]]) -> list[dict[str, str]]:
    today = datetime.today().date()
    birthdays = []

    for user in users:
        birthday = datetime.strptime(user["birthday"], DATE_FORMAT).date()
        birthday_this_year = birthday.replace(year=today.year)
        
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        if birthday_this_year >= today and birthday_this_year < today + timedelta(days=7):
            if birthday_this_year.weekday() in (5, 6):
                birthday_this_year += timedelta(days=(7 - birthday_this_year.weekday()))

            birthdays.append({
                "name": user["name"],
                "congratulation_date": birthday_this_year.strftime(DATE_FORMAT)
            })

    return birthdays
    

users = [
    {"name": "John Doe", "birthday": "1985.01.23"},
    {"name": "Jane Smith", "birthday": "1990.01.27"},
    {"name": "Олег Коваль", "birthday": "1988.10.13"},        # понеділок
    {"name": "Ірина Шевченко", "birthday": "1992.10.15"},     # середа
    {"name": "Марія Іванова", "birthday": "1995.10.17"},      # п'ятниця
    {"name": "Петро Сидоренко", "birthday": "1983.10.18"},    # субота - переноситься на понеділок )( +2 дні ) {'name': 'Петро Сидоренко', 'congratulation_date': '2025.10.20'}
    {"name": "Анна Коваленко", "birthday": "1991.09.30"},
    {"name": "Сергій Бондар", "birthday": "1987.11.18"}
]

upcoming_birthdays = get_upcoming_birthdays(users)
print("Список привітань на цьому тижні:", upcoming_birthdays) 