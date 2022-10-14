from aiogram import Bot, Dispatcher, executor, types
import logging

from typing import Optional, Union

# from local dir
from webapp.ownsecrets import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def event_process(event: Union[types.Message, types.CallbackQuery]) -> types.Message:

	if type(event) is types.Message:
		return event
	else:
		await bot.answer_callback_query(callback_query_id=event.id)
		return event.message


@dp.message_handler(commands=['start', 'main'])
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'menu')
async def menu(event: Union[types.Message, types.CallbackQuery], init_message_editable: bool = True):

	message = await event_process(event)

	inline_keyboard_markup = types.InlineKeyboardMarkup(inline_keyboard=[
		[types.InlineKeyboardButton("Услуги", callback_data='services')],
		[types.InlineKeyboardButton("Информация", callback_data='info')],
		[types.InlineKeyboardButton("Активные записи 🏗️", callback_data='active')]
	])

	text = "Меню"

	if type(event) is types.CallbackQuery and init_message_editable:
		await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
			text=text,
			reply_markup=inline_keyboard_markup)
	else:
		await bot.send_message(chat_id=message.chat.id,
			text=text,
			parse_mode='Markdown',
			reply_markup=inline_keyboard_markup)


@dp.message_handler(commands=['services'])
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'services')
async def services(event: Union[types.Message, types.CallbackQuery], init_message_editable: bool = True):

	message = await event_process(event)

	inline_keyboard_markup = types.InlineKeyboardMarkup(inline_keyboard=[
		[types.InlineKeyboardButton("Записаться", web_app=types.WebAppInfo(url='https://fruitourist.ru/liot/make_order'))],
		[types.InlineKeyboardButton("« Меню", callback_data='menu')]
	])

	text = """Наши услуги:\n\n— Мужская стрижка · 1000 ₽\n— Оформление бороды · 500 ₽\n— Ваксинг (нос/уши/щеки) · 300 ₽"""

	if type(event) is types.CallbackQuery and init_message_editable:
		await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
			text=text,
			reply_markup=inline_keyboard_markup)
	else:
		await bot.send_message(chat_id=message.chat.id,
			text=text,
			parse_mode='Markdown',
			reply_markup=inline_keyboard_markup)


@dp.message_handler(commands=['info'])
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'info')
async def info(event: Union[types.Message, types.CallbackQuery], init_message_editable: bool = True):

	message = await event_process(event)

	inline_keyboard_markup = types.InlineKeyboardMarkup(inline_keyboard=[
		[types.InlineKeyboardButton("Адрес", callback_data='address')],
		[types.InlineKeyboardButton("Контакты", callback_data='contacts')],
		[types.InlineKeyboardButton("« Меню", callback_data='menu')]
	])

	text = "🕓 Работаем каждый день с 11:00 до 21:00"

	if type(event) is types.CallbackQuery and init_message_editable:
		await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
			text=text,
			reply_markup=inline_keyboard_markup)
	else:
		await bot.send_message(chat_id=message.chat.id,
			text=text,
			parse_mode='Markdown',
			reply_markup=inline_keyboard_markup)


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'address')
async def address(event: Union[types.Message, types.CallbackQuery]):

	message = await event_process(event)

	text = "📍 Улица имени В.И. Оржевского, 5, Саратов"
	
	await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
		text=text)

	await bot.send_location(chat_id=message.chat.id,
		latitude=51.605542,
		longitude=46.012642)

	await info(message, init_message_editable=False)



@dp.callback_query_handler(lambda callback_query: callback_query.data == 'contacts')
async def contacts(event: Union[types.Message, types.CallbackQuery]):

	message = await event_process(event)

	await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

	await bot.send_contact(chat_id=message.chat.id, phone_number="+7 (8452) 49-55-40", first_name="Артём")

	await info(message, init_message_editable=False)


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)