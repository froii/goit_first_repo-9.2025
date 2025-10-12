import re
'''
Написати код, який буде аналізувати текст та прибирати в ньому спам слова

Python, Guido van Rossum 

Python is the best programming language!
* is the best programming language!
'''

SPAM_WORDS_LIST = ["Python", "Guido van Rossum"]

def remove_spam_words(message: str) -> str:
    for spam_word in SPAM_WORDS_LIST:
        message = re.sub(rf"\b{spam_word}\b", "*", message)
    return message




assert remove_spam_words("Guido van Rossum") == '*'
assert remove_spam_words("Python") == '*' # '******'
assert remove_spam_words("Guido van Rossum Python") == '* *'

print(remove_spam_words("Guido van Rossum began working on Python "
"in the late 1980s as a successor to the ABC programming language "
"and first released it in 1991 as Python 0.9.0."))