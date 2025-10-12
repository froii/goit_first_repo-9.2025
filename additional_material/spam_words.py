import re
'''
Написати код, який буде аналізувати текст та прибирати в ньому спам слова

Python, Guido van Rossum 

Python is the best programming language!
* is the best programming language!
'''

SPAM_WORDS_LIST = ["Python", "Guido van Rossum"]

def remove_spam_words(message: str) -> str:
    def set_len_stars(match: re.Match) -> str:
        return '*' * len(match.group(0))
    for spam_word in SPAM_WORDS_LIST:
        message = re.sub(rf"\b{spam_word}\b", set_len_stars, message)
    return message




assert remove_spam_words("Guido van Rossum") == '****************' # довжина слова len('Guido van Rossum') = 16
assert remove_spam_words("Python") == '******' # '******' # довжина слова len('Python') = 6
assert remove_spam_words("Guido van Rossum Python") == '**************** ******' # '**************** ******' # довжина слова len('Guido van Rossum') = 16, len('Python') = 6

print(remove_spam_words("Guido van Rossum began working on Python "
"in the late 1980s as a successor to the ABC programming language "
"and first released it in 1991 as Python 0.9.0."))