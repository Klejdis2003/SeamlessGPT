import time

from cliboard_tracker import get_clipboard, copy_to_clipboard
from gpt import Gpt4O


def main():
    gpt = Gpt4O()
    value = get_clipboard()
    response = gpt.send_single_prompt(value)
    print(f'Response to "{value}":\n {response}')
    copy_to_clipboard(response)
    print('Response copied to clipboard')
    start = time.time()


if __name__ == '__main__':
    main()
