import os
import re
import openai
import functools

# import subprocess


class ChatGPT:
    def __init__(self, api_key: str) -> None:
        self.__api_key = api_key
        self.__model = "gpt-3.5-turbo"
        self.__set_env_api_key(self.__api_key)

    def __set_env_api_key(self, key: str) -> None:
        os.environ["OPENAI_API_KEY"] = key

    def answer(self, ask_text: str) -> str:
        openai.api_key = self.__api_key
        output = self.__answer_cache(self.__model, ask_text)
        return self.replace_non_ascii(output)

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def __answer_cache(model: str, ask_text: str) -> str:
        data_openai = [{"role": "user", "content": ask_text}]
        response = openai.ChatCompletion.create(model=model, messages=data_openai)
        return response.choices[0].message.content

    def replace_non_ascii(self, text: str) -> str:
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return ansi_escape.sub("", text)

    # @property
    # def answer(self) -> str:
    #     result = subprocess.Popen(
    #         f"./sgpt.bin '{self.__ask_text}'",
    #         shell=True,
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.PIPE,
    #         encoding="UTF-8",
    #     )
    #     output, error = result.communicate()
    #     return self.replace_non_ascii(output)
