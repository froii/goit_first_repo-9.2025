
"    +38(050)123-32-34"
"     0503451234"
"(050)8889900"
"38050-111-22-22"
"38050 111 22 11   "


import re 

UKRAINIAN_CODE = "+38"

def normalize_phone(phone_number: str) -> str:
    try:
        if not isinstance(phone_number, str):
            return 'phone_number must be a string'
        
        only_numbers = re.sub(r'[^0-9]', '', phone_number)

        if phone_number.startswith('+00') or only_numbers.startswith('00'):
            return only_numbers
        
        elif phone_number.startswith('+') or only_numbers.startswith('38'):
            return '+' + only_numbers

        return UKRAINIAN_CODE + only_numbers

    except Exception:
        return "Please, use correct phone number"


raw_numbers = [
    "067\t123 4567",
    "(095) 234-5678\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050 111 22 11   ",
    "+1 (202) 555-0173",         # USA
    "+44 20 7946 0958",          # UK
    "+49-89-636-48018",          # Germany
    "0033 1 42 68 53 00",        # France (with 00 prefix)
    "+81 3-1234-5678",           # Japan
    "0039 06 6982",              # Italy (with 00 prefix)
    "+91-9876543210",            # India
    "+61 2 9876 5432",           # Australia
    "+34 912 34 56 78",          # Spain
    "0032 2 702 92 00",          # Belgium (with 00 prefix)   - не буде працювати нормально .
]

# номери дуже різні, довжина можу бути від 11 до 15 цифр, в деяких країнах пишуть без + а з 00 
# не можна бути впевненим що я оброблю всі номери правильно без написання пакета, такого як phonenumbers . 
# тепер туди можна вписати будь які цифри і кількість не перевіриш === багато винятків які не охоплює функція. 

sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)
