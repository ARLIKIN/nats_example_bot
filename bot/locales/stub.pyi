from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    hello: Hello
    button: Button
    no: No
    send: Send
    successfully: Successfully
    text: Text
    will: Will


class Hello:
    @staticmethod
    def user(*, username) -> Literal["""Привет, { $username }. Нажмите на кнопку"""]: ...


class Button:
    @staticmethod
    def button() -> Literal["""Кнопка"""]: ...

    @staticmethod
    def pressed() -> Literal["""Вы нажали на кнопку"""]: ...


class No:
    @staticmethod
    def copy() -> Literal["""Данный тип апдейтов не поддерживается методом send_copy"""]: ...


class Send:
    @staticmethod
    def text() -> Literal["""Отправьте любой текст, который необходимо сохранить в FSM-хранилище NATS"""]: ...


class Successfully:
    @staticmethod
    def saved() -> Literal["""Ваш текст успешно сохранен в NATS FSM-storage

Теперь вы можете получить данные из хранилища, отправив команду /read."""]: ...


class Text:
    @staticmethod
    def only() -> Literal["""Пожалуйста, отправляйте только текстовые сообщения"""]: ...


class Will:
    @staticmethod
    def delete(*, delay) -> Literal["""Это сообщение удалится через { $delay -&gt;
[one] { $delay }
[one]  секунду
[few] { $delay }
[few]  секунды
*[other] { $delay }
*[other]  секунд
}"""]: ...

