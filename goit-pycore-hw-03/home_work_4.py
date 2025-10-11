
from datetime import datetime, timedelta  

DATE_FORMAT = '%Y-%m-%d'

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
    {"name": "John Doe", "birthday": "1985-10-11"},         
    {"name": "Jane Smith", "birthday": "1990-10-12"},       
    {"name": "Alice Johnson", "birthday": "1988-10-13"},    
    {"name": "Bob Williams", "birthday": "1992-09-14"},     
    {"name": "Charlie Brown", "birthday": "1987-09-15"},    
    {"name": "Diana Martinez", "birthday": "1995-09-16"},   
    {"name": "Edward Davis", "birthday": "1989-09-17"},     
    {"name": "Fiona Garcia", "birthday": "1991-09-18"},     
    {"name": "George Wilson", "birthday": "1986-09-05"},
    {"name": "Helen Clark", "birthday": "1993-10-14"},
    {"name": "Ivan Petrov", "birthday": "1984-10-15"},
    {"name": "Julia Roberts", "birthday": "1996-10-16"},
]


upcoming_birthdays = get_upcoming_birthdays(users)
print("Список привітань на цьому тижні:", upcoming_birthdays)

