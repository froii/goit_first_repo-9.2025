from datetime import date

def checkio(date1: date, date2: date) -> int:
    first_day = date1.weekday()
    period = (date2 - date1).days + 1
    
    weekends = period // 7 * 2 
    extra_days = period % 7

    extra_weekends = 0
    if extra_days > 0:
        if first_day <= 5 and first_day + extra_days > 5:
            extra_weekends += 1
        if first_day <= 6 and first_day + extra_days > 6:
            extra_weekends += 1
 
    return weekends + extra_weekends

# Передумова: start_date < end_date.
# #These "asserts" using only for self-checking and not necessary for auto-testing
# if __name__ == '__main__':
assert checkio(date(2013, 9, 18), date(2013, 9, 23)) == 2, "1st example"
assert checkio(date(2013, 1, 1), date(2013, 2, 1)) == 8, "2nd example"
assert checkio(date(2013, 2, 2), date(2013, 2, 3)) == 2, "3rd example"
# Нові тести:
assert checkio(date(2013, 9, 14), date(2013, 9, 15)) == 2  # Сб-Нд
assert checkio(date(2013, 9, 13), date(2013, 9, 15)) == 2  # Пт-Нд
assert checkio(date(2013, 9, 16), date(2013, 9, 20)) == 0  # Пн-Пт
assert checkio(date(2013, 1, 5), date(2013, 1, 6)) == 2    # Сб-Нд
assert checkio(date(2013, 1, 1), date(2013, 1, 1)) == 0    # 1 день (Вт)
assert checkio(date(2013, 1, 5), date(2013, 1, 5)) == 1    # 1 день (Сб)
assert checkio(date(2013, 1, 6), date(2013, 1, 6)) == 1    # 1 день (Нд)
assert checkio(date(2013, 1, 1), date(2013, 12, 31)) == 104 # Весь 2013
assert checkio(date(2013, 9, 1), date(2013, 9, 30)) == 9   # Весь вересень
assert checkio(date(2013, 2, 1), date(2013, 2, 28)) == 8   # Лютий

print(checkio(date(2013, 9, 18), date(2013, 9, 23)))
print(checkio(date(2013, 9, 4), date(2013, 9, 23)))

