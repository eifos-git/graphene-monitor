from . import AbstractAction
import telegram_send


class TelegramAction(AbstractAction):

    def __init__(self, config):
        super().__init__(config)

    def fire(self, message):
        #telegram_send(message)
        print("------------TELEGRAM-------------")
        print(message)
        print("------------TELEGRAM-END-------------")
