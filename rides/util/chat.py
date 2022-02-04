from re import sub
from typing import Tuple


def parse_yes_no(text: str) -> Tuple[bool, bool]:
    '''Returns best guess at yes/no and 100% confidence level'''
    text = sub('[^A-Za-z]+', ' ', text)
    words = set(text.lower().split())

    yes = 'yes' in words
    no = 'no' in words

    if (yes and no) or not (yes or no):
        # TODO: Write a parse that determines minimum distance
        return True, False
    elif yes:
        return True, True
    elif no:
        return False, True
    else:
        # TODO: Raise error as this should be unreachable
        return False, False


def parse_number(text: str) -> Tuple[int, bool]:
    '''Returns best guess at number and 100% confidence level'''
    text = sub('[^0-9A-Za-z]+', ' ', text)
    words = text.lower().split()
    numbers = [element for element in words if element.isdecimal()]

    if len(numbers) == 1:
        return int(numbers[0]), True
    else:
        return 0, False
