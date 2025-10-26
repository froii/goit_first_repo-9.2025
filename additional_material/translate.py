# ========== 1. БАЗОВІ ПРИКЛАДИ ==========

def basic_examples():
    # Проста заміна
    table = str.maketrans('aeiou', '12345')
    text = "Hello World"
    print(f"Оригінал: {text}")
    print(f"Заміна голосних: {text.translate(table)}")
    
    # Видалення символів
    table = str.maketrans('', '', 'aeiou')
    print(f"Видалення голосних: {text.translate(table)}")
    
    # Перевірка регістру
    table = str.maketrans('a', 'X')
    test = "Aa"
    print(f"\n'{test}' → '{test.translate(table)}' (тільки нижній 'a' замінився)")
    print()


# ========== 2. ПРИКЛАД: HEX → BINARY ==========
def hex_to_binary():
    symbols = "0123456789ABCDEF"
    code = [
        '0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111',
        '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111'
    ]
    
    MAP = {}
    for s, c in zip(symbols, code):
        MAP[ord(s)] = c + ' '  # Додаємо пробіл для читабельності
        MAP[ord(s.lower())] = c + ' '
    
    hex_string = "34 DF 56 AC"
    result = hex_string.translate(MAP).strip()
    print(f"HEX: {hex_string}")
    print(f"BIN: {result}")
    print()


# ========== 3. ПРИКЛАД: АЗБУКА МОРЗЕ ==========
def text_to_morse():
    morse_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', ' ': '/'
    }
    
    # Створення таблиці перекладу
    table = {ord(k): v + ' ' for k, v in morse_dict.items()}
    
    text = "Hello World"
    result = text.upper().translate(table).strip()
    print(f"Текст: {text}")
    print(f"Морзе: {result}")
    print()


# ========== 4. РЕАЛЬНІ СЦЕНАРІЇ ==========

def practical_examples():
    """Практичні застосування"""
    print("=== ПРАКТИЧНІ ПРИКЛАДИ ===\n")
    
    # Очищення URL
    table = str.maketrans(' ', '-', '!@#$%^&*()')
    url_text = "My @Blog Post!"
    print(f"URL slug: '{url_text}' → '{url_text.translate(table)}'")
    
    # Видалення пунктуації
    import string
    table = str.maketrans('', '', string.punctuation)
    text = "Hello, world! How are you?"
    print(f"Без пунктуації: '{text.translate(table)}'")
    
    # Маскування карток
    table = str.maketrans('0123456789', 'X' * 10)
    card = "1234 5678 9012 3456"
    masked = card[:4] + card[4:14].translate(table) + card[14:]
    print(f"Картка: {card} → {masked}")
    
    # Емодзі-кодування
    table = {ord('!'): '💥', ord('?'): '❓', ord('.'): '⭐'}
    text = "Hello! How are you?"
    print(f"Емодзі: {text.translate(table)}")
    print()


# ========== 5. СЛОВНИК VS MAKETRANS ==========

def dict_vs_maketrans():
    """Різні способи створення таблиці"""
    print("=== СЛОВНИК VS MAKETRANS ===\n")
    
    # Метод 1: maketrans (простіше)
    table1 = str.maketrans('abc', 'XYZ')
    print(f"maketrans: 'abc' → {repr('abc'.translate(table1))}")
    
    # Метод 2: словник (гнучкіше)
    table2 = {ord('a'): 'XX', ord('b'): None, ord('c'): 'Z'}
    print(f"Словник: 'abc' → {repr('abc'.translate(table2))}")
    print("  (a→XX, b→видалено, c→Z)")
    print()


# ========== 6. ПОРІВНЯННЯ ПРОДУКТИВНОСТІ ==========

def performance_comparison():
    """Порівняння швидкості translate vs replace"""
    print("=== ПОРІВНЯННЯ ШВИДКОСТІ ===\n")
    import time
    
    text = "a" * 100000
    
    # replace (повільно)
    start = time.time()
    result = text
    for char in "aeiou":
        result = result.replace(char, "X")
    time_replace = time.time() - start
    
    # translate (швидко)
    start = time.time()
    table = str.maketrans("aeiou", "XXXXX")
    result = text.translate(table)
    time_translate = time.time() - start
    
    print(f"replace(): {time_replace:.5f} сек")
    print(f"translate(): {time_translate:.5f} сек")
    print(f"translate() швидший у {time_replace/time_translate:.1f} разів")
    print()


# ========== 7. ПІДВОДНІ КАМЕНІ ==========

def common_mistakes():
    """Типові помилки"""
    print("=== ТИПОВІ ПОМИЛКИ ===\n")
    
    # Помилка 1: Забули ord()
    try:
        table = {'a': 'X'}
        result = "abc".translate(table['a'])
        print(result)  # просто поверне 'abc' . помилок не буде
    except TypeError as e:  
        print(f"❌ Помилка без ord(): {e}")  # не буде помилки але і змін не буде
    
    # Правильно
    table = {ord('a'): 'X'}
    print(f"✅ З ord(): 'abc' → '{('abc'.translate(table))}'")
    
    # Помилка 2: None видаляє символ
    table = {ord('a'): None}
    print(f"\nNone видаляє: 'banana' → '{'banana'.translate(table)}'")
    print()


# ========== 8. ORD() І UNICODE ==========

def ord_examples():
    """Робота з ord() та Unicode"""
    print("=== ORD() ТА UNICODE ===\n")
    
    print(f"ord('A') = {ord('A')}")
    print(f"ord('a') = {ord('a')}")
    print(f"ord('Я') = {ord('Я')}")
    print(f"chr(65) = '{chr(65)}'")
    
    # Створення таблиці з Unicode
    table = {65: 'X', 97: 'y'}  # 65='A', 97='a'
    print(f"\n'AaBbCc'.translate(table) = '{'AaBbCc'.translate(table)}'")
    print()


# ========== ГОЛОВНА ФУНКЦІЯ ==========

def main():
    """Запуск всіх прикладів"""
    basic_examples()
    hex_to_binary()
    text_to_morse()
    practical_examples()
    dict_vs_maketrans()
    performance_comparison()
    common_mistakes()
    ord_examples()
    
    print("=== ПІДСУМОК ===")
    print("✅ translate() - для множинних замін")
    print("✅ maketrans() - для створення таблиці")
    print("✅ ord() - для Unicode-кодів")
    print("✅ Швидший у 3-5 разів за replace()")


if __name__ == "__main__":
    main()