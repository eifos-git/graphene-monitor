from . import AbstractAction
import telegram_send


class Telegram(AbstractAction):
    """Sends you a message via telegram. Requires setup of the telegram_send module."""

    def fire(self, message):
        telegram_send.send(messages=[message])
