# import os
import yaml

# from typing import List

# from dotenv import load_dotenv


# load_dotenv()


class Config:
    def __init__(self, config_file_path="config.yaml"):
        self.config = self.__read_conf(config_file_path)
        self.__parse_section("OPENAI_API_KEY")
        self.__parse_section("BOT_TOKEN")
        self.__parse_section("ADMIN_ID")

    def __read_conf(self, file_path):
        with open(file_path, "r") as file:
            return yaml.safe_load(file)

    def __parse_section(self, section_name):
        setattr(self, section_name, self.config[section_name])
        return self.config[section_name]


# def load_env(env_name: str) -> str:
#     __env = os.getenv(env_name)
#     if not __env:
#         print(f"Not found {env_name} in .env file")
#         return
#     return __env


class RoundRobinApiKey:
    def __init__(self, key_list) -> None:
        self.__key_list = key_list
        self.__active_key = self.__key_list[0]

    @property
    def key(self) -> str:
        now_index = self.__key_list.index(self.__active_key)
        if now_index == len(self.__key_list) - 1:
            now_index = 0
        else:
            now_index += 1
        self.__active_key = self.__key_list[now_index]
        return self.__active_key


config = Config()
api_key = RoundRobinApiKey(config.OPENAI_API_KEY)

#     def load_key_list(self, max_index: int) -> List[str]:
#         key_list = list()
#         for index in range(1, max_index):
#             key = load_env(f"OPENAI_API_KEY_{index}")
#             if key is None:
#                 continue
#             key_list.append(key)
#         return key_list

# BOT_TOKEN = load_env("BOT_TOKEN")
# ADMIN_ID = load_env("ADMIN_ID")
