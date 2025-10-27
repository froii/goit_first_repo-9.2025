# 12. Дан текст. Виведіть усі слова, що зустрічаються в тексті, по одному на кожен рядок.
# Слова мають бути відсортовані за зменшенням їхньої кількості появи в тексті,
# а при однаковій частоті появи — у лексикографічному порядку.

# Вказівка. Після того, як ви створите словник всіх слів, вам захочеться відсортувати його за частотою слова.
# Бажаного можна домогтися, якщо створити список, елементами якого будуть кортежі з двох елементів: частота слова і саме слово.
# Наприклад, [(2, 'hi'), (1, 'what'), (3, 'is')].
# Тоді стандартне сортування сортуватиме список кортежів, при цьому кортежі порівнюються за першим елементом,
# а якщо вони рівні — то за другим. Це майже те, що потрібно завдання.

from collections import defaultdict, Counter
import re

my_fav_words = """That thou hast her it is not all my grief,
    And yet it may be said I loved her dearly,
    That she hath thee is of my wailing chief,
    A loss in love that touches me more nearly.
    Loving offenders thus I will excuse ye,
    Thou dost love her, because thou know'st I love her,
    And for my sake even so doth she abuse me,
    Suff'ring my friend for my sake to approve her.
    If I lose thee, my loss is my love's gain,
    And losing her, my friend hath found that loss,
    Both find each other, and I lose both twain,
    And both for my sake lay on me this cross,
    But here's the joy, my friend and I are one,
    Sweet flattery, then she loves but me alone.""".lower().split()

grouped_words = defaultdict(Counter)

for word in my_fav_words:
    grouped_words[word[0]][word] += 1  # додаємо 1 до підрахунку

print(grouped_words)
# красивий вивід:
# for letter in sorted(grouped_words.keys()):
#     print(f"\n{letter.upper()}:")
#     for word, count in sorted(grouped_words[letter].items()):
#         print(f"  {word:<15} {count}")


text = """That thou hast her it is not all my grief,
And yet it may be said I loved her dearly,
That she hath thee is of my wailing chief,
A loss in love that touches me more nearly.
Loving offenders thus I will excuse ye,
Thou dost love her, because thou know'st I love her,
And for my sake even so doth she abuse me,
Suff'ring my friend for my sake to approve her.
If I lose thee, my loss is my love's gain,
And losing her, my friend hath found that loss,
Both find each other, and I lose both twain,
And both for my sake lay on me this cross,
But here's the joy, my friend and I are one,
Sweet flattery, then she loves but me alone"""

words = re.findall(r"\b[\w\']+\b", text.lower())

counter = Counter(words)

result = defaultdict(list)
for word, count in counter.items():
    result[count].append(word)

print(sorted(result.items(), reverse=True))
