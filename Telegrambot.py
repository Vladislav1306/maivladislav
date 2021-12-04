import telebot;
import sqlite3;
from telebot import types;

conn = sqlite3.connect('DataBase1.db', check_same_thread=False);
cursor = conn.cursor();

bot = telebot.TeleBot('мяу');

@bot.message_handler(commands=['start'])
def start_message(message):

	bot.send_message(message.chat.id, 'Добро пожаловать, введите ваш персональный код.')

op_git = 0

@bot.message_handler(content_types=['text'])

def authorization(message):

	if message.text.isdigit() == True :
		if message.text == "50" :
			for row in cursor.execute(f"SELECT Name, Surname, Post FROM Univer WHERE Number = {message.text}"):
				bot.send_message(message.chat.id, f'Вы вошли под именем {row[0]} {row[1]} ({row[2]}).')
				bot.send_message(message.chat.id, 'Вы можете отправить ссылку на git с модульными тестами. Для этого введите 1 и следующим сообщением отправьте ссылку.')
				bot.send_message(message.chat.id, 'Вы можете опубликовать задание для конкретного студента. Для этого введите 2 и следуйте инструкциям.')
				bot.send_message(message.chat.id, 'Вы можете просмотреть данные о студентах. Для этого введите 3.')
				bot.send_message(message.chat.id, 'Вы можете поставить оценки студентам. Для этого введите 4.')
				bot.register_next_step_handler(message, choice_teacher);
		if int(message.text) >= 1 and int(message.text) <= 3:
			for row in cursor.execute(f"SELECT Task FROM Univer WHERE Number = {message.text}"):
				bot.send_message(message.chat.id, f'Твое задание: {row[0]}.')
			for row in cursor.execute(f"SELECT Option FROM Univer WHERE Number = {message.text}"):
				bot.send_message(message.chat.id, f'Твой вариант задания: {row[0]}.')
				global op_git
				op_git = row[0];
			bot.send_message(message.chat.id, 'Если ты хочешь сдать задние, то отправь боту ссылку на свой репозиторий git.')
			bot.register_next_step_handler(message, sub_task);
	else: bot.send_message(message.chat.id, 'Ввод некоректный.')

def sub_task(message):

	git = message.text;
	sql_update_query = """UPDATE Univer SET Git = ? WHERE Option = ?"""
	data = (git, op_git)
	cursor.execute(sql_update_query, data)
	conn.commit()
	bot.send_message(message.chat.id, 'Получил, жди оценку от преподавателя.')

def choice_teacher(message):
	
	global var
	if message.text == "1" or "2" or "3" or "4":
		if message.text == "1" :
			bot.send_message(message.chat.id, 'Ожидаю ссылку.')
			bot.register_next_step_handler(message, sub_gtest);
		if message.text == "2" :
			var = 2
			bot.send_message(message.chat.id, 'Введите номер студента в списке.')
			bot.register_next_step_handler(message, get_num);
		if message.text == "3" :
			bot.send_message(message.chat.id, 'Введите количество учеников в группе.')
			bot.register_next_step_handler(message, show_data);
		if message.text == "4" :
			var = 4
			bot.send_message(message.chat.id, 'Введите номер студента в списке.')
			bot.register_next_step_handler(message, get_num);
	else: bot.send_message(message.chat.id, 'Ввод некоректный.')

def sub_gtest(message):

	Git = message.text;
	Num = 50
	sql_update_query1 = """UPDATE Univer SET Git = ? WHERE Number = ?"""
	data1 = (Git, Num)
	cursor.execute(sql_update_query1, data1)
	conn.commit()
	bot.send_message(message.chat.id, 'Git с модульными тестами получен.')

def get_num(message):

	if message.text.isdigit() == True :
		if int(message.text) >= 1 and int(message.text) <= 3:
			global Num
			Num = message.text
			if var == 2 :
				bot.register_next_step_handler(message, get_task);
				bot.send_message(message.chat.id, 'Введите задание.')
			if var == 4 :
				bot.register_next_step_handler(message, get_mark);
				bot.send_message(message.chat.id, 'Введите оценку.')
		else: bot.send_message(message.chat.id, 'Ввод некоректный.')
	else: bot.send_message(message.chat.id, 'Ввод некоректный.')

def get_task(message):

	Task = message.text;
	sql_update_query2 = """UPDATE Univer SET Task = ? WHERE Number = ?"""
	data2 = (Task, Num)
	cursor.execute(sql_update_query2, data2)
	conn.commit()
	for row in cursor.execute(f"SELECT Name, Surname FROM Univer WHERE Number = {Num}"):
		bot.send_message(message.chat.id, f'Задание для {row[0]} {row[1]} записано.')

def show_data(message):

	if message.text.isdigit() == True :
		sqlite_select_query = """SELECT Number, Name, Surname, Task, Mark, Option, Git FROM Univer"""
		cursor.execute(sqlite_select_query)
		records = cursor.fetchmany(int(message.text))
		for row in records:
			bot.send_message(message.chat.id, f'| {row[0]} |	| {row[1]} |	| {row[2]} |	| {row[3]} |	| {row[4]} |	| {row[5]} |	| {row[6]} |.')
	else: bot.send_message(message.chat.id, 'Ввод некоректный.')

def	get_mark(message):

	Mark = message.text;
	sql_update_query3 = """UPDATE Univer SET Mark = ? WHERE Number = ?"""
	data3 = (Mark, Num)
	cursor.execute(sql_update_query3, data3)
	conn.commit()
	for row in cursor.execute(f"SELECT Name, Surname FROM Univer WHERE Number = {Num}"):
		bot.send_message(message.chat.id, f'Оценка для {row[0]} {row[1]} записана.')

bot.polling(none_stop=True, interval=0)
