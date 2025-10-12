print('Es')


from datetime import datetime
'''
Написати код, який буде рахувати вік людини
'''

keys = ['tee', 't']
keys.sort(key=len)
result_keys = sorted(keys, key=len)
print(result_keys)
print(keys)

def calculate_person_age(date_of_birth_str: str) -> int:
    date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d") # str parse time
    today = datetime.today()

    date_of_birth_this_year = date_of_birth.replace(year=today.year)
    # print(date_of_birth_this_year)
    age = today.year - date_of_birth.year
    
    if (date_of_birth_this_year > today):
        age -= 1 

    return age

def is_date_in_the_past(month_one: int, day_one: int, month_two: int, day_two: int) -> bool:
    return (month_one < month_two) or (month_one == month_two and day_one < day_two)
    # return (month_one < month_two) or (day_one < day_two)

def calculate_person_age_alternative(date_of_birth_str: str) -> int:
    date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d") # str parse time
    today = datetime.today()


    # 02-09 02-08 >
    # 02-07 02-08 <
    # 01-01 02-08 <
    # 01-01 01-01 =

    # print(date_of_birth_this_year)
    age = today.year - date_of_birth.year

    if (not is_date_in_the_past(date_of_birth.month, date_of_birth.day, today.month, today.day)):
        age -= 1

    return age


assert calculate_person_age("2000-01-01") == 25
assert calculate_person_age("2025-02-09") == 0
assert calculate_person_age("2024-02-07") == 1

assert calculate_person_age_alternative("2000-01-01") == 25
assert calculate_person_age_alternative("2025-02-09") == 0
assert calculate_person_age_alternative("2024-02-07") == 1
# if calculate_person_age("2000-01-01") != 30:
#     raise AssertionError

# print(calculate_person_age("2000-01-01")) # 25
# 2024-02-09
# print(calculate_person_age("2024-02-09")) # 0
# print(calculate_person_age("2024-02-07")) # 1

# 02-09 02-08 >
# 02-07 02-08 <
# 01-01 02-08 <
# 01-01 01-01 =
assert is_date_in_the_past(2, 9, 2, 8) == False
assert is_date_in_the_past(2, 7, 2, 8) == True
assert is_date_in_the_past(1, 1, 2, 8) == True
assert is_date_in_the_past(1, 1, 1, 1) == False

assert is_date_in_the_past(2, 10, 3, 9) == True