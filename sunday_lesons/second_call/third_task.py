# Власник взуттєвого магазину має певну кількість взуття.
# У нього є список, що містить розмір кожного взуття, яке він має в магазині.
# Є певна кількість клієнтів, які готові заплатити певну суму грошей, лише якщо вони отримають взуття потрібного їм розміру.
# Ваше завдання – обчислити, скільки грошей ви заробили.
# Формат вхідних даних
# Перший рядок містить список усіх розмірів взуття в магазині, розділений пробілами.
# другий рядок містить – кількість клієнтів.
# Наступні рядки містять значення , бажані клієнтом, та – ціну взуття, розділені пробілами.
# 2 3 4 5 6 8 7 6 5 18
# 6
# 6 55
# 6 45
# 6 55
# 4 40
# 18 60
# 10 50

from collections import Counter, defaultdict

# option 1
with open('data.txt', 'r', encoding='utf-8') as file:
    text = file.read()

lines = text.splitlines()

list_of_all_sizes = map(int, lines[0].split())

amount_of_clients = int(lines[1])

total_money = 0

counter = Counter(list_of_all_sizes)

for line in lines[2:]:
    size, price = map(int, line.split())
    if size in counter:
        counter[size] -= 1
        if counter[size] == 0:
            del counter[size]
        total_money += price
        print(size, price, total_money)

print(total_money)


# option 2
total = 0

with open("data.txt", "r") as f:
    sizes = f.readline().split()
    customer_count = int(f.readline())
    for i in range(customer_count):
        size, price_text = f.readline().split()
        if size in sizes:
            sizes.remove(size)
            total += int(price_text)

print(total)


# option 3
total = 0
bids = defaultdict(list) 

with open("data.txt", "r") as f:
    sizes = f.readline().split()
    customer_count = int(f.readline())
    for i in range(customer_count):
        size, price_text = f.readline().split()
        bids[size].append(int(price_text))


for size, size_bids in bids.items():
    for bid in sorted(size_bids, reverse=True):
        if size in sizes:
            sizes.remove(size)
            total += bid

print(total)
