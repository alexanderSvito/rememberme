import difflib

import config


def get_correction(wrong, right):
    diff = difflib.ndiff(wrong.lower(), right.lower())

    res = ''
    incorrect = 0
    correct = 0
    for letter in diff:
        if letter.startswith('-'):
            res += letter[-1] + '\u0336'
            incorrect += 1
        elif letter.startswith('+'):
            res += letter[-1] + '\u0332'
            incorrect += 1
        else:
            res += letter[-1]
            correct += 1

    if incorrect >= config.ERROR_THRESHOLD * len(wrong):
        res = right

    return res, correct, incorrect
