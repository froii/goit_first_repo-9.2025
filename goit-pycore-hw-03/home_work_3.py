
"    +38(050)123-32-34"
"     0503451234"
"(050)8889900"
"38050-111-22-22"
"38050 111 22 11   "


import re 

UKRAINIAN_CODE = "38"

def normalize_phone(phone_number: str) -> str:
    try:
        if not isinstance(phone_number, str):
            return 'phone_number must be a string'
        
        only_numbers = re.sub(r'[^0-9]', '', phone_number)
        
        return f"+{'' if phone_number[0] == '+' else UKRAINIAN_CODE}{only_numbers}"
               
    except Exception:
        return "Please, use correct phone number"




raw_numbers = [
    "067\\t123 4567",
    "(095) 234-5678\\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
]

sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)

# PS: якщо писати щопопало то і знак + може бути де попало .
