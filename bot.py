from aiogram import Bot, Dispatcher, executor, types

import requests
import json

from random import choice

from typing import Union, Tuple

# from local dir
from webapp.ownsecrets import BOT_TOKEN
from webapp.optional import WEBAPP_URL
from stylizing import stylize_date, stylize_time

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def process_event(event: Union[types.Message, types.CallbackQuery], with_user_id: bool = False) -> Union[types.Message, Tuple[types.Message, int]]:

    message = None
    if type(event) is types.Message:
        message = event
    else:
        await bot.answer_callback_query(event.id)
        message = event.message

    if not with_user_id:
        return message
    else:
        return (message, event.from_user.id)


async def deliver_message(event: Union[types.Message, types.CallbackQuery], init_message_editable: bool, **kwargs):

    message = await process_event(event)

    if type(event) is types.CallbackQuery and init_message_editable:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=kwargs['text'],
            reply_markup=kwargs['reply_markup']
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=kwargs['text'],
            parse_mode='Markdown',
            reply_markup=kwargs['reply_markup']
        )


@dp.message_handler(commands=['start', 'main'])
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'menu')
async def menu(event: Union[types.Message, types.CallbackQuery], init_message_editable: bool = True):

    inline_keyboard_markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton("Услуги", callback_data='services')],
        [types.InlineKeyboardButton("Информация", callback_data='info')],
        [types.InlineKeyboardButton("Активные записи", callback_data='active')]
    ])

    text = "Меню"

    await deliver_message(event, init_message_editable, text=text, reply_markup=inline_keyboard_markup)


@dp.message_handler(commands=['services'])
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'services')
async def services(event: Union[types.Message, types.CallbackQuery], init_message_editable: bool = True):

    message = await process_event(event)

    inline_keyboard_markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton("Записаться", web_app=types.WebAppInfo(url=f'{WEBAPP_URL}/make_order?init_message_id={message.message_id}'))],
        [types.InlineKeyboardButton("« Меню", callback_data='menu')]
    ])

    text = """Наши услуги:\n\n— Мужская стрижка · 1000 ₽\n— Оформление бороды · 500 ₽\n— Ваксинг (нос/уши/щеки) · 300 ₽"""

    await deliver_message(event, init_message_editable, text=text, reply_markup=inline_keyboard_markup)


@dp.pre_checkout_query_handler(lambda pre_checkout_query: True)
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):

    await bot.answer_pre_checkout_query(
        pre_checkout_query_id=pre_checkout_query.id,
        ok=True
    )


@dp.message_handler(content_types=types.message.ContentTypes.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):

    invoice_payload = message.successful_payment.invoice_payload
    user_id, init_message_id, services_ids, date_isoformat, time_isoformat = invoice_payload.split()
    user_id, init_message_id = int(user_id), int(init_message_id)

    requests.get(f'{WEBAPP_URL}/make_appointment', {
        'bot_token': BOT_TOKEN,
        'user_id': user_id,
        'services_ids': services_ids,
        'date_isoformat': date_isoformat,
        'time_isoformat': time_isoformat,
    }, verify=False)

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=init_message_id
    )

    sticker_id = choice((
        'CAACAgIAAxkBAAEGGPtjSrGs7cmA1WrC2SuEcnb4KrhQpwACyBEAAhXZmUi35TkWvq3pyioE',
        'CAACAgIAAxkBAAEGGP1jSrJ__QGsKO2PH3VSHGzQJmgNYAAC-Q4AAtKjmEgbHKF9Y-9YmioE',
        'CAACAgIAAxkBAAEGGP9jSrLNCRLXirCHfNbIQDmhVV8q1gACZhEAApcqUElfarX1iN_DOSoE'
    ))

    await bot.send_sticker(
        chat_id=message.chat.id,
        sticker=sticker_id
    )

    await menu(message, init_message_editable=False)


@dp.message_handler(commands=['info'])
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'info')
async def info(event: Union[types.Message, types.CallbackQuery], init_message_editable: bool = True):

    inline_keyboard_markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton("Адрес", callback_data='address')],
        [types.InlineKeyboardButton("Контакты", callback_data='contacts')],
        [types.InlineKeyboardButton("« Меню", callback_data='menu')]
    ])

    text = "🕓 Работаем каждый день с 11:00 до 21:00"

    await deliver_message(event, init_message_editable, text=text, reply_markup=inline_keyboard_markup)


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'address')
async def address(event: Union[types.Message, types.CallbackQuery]):

    message = await process_event(event)

    text = "📍 Улица имени В.И. Оржевского, 5, Саратов"
    
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=text
    )

    await bot.send_location(
        chat_id=message.chat.id,
        latitude=51.605542,
        longitude=46.012642
    )

    await info(message, init_message_editable=False)


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'contacts')
async def contacts(event: Union[types.Message, types.CallbackQuery]):

    message = await process_event(event)

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    await bot.send_contact(
        chat_id=message.chat.id,
        phone_number="+7 (8452) 49-55-40",
        first_name="Артём"
    )

    await info(message, init_message_editable=False)


@dp.message_handler(commands=['active'])
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'active')
async def active(event: Union[types.Message, types.CallbackQuery], active_appointment_idx: int = 0):

    message, user_id = await process_event(event, with_user_id=True)

    response = requests.get(f'{WEBAPP_URL}/get_active_appointments', {
        'bot_token': BOT_TOKEN,
        'user_id': user_id
    }, verify=False)

    active_appointments = response.json()['active_appointments']

    if (len(active_appointments) == 0):
        inline_keyboard_markup = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="« Меню", callback_data='menu')]])
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text="У вас пока нет активных записей",
            reply_markup=inline_keyboard_markup
        )
        return None

    active_appointment = active_appointments[active_appointment_idx]

    inline_keyboard_markup = types.InlineKeyboardMarkup()
    if (active_appointment_idx > 0):
            inline_keyboard_markup.insert(types.InlineKeyboardButton(text="« %s" % await stylize_date(active_appointments[active_appointment_idx - 1]['date']),
                    callback_data="active_nav prev %s" % active_appointment_idx))
    if (active_appointment_idx < len(active_appointments) - 1):
            inline_keyboard_markup.insert(types.InlineKeyboardButton(text="%s »" % await stylize_date(active_appointments[active_appointment_idx + 1]['date']),
                    callback_data="active_nav next %s" % active_appointment_idx))

    inline_keyboard_markup.add(types.InlineKeyboardButton(text="« Меню", callback_data="menu"))

    text = "Дата: *%s*\nВремя: *%s*\nУслуги:\n" % (await stylize_date(active_appointment['date']), await stylize_time(active_appointment['time']))
    for service_title in active_appointment['services_titles']:
            text += "\n— *%s*" % service_title

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=text,
        parse_mode='Markdown',
        reply_markup=inline_keyboard_markup
    )


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('active_nav'))
async def active_nav(callback_query: types.CallbackQuery):

    callback_query_data_split = callback_query.data.split()
    active_appointment_idx = int(callback_query_data_split[-1])

    if (callback_query_data_split[1] == 'prev'):
        await active(callback_query, active_appointment_idx - 1)
    else:
        await active(callback_query, active_appointment_idx + 1)


if __name__ == '__main__':
        executor.start_polling(dp, skip_updates=True)
