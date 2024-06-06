import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from random import randint
import datetime
import emoji
import time

logging.basicConfig(level=logging.INFO)
API_TOKEN = '6197458162:AAHsEjKB9esNyaoKKX0nYp56j-sQVfjAw0M'
bot = Bot(token=API_TOKEN, timeout=30)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
conn = sqlite3.connect('base.db')
cursor = conn.cursor()

id_of_commit = 0
name_of_commit = ''
end_of_commit_date = ''
id_of_first_person = 0
id_of_second_person = 0
id = 0
unique_id = 0
id_of_answer = 0

inline_kb1 = InlineKeyboardMarkup()
kb1 = InlineKeyboardButton('Спор', callback_data='Спор')
inline_kb1.add(kb1)

inline_kb2 = InlineKeyboardMarkup().add(InlineKeyboardButton(emoji.emojize(':check_mark_button:'), callback_data='Подтверждаю'))
inline_kb2.add(InlineKeyboardButton(emoji.emojize(':cross_mark:'), callback_data='Не подтверждаю'))

inline_kb3 = InlineKeyboardMarkup()
inline_kb3.add(InlineKeyboardButton('Название', callback_data='Название'))
inline_kb3.add(InlineKeyboardButton('Дата', callback_data='Дата'))
inline_kb3.add(InlineKeyboardButton('Видео', callback_data='Видео'))
inline_kb3.add(InlineKeyboardButton('Вернуться на старт', callback_data='Отмена'))

inline_kb4 = InlineKeyboardMarkup().add(InlineKeyboardButton('Я согласен с условиями' + ' ' + emoji.emojize(':check_mark_button:'), callback_data='Согласен'))
inline_kb4.add(InlineKeyboardButton('Я не согласен с условиями' + ' ' + emoji.emojize(':cross_mark:'), callback_data='Не согласен'))

reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
reply_keyboard.row(KeyboardButton('Я - инициатор'), KeyboardButton('Я - компаньон'), KeyboardButton('Текущие комиты'))

reply_keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
reply_keyboard2.row(KeyboardButton('Я был инициатором'), KeyboardButton('Я был компаньоном'))

inline_kb5 = InlineKeyboardMarkup().add(InlineKeyboardButton('Подтверждаю', callback_data='Подтверждаю2'))
inline_kb5.add(InlineKeyboardButton('Не подтвержаю', callback_data='Не подтверждаю2'))

inline_kb6 = InlineKeyboardMarkup().add(InlineKeyboardButton('Да', callback_data='Да'))
inline_kb6.add(InlineKeyboardButton('Нет', callback_data='Нет'))


class Form(StatesGroup):
    name = State()
    date = State()
    video = State()
    acception = State()


class Form2(StatesGroup):
    state1 = State()
    state2 = State()


class Form3(StatesGroup):
    state1 = State()
    state2 = State()


class Form4(StatesGroup):
    state1 = State()
    state2 = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    global id, id_of_commit, id_of_first_person, id_of_second_person, name_of_commit, end_of_commit_date, unique_id, id_of_answer
    await message.answer('Привет! Я помогу тебе заключить сделку и не забыть о ее взаимных условиях и, если будет нужно, сразу составлю соглашение, чтобы ты не тратил на это время! Ведь слово - ценно!')
    time.sleep(2)
    await message.answer('Суть проста. Просто выбери свою роль: ', reply_markup=reply_keyboard)
    id_of_commit = 0
    name_of_commit = ''
    end_of_commit_date = ''
    id_of_first_person = 0
    id_of_second_person = 0
    id = 0
    unique_id = 0
    id_of_answer = 0


@dp.message_handler(Text('Текущие комиты'))
async def process_button1(message: types.Message):
    await message.answer('Выберите:', reply_markup=reply_keyboard2)


@dp.message_handler(Text('Я был инициатором комита'))
async def process_button1(message: types.Message):
    global conn, cursor
    id = message.chat.id
    cursor.execute("SELECT * FROM list_of_iniciators WHERE id_of_iniciator=?", (id,))
    result = cursor.fetchall()
    if len(result) > 0:
        await message.answer('Список комитов: ')
        for e in result:
            id = e[3]
            cursor.execute("SELECT * FROM Svyaz WHERE unique_id=?", (id,))
            result2 = cursor.fetchall()
            result2 = result2[0]
            await message.answer(e[1])
            await message.answer(e[2])
            await bot.forward_message(chat_id=message.from_user.id, from_chat_id=result2[0], message_id=result2[3])
            await bot.forward_message(chat_id=message.from_user.id, from_chat_id=result2[0], message_id=result2[4])
    else:
        await message.answer('У вас еще нет комитов')


@dp.message_handler(Text('Я был компаньоном комита'))
async def process_button1(message: types.Message):
    global conn, cursor
    id = message.chat.id
    cursor.execute("SELECT * FROM list_of_companions WHERE id_of_companion=?", (id,))
    result = cursor.fetchall()
    if len(result) > 0:
        await message.answer('Список комитов: ')
        for e in result:
            id = e[3]
            cursor.execute("SELECT * FROM Svyaz WHERE unique_id=?", (id,))
            result2 = cursor.fetchall()
            result2 = result2[0]
            await message.answer(e[1])
            await message.answer(e[2])
            await bot.forward_message(chat_id=message.from_user.id, from_chat_id=result2[0], message_id=result2[3])
            await bot.forward_message(chat_id=message.from_user.id, from_chat_id=result2[0], message_id=result2[4])
    else:
        await message.answer('У вас еще нет комитов')


@dp.message_handler(Text('Я - инициатор'))
async def process_button1(message: types.Message):
    global id_of_first_person
    id_of_first_person = message.chat.id
    await message.answer('Какой у вас тип сделки?', reply_markup=inline_kb1)


@dp.callback_query_handler(lambda c: c.data == 'Спор')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Как будет называться ваша сделка? Напишите, я его запомню: ')
    await Form.name.set()
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


@dp.message_handler(state=Form.name)
async def name(message: types.Message):
    global name_of_commit
    try:
        name_of_commit = message.text
        await message.answer('Напишите дату, до какого времени сделка должна быть исполнена (формат ДД.ММ.ГГГГ): ')
        await Form.next()
    except Exception:
        await message.answer('Ошибка! Введите еще раз: ')
        await Form.name.set()


@dp.message_handler(state=Form.date)
async def date(message: types.Message, state: FSMContext):
    global end_of_commit_date
    end_of_commit_date = message.text
    try:
        date2 = end_of_commit_date
        date2 = date2.split('.')
        date2 = datetime.date(int(date2[2]), int(date2[1]), int(date2[0]))
        if datetime.date.today() > date2:
            await message.answer('Вы ввели дату в неверном формате, введите заново: ')
            await Form.date.set()
        else:
            await message.answer('Отлично! Теперь возьмите телефон и запишите на видео вашу сделку. Что нужно сделать:\n\
1) Озвучить ваши ФИО\n\
2) Озвучить на камеру суть сделки и ваши обязательства к партнеру\n\
3) Возможно пожелания по обязельствам партнера')
            await Form.next()
    except Exception:
        await message.answer('Вы ввели дату в неверном формате, введите заново: ')
        await Form.date.set()


@dp.message_handler(state=Form.video, content_types='video')
async def photo_or_doc_handler(message: types.Message, state: FSMContext):
    global id_of_commit
    try:
        id_of_commit = message.message_id
        await message.answer('Вот запись, на его базе мы сделаем соглашение. Посмотрите его, проверьте, все ли вы озвучили что хотели? Если да, то нажимай на галочку!', reply_markup=inline_kb2)
        await state.finish()
    except Exception:
        await message.answer('Ошибка! Введите еще раз: ')
        await Form.video.set()


@dp.callback_query_handler(lambda c: c.data == 'Подтверждаю')
async def process_callback_button(callback_query: types.CallbackQuery):
    global conn, cursor, id_of_commit, id_of_first_person, name_of_commit, end_of_commit_date
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    unique_id = randint(1000000, 9999999)
    end_of_commit_date = end_of_commit_date.replace('.', '-')
    end_of_commit_date = '-'.join(reversed(end_of_commit_date.split('-')))
    await bot.send_message(callback_query.from_user.id, f'Отлично, вот id сделки: {unique_id}. Отправляйте его вашему партнеру и если он согласует условия - то сделка вступит в силу')
    cursor.execute(
        f"INSERT INTO Svyaz (id_of_first, id_of_second, unique_id, message_id) VALUES ({int(id_of_first_person)}, 0, {int(unique_id)}, {int(id_of_commit)})")
    conn.commit()
    cursor.execute(
        f"INSERT INTO list_of_iniciators (id_of_iniciator, name_of_commit, ending_date_of_commit, unique_id) VALUES ({int(id_of_first_person)}, '{name_of_commit}', '{str(end_of_commit_date)}', {int(unique_id)})")
    conn.commit()


@dp.callback_query_handler(lambda c: c.data == 'Не подтверждаю')
async def process_callback_button(callback_query: types.CallbackQuery, ):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Так, давайте поправим, что не так: ', reply_markup=inline_kb3)


@dp.callback_query_handler(lambda c: c.data == 'Название')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Дайте название комиту:')
    await Form.name.set()


@dp.callback_query_handler(lambda c: c.data == 'Дата')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Напишите дату, до какого времени сделка должна быть исполнена (формат ДД.ММ.ГГГГ): ')
    
    await Form.date.set()


@dp.callback_query_handler(lambda c: c.data == 'Видео')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Отлично! Теперь возьмите телефон и запишите на видео вашу сделку. Что нужно сделать:\n\
    1) Озвучить ваши ФИО\n\
    2) Озвучить на камеру суть сделки и ваши обязательства к партнеру\n\
    3) Возможно пожелания по обязельствам партнера')
    await Form.video.set()


@dp.callback_query_handler(lambda c: c.data == 'Отмена')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Спасибо за обращение')
    cursor.execute("DELETE * FROM Svyaz WHERE unique_id=?", (id,))
    conn.commit()
    cursor.execute("DELETE * FROM list_of_companions WHERE unique_id=?", (id,))
    conn.commit()
    cursor.execute("DELETE * FROM list_of_iniciators WHERE unique_id=?", (id,))
    conn.commit()


@dp.message_handler(Text('Я - компаньон'))
async def process_button1(message: types.Message):
    try:
        global id_of_second_person
        id_of_second_person = message.chat.id
        await message.answer('Отправьте id обращения, которое Вам передал инициатор: ')
        await Form2.state1.set()
    except Exception:
        await message.answer('Ошибка! Введите еще раз: ')


@dp.message_handler(state=Form2.state1)
async def condition(message: types.Message, state: FSMContext):
    try:
        global id, conn, cursor
        id = int(message.text)
        if len(str(id)) != 7:
            await message.answer('Некорректная форма идентификатора, проверьте правильность ввода.')
            await message.answer('Отправьте уникальный идентификатор связи, который перед Вам Ваш партнер: ')
            await Form2.state1.set()
        cursor.execute("SELECT * FROM Svyaz WHERE unique_id=?", (id,))
        result = cursor.fetchone()
        if result[1] == 0:
            await message.answer('Вот суть сделки, которую озвучил ваш партнер.')
            cursor.execute("SELECT * FROM list_of_iniciators WHERE unique_id=?", (id,))
            result2 = cursor.fetchone()
            await bot.send_message(chat_id=message.from_user.id, text=f'{result2[1]}')
            await bot.send_message(chat_id=message.from_user.id, text=f'{result2[2]}')
            await bot.forward_message(chat_id=message.from_user.id, from_chat_id=result[0], message_id=result[3])
            cursor.execute("UPDATE svyaz SET id_of_second=? WHERE unique_id=? ",
                           (id_of_second_person, id))
            conn.commit()
        elif result[1] == id_of_second_person:
            await bot.send_message(chat_id=message.from_user.id, text='Вот суть сделки, которую озвучил ваш партнер.: ')
            cursor.execute("SELECT * FROM list_of_iniciators WHERE unique_id=?", (id,))
            result2 = cursor.fetchone()
            await bot.send_message(chat_id=message.from_user.id, text=f'{result2[1]}')
            await bot.send_message(chat_id=message.from_user.id, text=f'{result2[2]}')
            await bot.forward_message(chat_id=message.from_user.id, from_chat_id=result[0], message_id=result[3])
        else:
            print('Вы ввели идентификатор, который принадлежит другому человеку')
            await Form2.state1.set()
        await message.answer('Внимательно все прослушайте, и согласуйте условия: ', reply_markup=inline_kb4)
        await state.finish()
    except Exception:
        await message.answer('Ошибка! Введите еще раз: ')
        await Form.video.set()


@dp.callback_query_handler(lambda c: c.data == 'Согласен')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Отлично! Теперь возьмите телефон и запишите на видео вашу сделку. Что нужно сделать:\n\
1) Озвучить ваши ФИО\n\
2) Озвучить на камеру суть сделки и ваши обязательства к партнеру\n\
3) Возможно пожелания по обязельствам партнера')
    await Form2.state1.set()


@dp.callback_query_handler(lambda c: c.data == 'Не согласен')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    cursor.execute("SELECT * FROM Svyaz WHERE unique_id=?", (id,))
    result = cursor.fetchone()
    user_id = int(result[0])
    await bot.send_message(callback_query.from_user.id,
                           'Отлично, что правим в условиях? Напишите пожалуйста ваши комментарии для правок, чтобы ваш партнер мог их учесть')



    #Доделать





    await bot.send_message(chat_id=user_id, text='Ваш компаньон не согласился с условиями.',
                           reply_markup=reply_keyboard)
    await bot.send_message(callback_query.from_user.id, 'Добрый день, выберите режим работы',
                           reply_markup=reply_keyboard)
    cursor.execute("DELETE * FROM Svyaz WHERE unique_id=?", (id,))
    conn.commit()
    cursor.execute("DELETE * FROM list_of_companions WHERE unique_id=?", (id,))
    conn.commit()
    cursor.execute("DELETE * FROM list_of_iniciators WHERE unique_id=?", (id,))
    conn.commit()


@dp.message_handler(state=Form3.state1, content_types='video')
async def photo_or_doc_handler(message: types.Message, state: FSMContext):
    try:
        global id_of_answer
        id_of_answer = message.message_id
        await message.answer('Подтвержаете ли Вы все условия, озвученные в видео.', reply_markup=inline_kb5)
        await state.finish()
    except Exception:
        await message.answer('Ошибка! Введите еще раз: ')
        await Form3.state1.set()


@dp.callback_query_handler(lambda c: c.data == 'Подтверждаю2')
async def process_callback_button(callback_query: types.CallbackQuery):
    global conn, cursor, id_of_answer, id, end_of_commit_date, name_of_commit
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    cursor.execute(f'UPDATE svyaz SET answer_id=? WHERE unique_id=?', (id_of_answer, id,))
    conn.commit()
    cursor.execute("SELECT * FROM Svyaz WHERE unique_id=?", (id,))
    result = cursor.fetchone()
    await bot.forward_message(from_chat_id=result[1], chat_id=result[0], message_id=result[-1])
    cursor.execute("SELECT * FROM Svyaz WHERE unique_id=?", (id,))
    result = cursor.fetchone()
    await bot.send_message(chat_id=result[0], text='Вы согласны?', reply_markup=inline_kb6)
    cursor.execute("SELECT * FROM list_of_iniciators WHERE unique_id=?", (id,))
    result = cursor.fetchone()
    cursor.execute(
        f"INSERT INTO list_of_companions (id_of_companion, name_of_commit, ending_date_of_commit, unique_id) VALUES ({id_of_second_person}, '{result[1]}', '{result[2]}', {id})")
    conn.commit()


@dp.callback_query_handler(lambda c: c.data == 'Не подтверждаю2')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Запишите видео еще раз:')
    await Form3.state1.set()


@dp.callback_query_handler(lambda c: c.data == 'Да')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    cursor.execute("SELECT * FROM Svyaz WHERE unique_id=?", (id,))
    result = cursor.fetchone()
    await bot.send_message(chat_id=result[0], text='Пусть так и будет. Объявляем сделку заключенной. Слово - ценно!', reply_markup=reply_keyboard)
    await bot.send_message(chat_id=result[1], text='Пусть так и будет. Объявляем сделку заключенной. Слово - ценно!', reply_markup=reply_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'Нет')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    cursor.execute("DELETE * FROM Svyaz WHERE unique_id=?", (id,))
    conn.commit()
    cursor.execute("DELETE * FROM list_of_companions WHERE unique_id=?", (id,))
    conn.commit()
    cursor.execute("DELETE * FROM list_of_iniciators WHERE unique_id=?", (id,))
    conn.commit()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
