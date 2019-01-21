from monitor.action.AbstractAction import AbstractAction
import telegram_send


class TelegramAction(AbstractAction):

    def __init__(self, config):
        super().set_config(config)

    def fire(self, message):
        telegram_send.send(messages=[message])
