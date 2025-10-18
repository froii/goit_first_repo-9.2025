from pathlib import Path


def total_salary(path: str) -> tuple[float, float]:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            total_salary = 0
            count = 0

            for line in file:
                try:
                    name, salary = line.strip().split(',')
                    total_salary += float(salary)
                    count += 1
                
                except ValueError:
                    print(f"Skipping invalid line: {line.strip()}")
                    continue

            if count == 0:
                return 0.00, 0.00
        
            average_salary = total_salary / count
            return round(total_salary, 2), round(average_salary, 2)
        
    except (FileNotFoundError, ValueError):
        print(f"File not found or invalid format: {path}")
        return 0.00, 0.00
    
    except OSError as e:
        print(f"Error opening/reading file {e}")
        return 0.00, 0.00  
  

# Критерії оцінювання:
# Функція повинна точно обчислювати загальну та середню суми.
# Повинна бути обробка випадків, коли файл відсутній або пошкоджений.
# Код має бути чистим, добре структурованим і зрозумілим.


salary_path = Path(__file__).resolve().parent / "path/to/salary_file.txt"
total, average = total_salary(str(salary_path))
print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")
# Загальна сума заробітної плати: 16300, Середня заробітна плата: 2037.5