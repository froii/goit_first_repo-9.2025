
from typing import Callable

def caching_fibonacci() -> tuple[Callable[[int], int], list[int]]:
    repeat = [0, 0] # [0]: total calls, [1]: new calculations
    cache = {}

    def fibonacci(n):
        repeat[0] += 1

        if n <= 1:
            return n

        if n in cache:
            return cache[n]
        
        repeat[1] += 1 

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci, repeat


# Вимоги до завдання:
# Функція caching_fibonacci() повинна повертати внутрішню функцію fibonacci(n).
# fibonacci(n) обчислює n-те число Фібоначчі. Якщо число вже знаходиться у кеші, функція має повертати значення з кешу.
# Якщо число не знаходиться у кеші, функція має обчислити його, зберегти у кеш та повернути результат.
# Використання рекурсії для обчислення чисел Фібоначчі.

# Опис:
# Функція caching_fibonacci створює внутрішню функцію fibonacci і словник cache для зберігання результатів обчислення чисел Фібоначчі. 
# Кожен раз, коли викликається fibonacci(n), спочатку перевіряється, чи вже збережено значення для n у cache. 
# Якщо значення є у кеші, воно повертається негайно, що значно зменшує кількість рекурсивних викликів. 
# Якщо значення відсутнє у кеші, воно обчислюється рекурсивно і зберігається у cache. 
# Функція caching_fibonacci повертає внутрішню функцію fibonacci, яка тепер може бути використана для обчислення чисел Фібоначчі з використанням кешування.

# Отримуємо функцію fibonacci
fib, repeat = caching_fibonacci()

# Використовуємо функцію fibonacci для обчислення чисел Фібоначчі
print(fib(10), repeat)  # Виведе 55
print(fib(15), repeat)  # Виведе 610
print(fib(65), repeat)  # Виведе 17167680177565
print(fib(15), repeat)  # Виведе 610
print(fib(105), repeat) # Виведе 3928413764606871165730
