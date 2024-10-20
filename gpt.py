from os import getenv
from typing import Iterable

from dotenv import load_dotenv
from openai import AzureOpenAI, OpenAI
from openai.types.chat import ChatCompletion

load_dotenv()


class _OpenAiClient:
    def __init__(self, config: dict[str, any]):
        try:
            self._client: OpenAI = config["client"]
            self._model: str = config["model"]

            config.pop("client")
            config.pop("model")

            self.config = config
            self.completions = self._client.chat.completions
            self.chat = []
        except KeyError:
            raise ValueError("Invalid configuration. The configuration must at least contain the keys: client, model")

    def _send_chat(self, chat: Iterable[dict[str, str]], full_response=False, save=False, with_previous_context=False) -> ChatCompletion | str:
        chat = chat if with_previous_context else self.chat + chat

        response = self.completions.create(
            model=self._model,
            messages=chat,
            **self.config
        )

        if save:
            self.chat += chat

        return response if full_response else response.choices[0].message.content

    def send_message(self, message: str, full_response=False, with_previous_chat_context = False, remember_response = False) -> ChatCompletion | str:
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

        if with_previous_chat_context:
            self.chat.append({"role": "user", "content": message})
            response = self.completions.create(
                model=self._model,
                messages=self.chat,
                **self.config
            )
        else:
            response = self.start_chat_as_user(message, full_response, remember_chat=remember_response)
        return response if full_response else response.choices[0].message.content

    def start_chat_as_user(self, prompt: str, full_response=False, remember_chat = False) -> str | ChatCompletion:
        chat = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        response =  self.completions.create(
            model=self._model,
            messages=chat,
            **self.config
        )

        if remember_chat:
            self.chat.append(chat[0])
            self.chat.append({"role": "assistant", "content": response})
        return response


    def send_single_prompt(self, prompt: str, full_response=False):
        return self.send_message(message=prompt, with_previous_chat_context=False, full_response=full_response, remember_response=False)

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

    def get_suggestions(self, prompt: str, full_response=False):
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

    def exam_help(self, prompt: str, full_response=False):
        return self._send_chat(
            [
                {
                    "role": "system",
                    "content": "You are an assistant that can help with exams. You respond to questions concisely and absolutely do not format the text. Also, if a question is of multiple choice form, you only return the correct alternative, that's it."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            full_response=full_response,
            save=True,
            with_previous_context=True
        )

    def modify_config(self, **kwargs):
        self.config.update(kwargs)

    def clear_chat(self):
        self.chat = []




class Nemotron(_OpenAiClient):
    def __init__(self):
        super().__init__({
            "client": OpenAI(base_url="https://integrate.api.nvidia.com/v1",
                             api_key=getenv("NEMOTRON_OPENAI_API_KEY")
                             ),
            "model": "nvidia/llama-3.1-nemotron-70b-instruct",
            "temperature": 0.5,
            "top_p": 1,
            "max_tokens": 1024
        }
    )
