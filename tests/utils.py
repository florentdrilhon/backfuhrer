import enum
import random
import string
from typing import Union, List, Set, Optional

ASCII_LOWER = list(string.ascii_lowercase)
ASCII_UPPER = list(string.ascii_uppercase)
ASCII_DIGITS = list(string.digits)
ASCII_PUNCTUATION = list(string.punctuation)


def one_of(lst: Union[List, Set, enum.EnumMeta], excluding: Optional[Union[List, Set]] = None):
    if excluding is not None:
        lst = set(lst) - set(excluding)
    if isinstance(lst, enum.EnumMeta) or isinstance(lst, set):
        return random.choice(list(lst))
    else:
        return random.choice(lst)


def list_of(generator, count: Optional[int] = None, max_count: Optional[int] = 3, min_count: Optional[int] = 1):
    if not count:
        count = random.randint(min_count, max(max_count, min_count + 1))
    if isinstance(generator, enum.EnumMeta):
        lst = list(generator)
        k = random_number(min_count, min(count, len(lst)))
        return random.sample(lst, k)
    else:
        return [generator() for _ in range(0, count)]


def random_number(a=1, b=2147483647) -> int:
    return random.randint(a, b)


def boolean():
    return bool(random.randint(0, 1))


def random_string(min=15, max=30):
    return ''.join(random.choices(ASCII_LOWER + ASCII_UPPER + ASCII_DIGITS + list('.-_'), k=random.randint(min, max)))
