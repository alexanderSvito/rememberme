import telebot



TOKEN = '783293998:AAHoM0ehXwv7RSIDnDj1j7WlME3x1U1mtUk'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)
