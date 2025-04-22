from telebot import TeleBot, types

TOKEN = "7373105149:AAE_PPxgz6ku6gdF5QJX8HJ252fOLW3Nifo"  # TOKEN ni o'zgartiring
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
        self.prices = {
            "Lavash (9)": 15000,
            "Burger (4)": 20000,
            "Shaurma (4)": 18000,
            "Hot-Dog (8)": 12000,
            "Ichimliklar (11)": 5000,
            "Setlar (8)": 25000
        }
        self.lavash_items = [
            "Mol goshtidan qalampir lavash 1 - 15000 so'm",
            "Mol goshtidan pishloqli lavash Standard 2 - 18000 so'm",
            "FITTER 3 - 16000 so'm",
            "Tovuq goshtli qalampir lavash 4 - 17000 so'm",
            "Lavash cheese tovuq go'sht Standart 5 - 18000 so'm",
            "Lavash tovuq go'sht 6 - 16000 so'm",
            "Lavash mol go'sht 7 - 15000 so'm",
        ]
        self.burger_items = [
            "Classic Burger - 20000 so'm",
            "Cheese Burger - 22000 so'm",
            "Spicy Chicken Burger - 24000 so'm",
            "Veggie Burger - 18000 so'm"
        ]
        self.hot_dog_items = [
            "Classic Hot-Dog - 12000 so'm",
            "Cheese Hot-Dog - 14000 so'm",
            "Spicy Hot-Dog - 15000 so'm",
            "Veggie Hot-Dog - 13000 so'm",
            "BBQ Hot-Dog - 16000 so'm",
            "Chili Hot-Dog - 17000 so'm",
            "Bacon Hot-Dog - 18000 so'm",
            "Deluxe Hot-Dog - 20000 so'm"
        ]
        self.drink_items = [
            "Coca-Cola - 5000 so'm",
            "Fanta - 5000 so'm",
            "Sprite - 5000 so'm",
            "Pepsi - 5000 so'm",
            "Mineral Water - 3000 so'm",
            "Juice - 6000 so'm",
            "Iced Tea - 6000 so'm",
            "Coffee - 7000 so'm",
            "Tea - 3000 so'm",
            "Lemonade - 6000 so'm",
            "Energy Drink - 10000 so'm"
        ]
        self.shaurma_items = [
            "Mol go'shti shaormasi - 18000 so'm",
            "Tovuq go'shti shaormasi - 17000 so'm",
            "Vegetarian shaorma - 15000 so'm",
            "Spicy shaorma - 19000 so'm"
        ]
        self.set_items = [
            "Combo Plus Isituvchan (Qora choy) - 25000 so'm",
            "Iftar kofte grill mol go'shtidan - 27000 so'm",
            "Donar boks tovuq go'shtidan - 26000 so'm",
            "Iftar strips tovuq go'shtidan - 28000 so'm",
            "Donar boks mol go'shtidan - 29000 so'm",
            "FitCombo - 24000 so'm",
            "Kids COMBO - 22000 so'm",
            "COMBO+ - 30000 so'm"
        ]
        self.cart = []

    def display_menu(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for item in self.menu_items:
            markup.add(types.KeyboardButton(item))
        bot.send_message(message.chat.id, "Menyu:", reply_markup=markup)

    def display_food_menu(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for item in self.food_items:
            markup.add(types.KeyboardButton(item))
        markup.add(types.KeyboardButton("↩️ Orqaga qaytish ↩️"))
        bot.send_message(message.chat.id, "Taomlar:", reply_markup=markup)

    def display_lavash_menu(self, message):
        self._display_sub_menu(message, self.lavash_items, "Lavashlar:")

    def display_burger_menu(self, message):
        self._display_sub_menu(message, self.burger_items, "Burgerlar:")

    def display_hot_dog_menu(self, message):
        self._display_sub_menu(message, self.hot_dog_items, "Hot-Doglar:")

    def display_drink_menu(self, message):
        self._display_sub_menu(message, self.drink_items, "Ichimliklar:")

    def display_shauma_menu(self, message):
        self._display_sub_menu(message, self.shaurma_items, "Shaurmalar:")

    def display_set_menu(self, message):
        self._display_sub_menu(message, self.set_items, "Setlar:")

    def _display_sub_menu(self, message, items, title):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for item in items:
            markup.add(types.KeyboardButton(item))
        markup.add(types.KeyboardButton("↩️ Orqaga qaytish ↩️"))
        bot.send_message(message.chat.id, title, reply_markup=markup)

    def add_to_cart(self, item):
        self.cart.append(item)

    def view_cart(self, message):
        if not self.cart:
            bot.send_message(message.chat.id, "Savatchangiz bo'sh.")
        else:
            cart_items = "\n".join(self.cart)
            bot.send_message(message.chat.id, f"Savatchangiz:\n{cart_items}")

    def view_orders(self, message):
        if not self.cart:
            bot.send_message(message.chat.id, "Sizda hech qanday buyurtma yo'q.")
        else:
            orders = "\n".join(self.cart)
            bot.send_message(message.chat.id, f"Sizning buyurtmalaringiz:\n{orders}")

    def display_contact_info(self, message):
        contact_info = (
            "📞 **Aloqa** 📞\n\n"
            "Biz bilan bog'lanish juda oson! Sizni qiziqtirgan savollar yoki buyurtmalar bo'yicha yordam berish uchun biz har doim tayyormiz.\n\n"
            "🕒 **Ish vaqti**:\n"
            "- **Dushanba - Juma**: 09:00 - 20:00\n"
            "- **Shanba - Yakshanba**: 10:00 - 18:00\n\n"
            "📱 **Telefon raqami**:\n"
            "- +998 90 123 45 67\n\n"
            "🚚 **Yetkazib berish xizmati**:\n"
            "Biz sizning buyurtmangizni tez va sifatli yetkazib beramiz! Har qanday joyga yetkazib berishimiz mumkin. Sizning qulayligingiz biz uchun muhim!\n\n"
            "Agar sizda biron bir savol yoki taklif bo'lsa, iltimos, biz bilan bog'laning. Sizni kutamiz! 🌟"
        )
        bot.send_message(message.chat.id, contact_info, parse_mode='Markdown')

fast_food_bot = FastFoodBot()

@bot.message_handler(commands=['start'])
def start(message):
    fast_food_bot.display_menu(message)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "🍴 Menyu 🍴":
        fast_food_bot.display_food_menu(message)
    elif message.text == "Burger (4)":
        fast_food_bot.display_burger_menu(message)
    elif message.text == "Hot-Dog (8)":
        fast_food_bot.display_hot_dog_menu(message)
    elif message.text == "Ichimliklar (11)":
        fast_food_bot.display_drink_menu(message)
    elif message.text == "Shaurma (4)":
        fast_food_bot.display_shauma_menu(message)
    elif message.text == "Lavash (9)":
        fast_food_bot.display_lavash_menu(message)
    elif message.text == "Setlar (8)":
        fast_food_bot.display_set_menu(message)
    elif message.text == "📞 Aloqa 📞":
        fast_food_bot.display_contact_info(message)
    elif message.text == "📨 Xabar yuborish 📨":
        bot.send_message(message.chat.id, "Bu yer bo'sh.")
    elif message.text == "⚙️ Sozlamalar ⚙️":
        bot.send_message(message.chat.id, "Bu yerda baloyam yo'q 🤣")
    elif message.text == "↩️ Orqaga qaytish ↩️":
        fast_food_bot.display_menu(message)
    elif message.text in fast_food_bot.burger_items:
        fast_food_bot.add_to_cart(message.text)
        bot.send_message(message.chat.id, f"Savatchaga {message.text} qo'shildi.")
    elif message.text in fast_food_bot.hot_dog_items:
        fast_food_bot.add_to_cart(message.text)
        bot.send_message(message.chat.id, f"Savatchaga {message.text} qo'shildi.")
    elif message.text in fast_food_bot.drink_items:
        fast_food_bot.add_to_cart(message.text)
        bot.send_message(message.chat.id, f"Savatchaga {message.text} qo'shildi.")
    elif message.text in fast_food_bot.shaurma_items:
        fast_food_bot.add_to_cart(message.text)
        bot.send_message(message.chat.id, f"Savatchaga {message.text} qo'shildi.")
    elif message.text in fast_food_bot.lavash_items:
        fast_food_bot.add_to_cart(message.text)
        bot.send_message(message.chat.id, f"Savatchaga {message.text} qo'shildi.")
    elif message.text in fast_food_bot.set_items:
        fast_food_bot.add_to_cart(message.text)
        bot.send_message(message.chat.id, f"Savatchaga {message.text} qo'shildi.")
    elif message.text == "🛒 Savatcha 🛒":
        fast_food_bot.view_cart(message)
    elif message.text == "📋 Mening buyurtmalarim 📋":
        fast_food_bot.view_orders(message)
    else:
        bot.send_message(message.chat.id, "Noto'g'ri tanlov, qaytadan urinib ko'ring.")

bot.polling()
