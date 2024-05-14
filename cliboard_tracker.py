from pyperclip import copy, paste


def get_clipboard():
    return paste()


def copy_to_clipboard(text):
    copy(text)
