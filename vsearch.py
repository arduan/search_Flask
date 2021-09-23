# Испльзование множеств в нахождении   гласных букв в слове


def search_vowels(phrase: str, letters: str = 'aeiou') -> set:
    """Возвращает множество букв из 'letters' е в указанной фразе"""
    return set(letters).intersection(set(phrase))

