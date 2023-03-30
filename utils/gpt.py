import os
import subprocess
import re


class ChatGPT:
    def __init__(self, ask_text: str, api_key: str) -> None:
        self.__ask_text = ask_text
        self.__api_key = api_key
        self.__set_env_api_key(self.__api_key)

    def __set_env_api_key(self, key: str) -> None:
        os.environ["OPENAI_API_KEY"] = key

    @property
    def answer(self) -> str:
        result = subprocess.Popen(
            f"./sgpt.bin '{self.__ask_text}'",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="UTF-8",
        )
        output, error = result.communicate()
        return self.replace_non_ascii(output)

    def replace_non_ascii(self, text: str) -> str:
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return ansi_escape.sub("", text)
