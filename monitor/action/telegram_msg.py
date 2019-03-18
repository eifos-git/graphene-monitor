from . import AbstractAction
import telegram
token ='<your-telegram-token>'
bot = telegram.Bot(token=token)
chat_id = <your-chat-id>
# private: chat_id2 = <your-chat-id>


class TelegramMsg(AbstractAction):
    """Sends you a message via telegram."""
    def __init__(self, action_config):
        super().__init__(action_config)
        self.bot = telegram.Bot(token=token)

    def fire(self, message):
        self.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.parsemode.ParseMode.MARKDOWN)
