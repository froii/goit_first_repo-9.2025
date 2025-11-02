import random


def get_numbers_ticket(min: int, max: int, quantity: int) -> list[int] | str:
    try:
        if min < 1 or min >= max or max > 1000 or quantity < 1 or quantity > (max - min): 
            return []
         
        numbers = range(min, max)
        win_numbers = random.sample(numbers, quantity)
        return sorted(win_numbers)
             
  
    except TypeError:
        return "Please, use number type"
 

print(get_numbers_ticket(44, 111, 4))
print(get_numbers_ticket(44, 5555, 14))
print(get_numbers_ticket(0, 111, 4))
print(get_numbers_ticket(44, 555, 0))
print(get_numbers_ticket(44, 555, 10))
print(get_numbers_ticket(10, 15, 5))