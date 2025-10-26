# Як із рядка слов отримати словник де ключі та значення записані попарно.
# Наприклад: "Hello Hi Bye Goodbye List Array"
word = {"Hello": "Hi", 
        "Bye": "Goodbye", 
        "List": "Array"}

def parse_dict_to_string(data: dict) -> str:
    result = ""
    for key, value in data.items():
        result += f"{key} {value} "
    return result



def parse_string_to_dict(data: str) -> dict:
    words = data.split()
    result = {}
    for i, word in enumerate(words):
        if i % 2 == 0:
            result[word] = words[i + 1]
    return result


sent = "Hello Hi Bye Goodbye List Array".split(" ")
res = dict(zip(sent[::2], sent[1::2]))
input_ = "Hi"


# option 0
input_ = "Array"
if input_ in res:
    print(res[input_])
elif input_ in res.values():
    print(list(res.keys())[list(res.values()).index(input_)])
else:
    print("Not found")

# option 1
if input_ in res:
    print(res[input_])
elif input_ in res.values():
    print(list(res.keys())[list(res.values()).index(input_)])
else:
    print("Not found")

# option 2
res_op = dict(zip(res.values(), res.keys()))
if input_ in res:
    print(res[input_])
elif input_ in res_op:
    print(res_op[input_])
else:
    print('Not found')


def extend_dict(d):
    for key, value in list(d.items()):
        d[value] = key
    return d
sample_dict = {"Hello": "Hi", "Bye": "Goodbye", "List": "Array"}
extended_dict = extend_dict(sample_dict)
print(extended_dict)

words = "Hello Hi Bye Goodbye List Array ".split()
dict_r = {}
dict_r
for i in range(0, len(words), 2):
    dict_r[words[i]] = words[i + 1]
    dict_r[words[i + 1]] = words[i]
print(dict_r)

