import time

from pyperclip import set_clipboard

from cliboard_tracker import get_clipboard, copy_to_clipboard
from gpt import Gpt35


def main():
    gpt = Gpt35()
    value = get_clipboard()
    response = gpt.send_single_prompt(value)
    print(f'Response to "{value}":\n {response}')
    copy_to_clipboard(response)
    print('Response copied to clipboard')
    start = time.time()


if __name__ == '__main__':
    main()
