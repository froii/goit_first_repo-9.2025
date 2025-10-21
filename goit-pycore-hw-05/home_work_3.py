
import sys

# can be run in correct folder - goit-pycore-hw-05
# python home_work_3.py ./logs/logs.log error
# python home_work_3.py ./logs/logs.log warning
# python home_work_3.py ./logs/logs.log info
# python home_work_3.py ./logs/logs.log debuggg

LOG_TYPES = ['INFO', 'ERROR', 'DEBUG', 'WARNING']

# Реалізуйте функцію parse_log_line(line: str) -> dict для парсингу рядків логу.
def parse_log_line(line: str) -> dict:
    date, time, type, message = line.split(" ", maxsplit=3)
    return { "date": date, "time": time, "type": type, "message": message }

# Реалізуйте функцію load_logs(file_path: str) -> list для завантаження логів з файлу.
def load_logs(file_path: str) -> list:
    logs = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for lineno, line in enumerate(file, 1):
            line = line.strip()
            if not line:
                continue
            try:
                logs.append(parse_log_line(line))
            except ValueError as e:
                raise ValueError(f"Invalid log format on line {lineno}")
    return logs

# Реалізуйте функцію filter_logs_by_level(logs: list, level: str) -> list для фільтрації логів за рівнем.
# def filter_logs_by_type(logs: list, type: str) -> list:
#     sorted_logs = filter(lambda log: log['type'] == type.upper(), logs)
#     return list(sorted_logs)
def filter_logs_by_type(logs: list, type: str) -> list:
    return [log for log in logs if log['type'] == type.upper()]


# Реалізуйте функцію count_logs_by_level(logs: list) -> dict для підрахунку записів за рівнем логування.
def count_logs_by_type(logs: list) -> dict:
    types_count = {}
    for log in logs:
        type = log['type']
        #  немає counts[type] || 0 навіть через or - викличе KeyError при спробі прочитати неіснуючий ключ до того, як спрацює оператор 'or' -
        #  так само як і в if, тому не працює спрощення перевірок типів і наявності даних ( потрібні явні перевірки if key in dict and dict[key]:)
        types_count[type] = types_count.get(type, 0) + 1
    return types_count

# створює header таблиці
def display_log_table_header():
    print(f"{'Рівень логування':<20} | {'Кількість':<10}")
    print("-" * 20 + "-|-" + "-" * 10)

# виводить таблицю з підрахунком логів по типах
def display_log_counts(counts: dict):
    display_log_table_header()

    for log_type in LOG_TYPES:
        count = counts.get(log_type, 0)
        print(f"{log_type:<20} | {count:<10}")

# виводить логи певного типу / рівня
def display_filtered_logs(logs: list, log_type: str):
    print(f"Logs details for level '{log_type.upper()}':")
    for log in logs:
        print(f"{log['date']} {log['time']} - {log['message'].strip()}")


if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            print("Please provide the path to the log file as a command-line argument.")
            sys.exit(1)
        
        path = sys.argv[1]
        logs = load_logs(path)
        counts = count_logs_by_type(logs)
        display_log_counts(counts)

        if len(sys.argv) >= 3:
            if sys.argv[2].upper() not in LOG_TYPES:
                print(f"Unknown log type: {sys.argv[2]}")
                sys.exit(1)
            log_type = sys.argv[2]
            filtered_logs = filter_logs_by_type(logs, log_type)
            display_filtered_logs(filtered_logs, log_type)

    except (FileNotFoundError, OSError):
        print(f"Wrong file path {path}")
        sys.exit(1)
    except (ValueError, PermissionError) as e:
        print(f"Error: {e}")
        sys.exit(1)


# Вимоги до завдання:
# Скрипт повинен приймати шлях до файлу логів як аргумент командного рядка.
# Скрипт повинен приймати не обов'язковий аргумент командного рядка, після аргументу шляху до файлу логів.
# Він відповідає за виведення всіх записів певного рівня логування. І приймає значення відповідно до рівня логування файлу. 
# Наприклад аргумент error виведе всі записи рівня ERROR з файлу логів.
# Скрипт має зчитувати і аналізувати лог-файл, підраховуючи кількість записів для кожного рівня логування (INFO, ERROR, DEBUG, WARNING).
# Результати мають бути представлені у вигляді таблиці з кількістю записів для кожного рівня. 

# Реалізуйте функцію parse_log_line(line: str) -> dict для парсингу рядків логу.
# Реалізуйте функцію load_logs(file_path: str) -> list для завантаження логів з файлу.
# Реалізуйте функцію filter_logs_by_level(logs: list, level: str) -> list для фільтрації логів за рівнем.
# Реалізуйте функцію count_logs_by_level(logs: list) -> dict для підрахунку записів за рівнем логування.
# Для цього реалізуйте функцію display_log_counts(counts: dict), яка форматує та виводить результати. Вона приймає результати виконання функції count_logs_by_level.

# Рівень логування | Кількість
# -----------------|----------
# INFO             | 4
# DEBUG            | 3
# ERROR            | 2
# WARNING          | 1

# Деталі логів для рівня 'ERROR':
# 2024-01-22 09:00:45 - Database connection failed.
# 2024-01-22 11:30:15 - Backup process failed.







# Критерії оцінювання:
# Скрипт виконує всі зазначені вимоги, правильно аналізуючи лог-файли та виводячи інформацію.
# Скрипт коректно обробляє помилки, такі як неправильний формат лог-файлу або відсутність файлу.
# При розробці обов'язково було використано один з елементів функціонального програмування: лямбда-функція, списковий вираз, функція filter, тощо.
# Код добре структурований, зрозумілий і містить коментарі там, де це необхідно.
