from telebot import TeleBot, types

TOKEN = "7373105149:AAE_PPxgz6ku6gdF5QJX8HJ252fOLW3Nifo"
bot = TeleBot(TOKEN)

class FastFoodBot:
    def __init__(self):
        self.menu_items = [
            "🍴 Menyu 🍴",
            "📋 Mening buyurtmalarim 📋",
            "🛒 Savatcha 🛒",
            "📞 Aloqa 📞",
            "📨 Xabar yuborish 📨",
            "⚙️ Sozlamalar ⚙️"
        ]
        self.food_items = [
            "Setlar (8)",
            "Lavash (9)",
            "Burger (4)",
            "Shaurma (4)",
            "Hot-Dog (8)",
            "Ichimliklar (11)"
        ]
        self.lavash_items = [
            "Mol goshtidan qalampir lavash 1",
            "Mol goshtidan pishloqli lavash Standard 2",
            "FITTER 3",
            "Tovuq goshtli qalampir lavash 4",
            "Lavash cheese tovuq go'sht Standart 5",
            "Lavash tovuq go'sht 6",
            "Lavash mol go'sht 7",
        ]
        self.set_items = [
            "Combo Plus Isituvchan (Qora choy)",
            "Iftar kofte grill mol go'shtidan",
            "Donar boks tovuq go'shtidan",
            "Iftar strips tovuq go'shtidan",
            "Donar boks mol go'shtidan",
            "FitCombo",
            "Kids COMBO",
            "COMBO+",
            "☜(ﾟヮﾟ☜) Orqaga qaytish ☜(ﾟヮﾟ☜)"
        ]

    def display_menu(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for item in self.menu_items:
            markup.add(types.KeyboardButton(item))
        bot.send_message(message.chat.id, "Menyu:", reply_markup=markup)

    def display_food_menu(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for item in self.food_items:
            markup.add(types.KeyboardButton(item))
        markup.add(types.KeyboardButton("Orqaga qaytish"))  # Orqaga qaytish tugmasi
        bot.send_message(message.chat.id, "Taomlar:", reply_markup=markup)

    def display_lavash_menu(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for item in self.lavash_items:
            markup.add(types.KeyboardButton(item))
        markup.add(types.KeyboardButton("Orqaga qaytish"))  # Orqaga qaytish tugmasi
        bot.send_message(message.chat.id, "Lavashlar:", reply_markup=markup)

    def display_set_menu(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for item in self.set_items:
            markup.add(types.KeyboardButton(item))
        bot.send_message(message.chat.id, "Setlar:", reply_markup=markup)

fast_food_bot = FastFoodBot()

@bot.message_handler(commands=['start'])
def start(message):
    fast_food_bot.display_menu(message)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "🍴 Menyu 🍴":
        fast_food_bot.display_food_menu(message)
    elif message.text == "Lavash (9)":
        fast_food_bot.display_lavash_menu(message)
    elif message.text == "Setlar (8)":
        fast_food_bot.display_set_menu(message)
    elif message.text == "Orqaga qaytish":
        fast_food_bot.display_food_menu(message)  # Orqaga qaytish tugmasi
    elif message.text in fast_food_bot.menu_items:
        bot.send_message(message.chat.id, f"Siz {message.text} ni tanladingiz.")
    else:
        bot.send_message(message.chat.id, "Noto'g'ri tanlov, qaytadan urinib ko'ring.")

bot.polling()
