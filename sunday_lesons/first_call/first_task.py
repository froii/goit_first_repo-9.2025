from datetime import date

def checkio(date1: date, date2: date) -> int:
    first_day = date1.weekday()
    period = (date2 - date1).days + 1
    whole_time = first_day - (first_day - period)

    weekends = whole_time // 7 * 2 
    extra_days = whole_time % 7

    if first_day + extra_days > 6:
        extra_weekends = 2
    elif first_day + extra_days > 5:
        extra_weekends = 1
    else:
        extra_weekends = 0
 
    return weekends + extra_weekends

# Передумова: start_date < end_date.
# #These "asserts" using only for self-checking and not necessary for auto-testing
# if __name__ == '__main__':
assert checkio(date(2013, 9, 18), date(2013, 9, 23)) == 2, "1st example"
assert checkio(date(2013, 1, 1), date(2013, 2, 1)) == 8, "2nd example"
assert checkio(date(2013, 2, 2), date(2013, 2, 3)) == 2, "3rd example"

print(checkio(date(2013, 9, 18), date(2013, 9, 23)))
print(checkio(date(2013, 9, 4), date(2013, 9, 23)))

