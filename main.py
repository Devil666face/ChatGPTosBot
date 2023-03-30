#!./venv/bin/python
from bot.bot import bot_polling
from models.models import init_models
from utils.env import Config

if __name__ == "__main__":
    config = Config()
    print(config.__dict__)
    init_models()
    bot_polling()
