from . import AbstractAction
import telegram_send


class Telegram(AbstractAction):

    def fire(self, message):
        telegram_send.send(messages=[message])
