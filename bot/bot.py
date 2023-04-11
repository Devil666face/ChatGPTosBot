from functools import wraps
from aiogram import types
from utils.env import (
    config,
    api_key,
)
from aiogram import (
    Bot,
    Dispatcher,
    executor,
)
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from models.models import (
    User,
)
from aiogram.dispatcher.filters.state import (
    State,
    StatesGroup,
)
from bot.messages import Messages as _
from bot.keyboard import (
    kb,
    main_buttons,
)
from googletrans import Translator
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from utils.gpt import ChatGPT
from aiogram.utils.exceptions import CantParseEntities


translator = Translator()

bot = Bot(
    token=config.BOT_TOKEN,
    parse_mode="HTML",
)
dp = Dispatcher(
    bot,
    storage=MemoryStorage(),
)


class Form(StatesGroup):
    ask_state = State()


async def answer(message: types.Message, message_text: str) -> None:
    await message.answer(
        message_text,
        reply_markup=kb.main,
    )


async def answer_translate(message: types.Message) -> None:
    await message.answer(
        _.TRANSLATE,
        reply_markup=kb.translate,
    )


async def answer_gpt(message: types.Message, message_text: str) -> None:
    try:
        await message.answer(
            message_text,
            reply_markup=kb.main,
            # parse_mode=types.ParseMode.MARKDOWN_V2,
            parse_mode=types.ParseMode.MARKDOWN,
        )
    except CantParseEntities:
        await message.answer(
            message_text,
            reply_markup=kb.main,
        )


async def answer_translated_gpt(
    call: types.CallbackQuery, message_en_text: str
) -> None:
    try:
        await bot.send_message(
            call.from_user.id,
            translate(message_en_text),
            reply_markup=kb.main,
            # parse_mode=types.ParseMode.MARKDOWN_V2,
            parse_mode=types.ParseMode.MARKDOWN,
        )
    except CantParseEntities:
        await bot.send_message(
            call.from_user.id,
            translate(message_en_text),
            reply_markup=kb.main,
        )


def translate(text: str) -> str:
    return translator.translate(text, dest="ru", srs="en").text


def is_admin(id: int) -> bool:
    if id == int(config.ADMIN_ID):
        return True
    return False


async def answer_admin(message_text: str) -> None:
    await bot.send_message(config.ADMIN_ID, message_text)


def login(func):
    @wraps(func)
    async def wrapper(message, *args, **kwargs):
        if not User.is_allow_user(id=message.from_user.id):
            await message.answer(_.NO_PERMISSIONS)
            await answer_admin(
                _.WANT_COMMAND_WITH_NO_PERMISSIONS(
                    message.from_user.id, message.from_user.username
                )
            )
            return
        result = await func(message, *args, **kwargs)
        return result

    return wrapper


def bot_polling() -> None:
    executor.start_polling(dp, skip_updates=True)


@dp.message_handler(commands=["start"], state=None)
async def start(message: types.Message):
    id = message.from_user.id
    username = message.from_user.username
    if User.is_have_user(id, username):
        await answer(message, _.NEW_USER)
        await answer_admin(_.NEW_USER_ADMIN(id, username))
    elif not User.is_allow_user(id):
        await answer(message, _.GET_PERMISSIONS)
        await answer_admin(_.WANT_PERMISSIONS(id, username))
    else:
        await answer(message, _.ALL_PERMISSIONS)


@dp.message_handler(commands=["allow"], state=None)
async def allow(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    tg_id_to_allow = int(message.text.strip().split()[1])
    if User.set_allow_user(tg_id_to_allow):
        await answer(message, _.ALLOW_USER)
    else:
        await answer(message, _.DISSALOW_USER)


@dp.message_handler(Text(equals=main_buttons["ask"]))
@login
async def ask(message: types.Message, state: FSMContext):
    await state.finish()
    await answer(message, _.ASK_ME)
    await Form.ask_state.set()


@dp.message_handler(state=Form.ask_state)
@login
async def gpt_answer(message: types.Message, state: FSMContext):
    if message.text == main_buttons["ask"]:
        await state.finish()
        return
    await answer(message, _.AWAIT(message.text))
    chat_answer = ChatGPT(api_key=api_key.key).answer(message.text)
    # chat_answer = ChatGPT(ask_text=message.text, api_key=api_key.key).answer
    User.ask(message.from_user.id, message.text, chat_answer)
    await answer_gpt(message, chat_answer)
    await answer_translate(message)
    await state.finish()


@dp.callback_query_handler(text_contains="translate_")
@login
async def translate_handler(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    translate_state = bool(int(call.data.split("_")[1]))
    if translate_state:
        await answer_translated_gpt(call, User.get_last_answer(id=call.from_user.id))


@dp.message_handler(content_types=["text"], state=None)
@login
async def not_response(message: types.Message, state: FSMContext):
    await answer(message, _.NOT_RESPONCE)
    await state.finish()
