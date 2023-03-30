from dataclasses import dataclass


@dataclass
class Messages:
    NEW_USER = "Создаю нового пользователя. Для работы с ботом запросите доступ у администратора."
    GET_PERMISSIONS = "Для работы с ботом запросите доступ у администратора."
    ALL_PERMISSIONS = "Вы уже зарегестрированы и имеете доступ."
    ALLOW_USER = "Пользователь разрешен."
    DISSALOW_USER = "Ошибка разрешения пользователя."
    NO_PERMISSIONS = "У Вас недостаточно прав, запросите доступ у администратора."
    ASK_ME = "Задайте вопрос желательно на английском языке."
    TRANSLATE = "Желаете перевести ответ?"
    NOT_RESPONCE = "Не понимаю."

    def NEW_USER_ADMIN(id: int, username: str) -> str:
        return f"Новый пользователь {id} {username}."

    def WANT_PERMISSIONS(id: int, username: str) -> str:
        return f"Пользователь запрашивает права {id} {username}."

    def WANT_COMMAND_WITH_NO_PERMISSIONS(id: int, username: str) -> str:
        return f"Пользователь {id} {username} не смог получить доступ к действию."

    def AWAIT(answer: str) -> str:
        return f"Ваш вопрос '{answer}' - принят. Ожидайте ответа."
