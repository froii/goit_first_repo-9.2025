
from typing import Callable, Iterator
import re

# (?:^| ) - початок рядка або пробіл
# (?= |$) - пробіл або кінець рядка
# (?:...) групує і зберігає пам'ять без створення окремої групи в match.groups().
# (\d+(?:\.\d{1,2})?) - захоплює ціле число яке можливо має десяткове число з 1 чи 2 знаками після коми.
def generator_numbers(text: str) -> Iterator[float]:
    pattern = r'(?:^| )(\d+(?:\.\d{1,2})?)(?= |$)'
    for match in re.finditer(pattern, text):
        yield float(match.group())

def sum_profit(text: str, func: Callable) -> float:
    return sum(func(text))

# якщо без методів, а через цикл:
# def sum_profit(text: str, func: Callable) -> float:
#     total = 0.00
#     for number in func(text):
#         total += number
#     return total

# Критерії оцінювання:
# Правильність визначення та повернення дійсних чисел функцією generator_numbers.
# Коректність обчислення загальної суми в sum_profit.
# Чистота коду, наявність коментарів та відповідність стилю кодування PEP8.

text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")

# Загальний дохід: 1351.46