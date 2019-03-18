import telegram
token ='<your-telegram-token>'
bot = telegram.Bot(token=token)
chat_id = <your-chat-id>


message = 'Monitor Http_and_Peerplays_Monitor fired\nEvent Id: [1.22.256](http://95.216.13.245:8001/overview/event/1.22.256\n'
bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.parsemode.ParseMode.MARKDOWN)