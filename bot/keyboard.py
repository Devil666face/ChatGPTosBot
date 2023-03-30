from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

main_buttons = {
    "ask": "Спросить 🤖",
}


class Keyboard:
    def __init__(self):
        self.main = self.make_main_buttons()

    def make_main_buttons(self):
        _keyboard_main = ReplyKeyboardMarkup(resize_keyboard=True)
        for button_label in main_buttons.values():
            _keyboard_main.add(button_label)
        return _keyboard_main

    @property
    def translate(self):
        inline_keyboard = InlineKeyboardMarkup(row_width=2)
        true_button = InlineKeyboardButton(text="Да", callback_data=f"translate_1")
        false_button = InlineKeyboardButton(text="Нет", callback_data=f"translate_0")
        inline_keyboard.row(true_button, false_button)
        return inline_keyboard


kb = Keyboard()
