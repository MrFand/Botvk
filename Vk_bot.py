import vk_api
import time
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import sqlite3
import config
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import bs4
import time
import pyowm
import requests
import datetime
import random

class bot:
	
	def __init__(self, user_id):
		self.USER_ID = user_id
		self.USERNAME = self.get_name_from_vk(user_id)['name']
		self.COMMANDS = ['Привет', 'Погода', 'Время', 'Пока', 'Команды', 'Статистика', 'начать', 'Виселица']
		self.CITY = self.get_user_city(user_id)
		
		self.alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
	def random_word(self):
		word = config.words[random.randint(0, len(config.words))]
		return word
	def get_letter(self, user_id):
		user_data = self.sql_select_user(user_id)
		return user_data[5]
	def get_right_letter(self, user_id):
		user_data = self.sql_select_user(user_id)
		return user_data[4]	
	def Get_color(self, letter, user_id):
		letters = self.get_letter(user_id)
		right_letters = self.get_right_letter(user_id)
		if letter.lower() in right_letters:
			return VkKeyboardColor.POSITIVE
		elif letter.lower() in letters:
			return VkKeyboardColor.NEGATIVE
		else:
			return VkKeyboardColor.PRIMARY
	def keyboard(self, user_id):
		if self.get_mode(user_id) == 0:
			keyboard = VkKeyboard(one_time=True)
			keyboard.add_button('Погода', color=VkKeyboardColor.POSITIVE)
			keyboard.add_button('Статистика', color=VkKeyboardColor.POSITIVE)
			keyboard.add_line()
			keyboard.add_button('Виселица', color=VkKeyboardColor.NEGATIVE)
		if self.get_mode(user_id) == 1:
			keyboard = VkKeyboard(one_time=True)
			keyboard.add_button('А', color=self.Get_color('А', user_id))
			keyboard.add_button('Б', color=self.Get_color('Б', user_id))
			keyboard.add_button('В', color=self.Get_color('В', user_id))
			keyboard.add_button('Г', color=self.Get_color('Г', user_id))
			keyboard.add_button('Д', color=self.Get_color('Д', user_id))
			keyboard.add_line()
			keyboard.add_button('Е', color=self.Get_color('Е', user_id))
			keyboard.add_button('Ё', color=self.Get_color('Ё', user_id))
			keyboard.add_button('Ж', color=self.Get_color('Ж', user_id))
			keyboard.add_button('З', color=self.Get_color('З', user_id))
			keyboard.add_button('И', color=self.Get_color('И', user_id))
			keyboard.add_line()
			keyboard.add_button('Й', color=self.Get_color('Й', user_id))
			keyboard.add_button('К', color=self.Get_color('К', user_id))
			keyboard.add_button('Л', color=self.Get_color('Л', user_id))
			keyboard.add_button('М', color=self.Get_color('М', user_id))
			keyboard.add_button('Н', color=self.Get_color('Н', user_id))
			keyboard.add_line()
			keyboard.add_button('О', color=self.Get_color('О', user_id))
			keyboard.add_button('П', color=self.Get_color('П', user_id))
			keyboard.add_button('Р', color=self.Get_color('Р', user_id))
			keyboard.add_button('С', color=self.Get_color('С', user_id))
			keyboard.add_button('Т', color=self.Get_color('Т', user_id))
			keyboard.add_line()
			keyboard.add_button('У', color=self.Get_color('У', user_id))
			keyboard.add_button('Ф', color=self.Get_color('Ф', user_id))
			keyboard.add_button('Х', color=self.Get_color('Х', user_id))
			keyboard.add_button('Ц', color=self.Get_color('Ц', user_id))
			keyboard.add_button('Ч', color=self.Get_color('Ч', user_id))
			keyboard.add_line()
			keyboard.add_button('Ш', color=self.Get_color('Ш', user_id))
			keyboard.add_button('Щ', color=self.Get_color('Щ', user_id))
			keyboard.add_button('Ъ', color=self.Get_color('Ъ', user_id))
			keyboard.add_button('Ы', color=self.Get_color('Ы', user_id))
			keyboard.add_button('Ь', color=self.Get_color('Ь', user_id))
			keyboard.add_line()
			keyboard.add_button('Э', color=self.Get_color('Э', user_id))
			keyboard.add_button('Ю', color=self.Get_color('Ю', user_id))
			keyboard.add_button('Я', color=self.Get_color('Я', user_id))
			keyboard.add_line()
			keyboard.add_button('Меню', color=VkKeyboardColor.NEGATIVE)


		keyboard = keyboard.get_keyboard()
		return keyboard
	def sql_connection(self):
		try:

			connection = sqlite3.connect('Database.db')
			cursorObj = connection.cursor()
			try:
				cursorObj.execute('CREATE TABLE employees(user_id integer PRIMARY KEY, \
				mode integer, \
				word text,\
				blank text,\
				right_letter text,\
				letter text,\
				error integer)')
			except:
				print('Base already')
			print("Connection is established: Database is created in memory")
			return connection
		except:

		    print('Error')
	def get_mode(self, user_id):
		user_data = self.sql_select_user(user_id)
		if user_data == 'NULL':
			self.sql_new_user(user_id)
		user_data = self.sql_select_user(user_id)
		return user_data[1]
	def sql_new_user(self, user_id):
		connection = self.sql_connection()
		cursorObj = connection.cursor()
		data = (user_id, 0, '', '', '','', 0)
		cursorObj.execute('INSERT OR IGNORE INTO employees(user_id, mode, word, blank, right_letter,letter, error)\
			VALUES(?, ?, ?, ?, ?, ?, ?)', data)
		connection.commit()
		connection.close()

	def sql_select_user(self, user_id):
		connection = self.sql_connection()
		cursorObj = connection.cursor()
		cursorObj.execute('SELECT user_id,mode,word,blank,right_letter,letter, error FROM employees')
		rows = cursorObj.fetchall()
		data = 'NULL'
		for row in rows:
			if row[0] == user_id:
				data = row
				return data
			else:
				data = 'NULL'
		connection.close()
		print('data = ' + str(data))
		return data

	def get_name_from_vk(self, user_id):
		request = requests.get('https://vk.com/id' + str(user_id))
		bs = bs4.BeautifulSoup(request.text, "html.parser")
		name =self.clear_tags_for_str(bs.findAll('title'))
		name = name.split(' ')
		name = name[0].split('>')
		female = name[1].split('<')
		inicials = {
		'name': name[1],
		'female': female[0]
		}
		return inicials

	def sql_update_word(self, user_id):
		connection = self.sql_connection()
		cursorObj = connection.cursor()
		word = self.random_word()
		data = (word, user_id)
		cursorObj.execute('UPDATE employees SET word = ? WHERE user_id = ?', data)
		connection.commit()
		blank = '*' * len(word)
		data = (blank, user_id)
		cursorObj.execute('UPDATE employees SET blank = ? WHERE user_id = ?', data)
		connection.commit()
		data = ('', user_id)
		cursorObj.execute('UPDATE employees SET letter = ? WHERE user_id = ?', data)
		connection.commit()
		data = (0, user_id)
		cursorObj.execute('UPDATE employees SET error = ? WHERE user_id = ?', data)
		connection.commit()		
		connection.close()

	def sql_update_mode(self, user_id, mode):
		connection = self.sql_connection()
		cursorObj = connection.cursor()
		data = (mode, user_id)
		cursorObj.execute('UPDATE employees SET mode = ? WHERE user_id = ?', data)
		connection.commit()
		connection.close()

	def sql_update(self, user_id, word, blank, right_letter, letter, error):
		connection = self.sql_connection()
		cursorObj = connection.cursor()
		data = (word, user_id)
		cursorObj.execute('UPDATE employees SET word = ? WHERE user_id = ?', data)
		connection.commit()
		data = (blank, user_id)
		cursorObj.execute('UPDATE employees SET blank = ? WHERE user_id = ?', data)
		connection.commit()
		data = (right_letter, user_id)
		cursorObj.execute('UPDATE employees SET right_letter = ? WHERE user_id = ?', data)
		connection.commit()
		data = (letter, user_id)
		cursorObj.execute('UPDATE employees SET letter = ? WHERE user_id = ?', data)
		connection.commit()
		data = (error, user_id)
		cursorObj.execute('UPDATE employees SET error = ? WHERE user_id = ?', data)
		connection.commit()
		print('1')
		connection.close()

	def new_message(self, message):
		user_data = self.sql_select_user(self.USER_ID)
		if user_data[1] == 0 or user_data == 'NULL':
			if message.upper() == self.COMMANDS[0].upper():
				data = self.sql_select_user(self.USER_ID)
				if user_data =='NULL':
					self.sql_new_user(self.USER_ID)
					data = self.sql_select_user(self.USER_ID)
					print('New user')
				#return data
				return f"Привет-привет, {self.USERNAME}!"
		

			elif message.upper() == self.COMMANDS[1].upper():
				try:
					weather = self.getWeather(self.CITY)
					answer = "🌡" + "Температура(в " + str(weather['place']) + ") " + str(weather['temp']) + "℃ " + str(weather['icon']) + " Скорость ветра: " + str(weather['wind']) +" м/с" + " Направление: '" + str(weather['direction']) + "'"
					return str(answer)
				except:
					return 'К сожалению я не знаю ваш город! Пожалуйста для уточнения города напишите "Погода город"(город напишите в иминительном подеже)"!'
			elif message.upper().find('ПОГОДА ') != -1:
				try:
					city = message.split(' ')
					weather = self.getWeather(city[1])
					answer = "🌡" + "Температура(в " + str(weather['place']) + ") " + str(weather['temp']) + "℃ " + str(weather['icon']) + " Скорость ветра: " + str(weather['wind']) +" м/с" + " Направление: '" + str(weather['direction']) + "'"
					return answer
				except:
					return 'К сожалению я не знаю ваш город! Пожалуйста для уточнения города напишите "Погода город"(город напишите в иминительном подеже)"!'
			elif message.upper() == self.COMMANDS[2].upper():
				delta = datetime.timedelta(hours=4, minutes=0) 
				# Присваиваем дату и время переменной «t»
				t = (datetime.datetime.now(datetime.timezone.utc) + delta) 
				# текущее время
				nowtime = t.strftime("%H:%M") 
				return nowtime
			elif message.upper() == self.COMMANDS[3].upper():
				return f"Прощай, {self.USERNAME} ("
			elif message.upper() == self.COMMANDS[4].upper():
				return 'Вот мои команды:\n "Погода": показывает погоду в вашем городе,\n "Статистика": Выводит статистику заболеваемости короновируса в РФ,\n "Виселица": Мини-игра угадай слово.'
			elif message.upper() == self.COMMANDS[5].upper():
				return self.get_covid_statistic()
			elif message.upper() == self.COMMANDS[6].upper():
				# return f"Привет, {self.USERNAME}! Чтобы узнать что я могу напиши 'команды'"
				data = self.sql_select_user(self.USER_ID)
				if data =='NULL':
					self.sql_new_user(self.USER_ID)
					data = self.sql_select_user(self.USER_ID)
				return f"Привет, {self.USERNAME}! Чтобы узнать что я могу напиши 'команды'"
			elif message.upper() == self.COMMANDS[7].upper():
				self.sql_update_mode(self.USER_ID, 1)
				self.sql_update_word(self.USER_ID)
				return self.start_game(self.USER_ID)
			else:
				return 'Я не знаю такой команды. Чтобы узнать мои способности напиши "команды"!'
		else:
			return self.game(self.USER_ID, message)
			
	def blank(self, word, right_letter, blank):
		for i in range(len(word)):
				if word[i] in right_letter:
					blank = blank[:i] + word[i] + blank[i+1:]
		return blank

	def start_game(self, user_id):
		user_data = self.sql_select_user(self.USER_ID)
		message = '''Игра начинается:
		Ваше слово состоит из ''' + str(len(user_data[2])) + ''' букв,
		Слово: ''' + str(user_data[3]) + '''
		Ваша буква:'''
		return message

	def game(self, user_id, message):
		
		if message in self.alphabet:
			user_data = self.sql_select_user(user_id)
			if user_data == 'NULL':
				self.sql_new_user(user_id)
				user_data = self.sql_select_user(user_id)
			word = user_data[2]
			blank = user_data[3]
			right_letter = user_data[4]
			letter = user_data[5]
			error = int(user_data[6])
			message = message.lower()
			if message in letter:
				return 'Вы уже вводили эту букву!'
			else:
				if message in word:
					letter += message
					right_letter += message
					blank = self.blank(word, right_letter, blank)
					self.sql_update(user_id, word, blank, right_letter, letter, error)
					answer = '''Буква ''' + message + ''' есть в слове!
					Слово: ''' + blank + ''' 
					''' + config.vis[len(config.vis) - 1 - error]
				else:
					error += 1
					letter += message
					self.sql_update(user_id, word, blank, right_letter, letter, error)
					answer = '''Буквы ''' + message + ''' нет в слове!
					слово:''' + blank +''' 
					''' + config.vis[len(config.vis) - 1 - error]
			if word == blank:
				word = ''
				blank = ''
				right_letter = ''
				letter = ''
				error = 0
				answer = 'Вы победили! Для повторной игры напишите "Виселица"'
				self.sql_update(user_id, word, blank, right_letter, letter, error)
				self.sql_update_mode(user_id, 0)
			if error > len(config.vis) - 2:
					
					
				blank = ''
				right_letter = ''
				letter = ''
				error = 0
				answer =  '''Вы проиграли! 
				Слово было: ''' + word
				word = ''
				self.sql_update(user_id, word, blank, right_letter, letter, error)
				self.sql_update_mode(user_id, 0)
			
		
		elif message.upper() == 'МЕНЮ':
			user_data = self.sql_select_user(user_id)
			word = ''
			blank = ''
			right_letter = ''
			letter = ''
			error = 0
			self.sql_update(user_id, word, blank, right_letter, letter, error)
			self.sql_update_mode(user_id, 0)
			return '''Игра окончена!
			Ваше слово было: ''' + user_data[2]
		else:
			return 'Вы ввели не букву! Если хотите выйти напишите: "Меню"'
	
		
		return answer

	def clear_tags_for_str(self, line):
		not_skip = True
		result = ''
		# line = '<title>Рафаэль Хайруллов | ВКонтакте</title>'
		for i in line:
			if not_skip:
				if i == "<":
					not_skip = False
				else:
					result += str(i)
			else:
				if i == ">":
					not_skip = True
		return(result)

	def get_user_city(self, user_id):
		try:
			request = requests.get('https://vk.com/id' + str(user_id))
			bs = bs4.BeautifulSoup(request.text, "html.parser")
			info = self.clear_tags_for_str(bs.findAll("div", {"class": "OwnerInfo__rowCenter"})[0])
			city = info.split(':')
			city = city[1].split(' ')
			return city[1]
		except:
			return 'error'

	def getWeather(self, place):
		try:
			owm = pyowm.OWM(config.OWM_TOKEN, language = 'ru')
			#город указания температуры
			
			observation = owm.weather_at_place(place)
			#получение данных о погоде
			w = observation.get_weather()
			#присваеваем температуру переменной temp
			temp = w.get_temperature('celsius')["temp"]
			wind = w.get_wind('meters_sec')['speed']
			deg = w.get_wind('meters_sec')['deg']
			direction = 'error'
			if (deg >= 0 and deg <= 15) or (deg >= 345 and deg <= 360): # deg == 0 or deg == 360
				direction = "С"
			elif deg > 15 and deg < 75: #deg > 0 and deg < 90
				direction = "СВ"
			elif deg >= 75 and deg <= 105: #deg == 90
				direction = "В"
			elif deg > 105 and deg < 165: #deg > 90 and deg < 180
				direction = "ЮВ"
			elif deg >= 165 and deg <= 195: #deg == 180
				direction = 'Ю'
			elif deg > 195 and deg < 255: #deg > 180 and deg < 270
				direction = 'ЮЗ'
			elif deg >= 255 and deg <= 285: #deg == 270
				direction = 'З'
			elif deg > 285 and deg < 345: #deg > 270 and deg < 360
				direction = "СЗ"
			#получаем код состояния погоды
			code = w.get_weather_code()
			#Присвоение иконки
			icon = ' error(No data)'
			if code >= 200 and code < 300:#гроза
				icon = '⛈'
			elif code >= 300 and code < 400:#Изморось 
				icon = '❄'
			elif code >= 500 and code < 600:#снег
				icon = '🌧'
			elif code >= 600 and code < 700:#Дождь
				icon = '🌨'
			elif code == 800:#Ясно
				icon = '☀'
			elif code >= 801 and code < 900:#Облачно
				icon = '⛅'	
			weather = {
				'place': place,
				'temp': temp,
				'wind': wind,
				'direction': direction,
				'icon': icon
			}
			return weather
		except:
			return 'Произошла ошибка или у вас скрыт город. Пожалуйста для уточнения города напишите "Погода город"(город напишите в иминительном подеже)"!'
	
	def get_covid_statistic(self):
		request = requests.get('https://стопкоронавирус.рф')
		bs = bs4.BeautifulSoup(request.text, "html.parser")
		name =str(bs.findAll("div", {"class": "cv-countdown__item-value _accent"}))
		line = name.split('>')
		line1 = line[2].split('<')
		line2= line[6].split('<')

		vsegocabolevchih = line1[0]
		zaden = line2[0]
	
		name =str(bs.findAll("div", {"class": "cv-countdown__item-value"}))
		line = name.split('>')
		line3 = line[18].split('<')
		death = line3[0]
		line4 = line[14].split('<')
		vizdorovelo = line4[0]
		return f"Статистика в России. Выявлено заболевших: {vsegocabolevchih}, из них за сутки: {zaden}, смертей: {death}, выздоровело: {vizdorovelo}."




'''
def main():
	vk_session = vk_api.VkApi(token=config.VK_TOKEN)
	longpoll = VkBotLongPoll(vk_session, '173391069')
	lsvk = vk_session.get_api()
	print('True')
	for event in longpoll.listen():

		if event.type == VkBotEventType.MESSAGE_NEW:
			print('Новое сообщение:')
			print('Для меня от: ', end='')
			print(event.obj.from_id)
			print('Текст:', event.obj.text)
			print()
			if event.from_user:
				request = event.obj.text
				if request == 'Привет':
					lsvk.messages.send(
                    user_id = event.obj.user_id,
                    message = 'Привет)',
                    random_id = get_random_id(),
                    peer_id = event.obj.peer_id
                    )
				elif request == 'Пока':
					lsvk.messages.send(
						user_id = event.obj.user_id,
						message = 'Пока((',
						random_id = get_random_id(),
						peer_id = event.obj.peer_id
						)
				elif request == 'команды' or request == 'Команды':
					lsvk.messages.send(
						user_id = event.obj.user_id,
						message = 'Вот мои команды:' + str(COMMANDS) ,
						random_id = get_random_id(),
						peer_id = event.obj.peer_id
						)
				else:
					lsvk.messages.send(
						user_id = event.obj.user_id,
						message = 'Я не знаю такой команды. Чтобы узнать мои способности напиши "команды"!',
						random_id = get_random_id(),
						peer_id = event.obj.peer_id
						)

		elif event.type == VkBotEventType.MESSAGE_REPLY:
			print('Новое сообщение:')
			print('От меня для: ', end='')
			print(event.obj.peer_id)
			print('Текст:', event.obj.text)
			print()
		elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
			print('Печатает ', end='')
			print(event.obj.from_id, end=' ')
			print('для ', end='')
			print(event.obj.to_id)
			print()
		elif event.type == VkBotEventType.GROUP_JOIN:
			print(event.obj.user_id, end=' ')
			print('Вступил в группу!')
			print()

		elif event.type == VkBotEventType.GROUP_LEAVE:
			print(event.obj.user_id, end=' ')
			print('Покинул группу!')
			print()
		else:
			print(event.type)
			print()


if __name__ == '__main__':
    main()
'''