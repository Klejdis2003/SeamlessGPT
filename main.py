import time

from cliboard_tracker import get_clipboard, copy_to_clipboard
from gpt import Nemotron


def main():
    gpt = Nemotron()
    value = get_clipboard()
    response = gpt.send_single_prompt(value)
    print(f'Response to "{value}":\n {response}')
    copy_to_clipboard(response)
    print('Response copied to clipboard')


if __name__ == '__main__':
    main()

