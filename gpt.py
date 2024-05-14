from os import getenv

from dotenv import load_dotenv
from openai import AzureOpenAI
from openai.types.chat import ChatCompletion

load_dotenv()


class _GptClient:
    def __init__(self):
        self._client = AzureOpenAI(
            azure_endpoint=getenv("AZURE_OPENAI_API_ENDPOINT"),
            api_key=getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-01"
        )
        self.completions = self._client.chat.completions


class Gpt35:
    def __init__(self, client=_GptClient()):
        self.client = client
        self._model = "ChatGPT35"

    def _send_chat(self, chat: list, full_response=False) -> ChatCompletion | str:
        """
        Send a chat to the GPT-3.5 model. Must be in the format:
        [
        {
        "role": "system" or "user" or "assistant",
        "content": "string"
        }
        ]
        Start with system, to set up the assistant in the right context.
        :param chat: list of dictionaries
        :param full_response: flag to return the full response or just the message content
        :return: response from the GPT-3.5 model
        """
        response = self.client.completions.create(
            model=self._model,
            messages=chat
        )
        return response if full_response else response.choices[0].message.content

    def send_single_prompt(self, prompt: str, full_response=False):
        return self._send_chat(
            [
                {
                    "role": "user",
                    "content": prompt
                }],
            full_response=full_response)

    def get_data_list_analysis(self, data: list, full_response=False) -> ChatCompletion | str:
        """
        Send a list of numbers to the GPT-3.5 model to analyze and extract meaning out of.
        It will return structured JSON, which includes things such as the mean, median, mode, etc.
        :param data: a list
        :param full_response: flag to return the full ChatCompletion object or just the message content
        :return: response from the GPT-3.5 model
        """
        return self._send_chat(
            [
                {
                    "role": "system",
                    "content": "You are an assistant that can analyze data. Every metric that you analyze and extract "
                               "meaning out of should be structured in a json format and you only return structured "
                               "data and no human-like sentences. Users will give you lists of numbers and can also "
                               "generate custom prompts, but the initial instructions stay."
                },
                {
                    "role": "user",
                    "content": f'{data}. '
                }
            ],
            full_response=full_response
        )

    def extract_valuable_info_from_text(self, text: str, full_response=False):
        return self._send_chat(
            [
                {
                    "role": "system",
                    "content": "You are an assistant that can extract valuable information from text. You only return "
                               "structured data and no human-like sentences. Users will give you text and can also "
                               "generate custom prompts, but the initial instructions stay."
                               "Valuable information includes names, addresses, emails, phone numbers, dates, etc."
                               "You can also extract any other information that you think is valuable. ONLY "
                               "structured data in JSON format, no text."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            full_response=full_response
        )

    def get_suggestions(self, prompt:str, full_response=False):
        return self._send_chat(
            [
                {
                    "role": "system",
                    "content": "You are an assistant that can generate suggestions based on a prompt. You only return "
                               "structured data and no human-like sentences. Users will give you prompts and can also "
                               "generate custom prompts, but the initial instructions stay."
                               "Suggestions should be structured in a json format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            full_response=full_response
        )



