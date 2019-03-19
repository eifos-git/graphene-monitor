from . import AbstractAction
import logging
import telegram
token ='<your-telegram-token>'
bot = telegram.Bot(token=token)
chat_id = <your-chat-id>
# private: chat_id2 = <your-chat-id>


class TelegramMsg(AbstractAction):
    """Sends you a message via telegram.
    Config values are:

    * token: The individual token for your telegram bot. :ref:`How to setup <telegram_setup>`
    * chat_id: Chat id for your telegram bot. See token on how to get it.
    """
    def __init__(self, action_config):
        super().__init__(action_config)
        self.token = self.get_token()
        self.chat_id = self.get_chat_id()
        if self.token:
            self.bot = telegram.Bot(token=self.token)

    def get_token(self):
        return self.get_config("token")

    def get_chat_id(self):
        return self.get_config("chat_id")

    def fire(self, message):
        if self.token is None:
            logging.warning("Unable to send message due to missing token")
            return
        if self.chat_id is None:
            logging.warning("Unable to send message due to missing chat_id")
            return
        try:
            self.bot.send_message(chat_id=self.chat_id, text=message, parse_mode=telegram.parsemode.ParseMode.MARKDOWN)
        except telegram.error.BadRequest:
            logging.warning("Bad Request for telegram.send_message. Double-check the token and chat_id values. This "
                            "may also be because you added a underscore (_) symbol to your config. Those are not "
                            "supported for markdown. Remove them or use \_ instead")
        except telegram.error.Unauthorized:
            logging.warning("Unauthorized Error in Telegram send. Make sure that token and chat_id are correct and"
                            "that you contacted the bot first")

