import psycopg2
import telebot
from telebot import types
from datetime import datetime

API_TOKEN = '7373105149:AAE_PPxgz6ku6gdF5QJX8HJ252fOLW3Nifo'
bot = telebot.TeleBot(API_TOKEN)

# Admin IDlari ro'yxati
ADMIN_IDS = [123456789]  # Haqiqiy admin IDlarini kiriting

# Ma'lumotlar bazasiga ulanishni bir marta yaratamiz
try:
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='1234',
        host='localhost',
        port='5432',
        client_encoding='utf8'  # Kodlashni ko'rsatamiz
    )
    cursor = conn.cursor()
except Exception as e:
    print(f"Ma'lumotlar bazasiga ulanishda xatolik: {e}")
    exit()  # Dasturni to'xtatamiz, chunki ma'lumotlar bazasisiz ishlay olmaydi

# Sana formatini tekshirish funksiyasi
def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_name = message.from_user.username or message.from_user.first_name
    try:
        cursor.execute("INSERT INTO users (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING", (user_id, user_name))
        conn.commit()
        bot.send_message(message.chat.id, "Xush kelibsiz! Ro'yxatdan o'tdingiz.")
    except psycopg2.Error as e:  # psycopg2.Error dan foydalanamiz
        conn.rollback()
        bot.send_message(message.chat.id, f"Ro'yxatdan o'tishda xato yuz berdi: {e.pgcode} - {e.pgerror}")  # Batafsil xato ma'lumoti

# /newtask buyrug'i
@bot.message_handler(commands=['newtask'])
def new_task(message):
    bot.send_message(message.chat.id, "Vazifa nomini kiriting:")
    bot.register_next_step_handler(message, get_task_name)

def get_task_name(message):
    if not message.text:
        bot.send_message(message.chat.id, "Vazifa nomi bo'sh bo'lishi mumkin emas. Iltimos, qaytadan kiriting:")
        bot.register_next_step_handler(message, get_task_name)
        return

    task_name = message.text
    bot.send_message(message.chat.id, "Vazifa tavsifini kiriting:")
    bot.register_next_step_handler(message, get_task_description, task_name)

def get_task_description(message, task_name):
    task_description = message.text
    bot.send_message(message.chat.id, "Deadline (YYYY-MM-DD) formatida kiriting:")
    bot.register_next_step_handler(message, get_task_deadline, task_name, task_description)

def get_task_deadline(message, task_name, task_description):
    deadline = message.text
    if not is_valid_date(deadline):
        bot.send_message(message.chat.id, "Noto'g'ri sana formati. Iltimos, YYYY-MM-DD formatida kiriting:")
        bot.register_next_step_handler(message, get_task_deadline, task_name, task_description)
        return
    # Prioritetni tanlash uchun inline keyboard yaratamiz
    markup = types.InlineKeyboardMarkup()
    item_past = types.InlineKeyboardButton(text="Past", callback_data=f"priority:past:{task_name}:{task_description}:{deadline}")
    item_orta = types.InlineKeyboardButton(text="O'rta", callback_data=f"priority:orta:{task_name}:{task_description}:{deadline}")
    item_yuqori = types.InlineKeyboardButton(text="Yuqori", callback_data=f"priority:yuqori:{task_name}:{task_description}:{deadline}")
    markup.add(item_past, item_orta, item_yuqori)
    bot.send_message(message.chat.id, "Prioritetni tanlang:", reply_markup=markup)

# Prioritetni tanlash callbackini qayta ishlaymiz
@bot.callback_query_handler(func=lambda call: call.data.startswith("priority:"))
def process_priority_callback(call):
    priority_data = call.data.split(":")
    priority = priority_data[1]
    task_name = priority_data[2]
    task_description = priority_data[3]
    deadline = priority_data[4]

    user_id = call.from_user.id
    try:
        cursor.execute("INSERT INTO tasks (name, description, deadline, priority, user_id) VALUES (%s, %s, %s, %s, %s)",
                       (task_name, task_description, deadline, priority, user_id))
        conn.commit()
        bot.send_message(call.message.chat.id, "Vazifa yaratildi!")
    except psycopg2.Error as e:
        conn.rollback()
        bot.send_message(call.message.chat.id, f"Vazifa yaratishda xato yuz berdi: {e.pgcode} - {e.pgerror}")

@bot.message_handler(commands=['updatetask'])
def update_task(message):
    bot.send_message(message.chat.id, "Yangilamoqchi bo'lgan vazifa ID-sini kiriting:")
    bot.register_next_step_handler(message, get_task_id_to_update)

def get_task_id_to_update(message):
    try:
        task_id = int(message.text)
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        
        if task:
            bot.send_message(message.chat.id, "Yangi tavsifni kiriting:")
            bot.register_next_step_handler(message, update_task_description, task_id)
        else:
            bot.send_message(message.chat.id, "Bunday vazifa topilmadi.")
    except ValueError:
        bot.send_message(message.chat.id, "Iltimos, raqam kiriting.")
    except psycopg2.Error as e:
        bot.send_message(message.chat.id, f"Vazifani topishda xato yuz berdi: {e.pgcode} - {e.pgerror}")

def update_task_description(message, task_id):
    new_description = message.text
    try:
        cursor.execute("UPDATE tasks SET description = %s WHERE id = %s", (new_description, task_id))
        conn.commit()
        bot.send_message(message.chat.id, "Vazifa yangilandi!")
    except psycopg2.Error as e:
        conn.rollback()
        bot.send_message(message.chat.id, f"Vazifani yangilashda xato yuz berdi: {e.pgcode} - {e.pgerror}")

@bot.message_handler(commands=['deletetask'])
def delete_task(message):
    bot.send_message(message.chat.id, "O'chirmoqchi bo'lgan vazifa ID-sini kiriting:")
    bot.register_next_step_handler(message, get_task_id_to_delete)

def get_task_id_to_delete(message):
    try:
        task_id = int(message.text)
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        bot.send_message(message.chat.id, "Vazifa o'chirildi!")
    except ValueError:
        bot.send_message(message.chat.id, "Iltimos, raqam kiriting.")
    except psycopg2.Error as e:
        conn.rollback()
        bot.send_message(message.chat.id, f"Vazifani o'chirishda xato yuz berdi: {e.pgcode} - {e.pgerror}")

@bot.message_handler(commands=['stats'])
def stats(message):
    user_id = message.from_user.id
    try:
        # completed ustuni boolean bo'lishi kerak
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = %s AND completed = TRUE", (user_id,))
        completed_tasks = cursor.fetchone()
        completed_tasks_count = completed_tasks[0] if completed_tasks else 0

        cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = %s", (user_id,))
        total_tasks = cursor.fetchone()
        total_tasks_count = total_tasks[0] if total_tasks else 0

        bot.send_message(message.chat.id, f"Bajarilgan vazifalar: {completed_tasks_count}, Jami vazifalar: {total_tasks_count}")
    except psycopg2.Error as e:
        bot.send_message(message.chat.id, f"Statistikani olishda xato yuz berdi: {e.pgcode} - {e.pgerror}")

@bot.message_handler(commands=['mytasks'])
def my_tasks(message):
    user_id = message.from_user.id
    try:
        cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
        tasks = cursor.fetchall()
        
        if tasks:
            for task in tasks:
                # Assuming the columns are in this order: id, name, description, deadline, priority, user_id, completed
                task_id, task_name, task_description, task_deadline, task_priority, task_user_id, task_completed = task
                bot.send_message(message.chat.id, f"Vazifa: {task_name}, Tavsif: {task_description}, Deadline: {task_deadline}, Prioritet: {task_priority}, Bajarilgan: {'Ha' if task_completed else 'Yo\'q'}")
        else:
            bot.send_message(message.chat.id, "Sizda hech qanday vazifa yo'q.")
    except psycopg2.Error as e:
        bot.send_message(message.chat.id, f"Vazifalarni olishda xato yuz berdi: {e.pgcode} - {e.pgerror}")

# /help buyrug'i
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
    Komandalar:
    • /start - Botni ishga tushirish
    • /newtask - Yangi vazifa yaratish
    • /mytasks - Vazifalarni ko'rish
    • /updatetask - Vazifani yangilash
    • /deletetask - Vazifani o'chirish
    • /stats - Statistika ko'rish
    • /admin - Admin panel (faqat adminlar uchun)
    """
    bot.send_message(message.chat.id, help_text)

# Admin panel
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    user_id = message.from_user.id
    if user_id in ADMIN_IDS:
        # Admin panel funksiyalari (bu yerda admin funksiyalaringizni qo'shing)
        bot.send_message(message.chat.id, "Admin panelga xush kelibsiz!")
    else:
        bot.send_message(message.chat.id, "Siz admin emassiz!")

# Botni ishga tushirish
try:
    bot.polling()
except KeyboardInterrupt:
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Botda xato yuz berdi: {e}")
    cursor.close()
    conn.close()