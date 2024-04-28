import telebot
from sqlalchemy.engine import create_engine
from sqlalchemy.sql import text

name = None
password = None
name_of_pass = None
log_of_name = None
pass_of_pass = None

bot = telebot.TeleBot('6914013926:AAG4oYUHrZi8_KU4WrjopPNq5LqUJf8SxoY')


@bot.message_handler(commands=['start'])
def start(message):
    eng = create_engine("sqlite:///Profiles.sql")
    conn = eng.connect()

    conn.execute(text("""CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key,
                   name varchar(50), passw varchar(50), nameofpass varchar(50), loginofpass varchar(50),
                   passofpass varchar(50))"""))
    conn.commit()
    conn.close()
    bot.reply_to(message, f'Привет, {message.from_user.first_name} {message.from_user.last_name} '
                          f'вы хотите зарегистрироваться или войти в аккаунт? (Войти/Зарегистрироваться)')
    bot.register_next_step_handler(message, check_ans)


def check_ans(message):
    if message.text.lower() == 'войти':
        bot.send_message(message.chat.id, 'Введите логин')
        bot.register_next_step_handler(message, entname)
    elif message.text.lower() == 'зарегистрироваться':
        bot.send_message(message.chat.id, 'Введите логин для вашего аккаунта')
        bot.register_next_step_handler(message, regname)
    else:
        bot.send_message(message.chat.id, 'Вы ввели неизвестную команду, напишите команду /start и попробуйте ещё раз')


def entname(message):
    global name
    name = message.text.strip()
    if name == '0':
        bot.reply_to(message, f'Привет, {message.from_user.first_name} {message.from_user.last_name} '
                              f'вы хотите зарегистрироваться или войти в аккаунт? (Войти/Зарегистрироваться)')
        bot.register_next_step_handler(message, check_ans)
    else:
        bot.send_message(message.chat.id, 'Введите пароль.')
        bot.register_next_step_handler(message, ent_pass)


def regname(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль.')
    bot.register_next_step_handler(message, reg_pass)


def ent_pass(message):
    global password
    password = message.text.strip()
    eng = create_engine("sqlite:///Profiles.sql")
    conn = eng.connect()
    users = conn.execute(text('SELECT * FROM users')).fetchall()
    k = 0
    for elem in users:
        if elem[1] == name and elem[2] == password and k != 1:
            k = 1
            sp = list()
            sp.append('Вы вошли в аккаунт! Что вы хотите сделать дальше?')
            sp.append("-Увидеть ваши сохраненные пароли (напишите ,,1'')")
            sp.append("-Сохранить Пароль (напишите ,,2'')")
            bot.send_message(message.chat.id, '\n'.join(sp))
            bot.register_next_step_handler(message, ent_do)
    if k == 0:
        bot.send_message(message.chat.id, 'Таких тут нет, попробуйте ещё раз или введите 0 для выхода')
        bot.send_message(message.chat.id, 'Введите логин')
        bot.register_next_step_handler(message, entname)

    conn.close()


def ent_do(message):
    ans = message.text.strip()
    if ans == str(2):
        bot.send_message(message.chat.id, 'Видите имя пароля')
        bot.register_next_step_handler(message, snop)
    elif ans == str(1):
        eng = create_engine("sqlite:///Profiles.sql")
        conn = eng.connect()
        users = conn.execute(text('SELECT * FROM users')).fetchall()

        info = ''
        for elem in users:
            if elem[1] == name and elem[3] != str(1):
                info += f'Имя: {elem[3]}, Логин: {elem[4]}, Пароль: {elem[5]}\n'

        conn.close()
        if len(info) != 0:
            bot.send_message(message.chat.id, info)
        else:
            bot.send_message(message.chat.id, 'У вас ещё нет сохраненных паролей.')
        sp = list()
        sp.append('Вы вошли в аккаунт! Что вы хотите сделать дальше?')
        sp.append("-Увидеть ваши сохраненные пароли (напишите ,,1'')")
        sp.append("-Сохранить Пароль (напишите ,,2'')")
        bot.send_message(message.chat.id, '\n'.join(sp))
        bot.register_next_step_handler(message, ent_do)


def snop(message):
    global name_of_pass
    name_of_pass = message.text.strip()
    bot.send_message(message.chat.id, 'Введите логин')
    bot.register_next_step_handler(message, logsp)


def logsp(message):
    global log_of_name
    log_of_name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, savepass)


def savepass(message):
    global pass_of_pass
    pass_of_pass = message.text.strip()
    eng = create_engine("sqlite:///Profiles.sql")
    conn = eng.connect()
    conn.execute(text(
        f"""INSERT INTO users (name, passw, nameofpass, loginofpass, passofpass)
            VALUES ('{name}', '{password}', '{name_of_pass}', '{log_of_name}', '{pass_of_pass}')"""
    ))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, 'Всё сохранилось')
    sp = list()
    sp.append('Вы вошли в аккаунт! Что вы хотите сделать дальше?')
    sp.append("-Увидеть ваши сохраненные пароли (напишите ,,1'')")
    sp.append("-Сохранить Пароль (напишите ,,2'')")
    bot.send_message(message.chat.id, '\n'.join(sp))
    bot.register_next_step_handler(message, ent_do)


def reg_pass(message):
    global password
    password = message.text.strip()
    eng = create_engine("sqlite:///Profiles.sql")
    conn = eng.connect()
    users = conn.execute(text('SELECT * FROM users')).fetchall()

    k = 0
    for elem in users:
        if elem[1] == name:
            k += 12
    if k == 0:
        conn.execute(text(f"""
            INSERT INTO users (name, passw, nameofpass, loginofpass, passofpass)
            VALUES ('{name}', '{password}', 1, 1, 1)
        """))
        conn.commit()
        conn.close()

        bot.send_message(message.chat.id, 'Пользователь зарегиистрирован! Что вы хотите сделать дальше?')
        sp = list()
        sp.append("-Увидеть ваши сохраненные пароли (напишите ,,1'')")
        sp.append("-Сохранить Пароль (напишите ,,2'')")
        bot.send_message(message.chat.id, '\n'.join(sp))
        bot.register_next_step_handler(message, ent_do)
    else:
        bot.send_message(
            message.chat.id,
            'Такой пользователь уже есть. Напишите команду /start, чтобы попробовать снова'
        )


bot.polling(none_stop=True)