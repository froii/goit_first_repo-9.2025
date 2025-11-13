"""AddressBook class for managing contacts."""
from collections import UserDict
from datetime import datetime, timedelta
from constants import DATE_FORMAT


class AddressBook(UserDict):
    """Class for managing a collection of contacts."""
    
    def add_record(self, record):
        """Add a record to the address book."""
        self.data[record.name.value] = record

    def find(self, name):
        """Find a record by name."""
        return self.data.get(name)

    def delete(self, name):
        """Delete a record by name."""
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self) -> list[dict[str, str]]:
        """Get birthdays occurring in the next 7 days."""
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
                    birthday_this_year += timedelta(days=(7 - birthday_this_year.weekday()))

                birthdays.append({
                    "name": user_data.name.value,
                    "congratulation_date": birthday_this_year.strftime(DATE_FORMAT),
                })

        return birthdays
