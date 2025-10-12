import re
'''
1234 5432
123456 654321

'''

def validate_pincode(pincode_str: str) -> bool:
    return re.fullmatch(r'[0-9]{4}|[0-9]{6}', pincode_str) is not None
    # return re.match(r'[0-9]{4}|[0-9]{6}', pincode_str) != None

assert validate_pincode("1234") == True
assert validate_pincode("123456") == True
assert validate_pincode("a123") == False
assert validate_pincode("12345") == False

print(validate_pincode("1234"))
print(validate_pincode("123a456"))