import MySQLdb
from day import Day
from event import Event

class Notebook:
	def __init__(self):
		self.mDays = dict()
		self.mEvents = dict()
		self.LoadDataOrNo = False

		url = "localhost"
		databaseName = "notebook"
		self.db = MySQLdb.connect(url, "root", '1234', databaseName)
		self.cursor = self.db.cursor()
		self.LoadData()

	def Clean(self):
		self.mDays = dict()
		self.mEvents = dict()

	def PrintData(self):

		try:
			sql = "SELECT idDay, dateDay FROM Days"
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			for row in results:
				idDay = row[0]
				dateDay = row[1]
				print("Day id: " + str(idDay) + ", date: " + dateDay)

			sql = "SELECT * FROM Events"
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			for row in results:
				idEvent = row[0]
				idDay = row[1]
				nameEvent = row[2]
				timeEvent = row[3]
				mandatoryEvent = row[4]
				print("Event id: " + str(idEvent) + ", Event id: " + str(idDay) + ", name: " + nameEvent +
							", time: " + str(timeEvent) + ", mandatory: " + str(mandatoryEvent))

		except:
			print("ПОМИЛКА при отриманні списку ")


	def LoadData(self):
		self.Clean()

		sql = "SELECT * FROM Days"
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		for row in results:
			idDay = row[0]
			dateDay = row[1]
			day = Day(idDay, dateDay)
			self.mDays[idDay] = day

		sql = "SELECT * FROM Events"
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		for row in results:
			idEvent = row[0]
			idDay = row[1]
			nameEvent = row[2]
			timeEvent = row[3]
			mandatoryEvent = row[4]
			event = Event(idEvent, idDay, nameEvent, timeEvent, mandatoryEvent)
			self.mEvents[idEvent] = event

		self.LoadDataOrNo = True
		self.PrintData()
		return 0


	def CreateDay(self, day):
		if self.LoadDataOrNo == False:
			self.LoadData()
		if len(self.mDays) == 0:
			key = 0
		else:
			key = max(self.mDays.keys()) + 1
		day.id = key
		self.mDays[key] = day

		sql = "INSERT INTO Days (idDay, dateDay) VALUES (%d, '%s')" % (day.id, day.date)
		try:
			self.cursor.execute(sql)
			self.db.commit()
			print("День %s успішно додан!" % day.date)
			return True
		except:
			print("ПОМИЛКА! День %s не додан !" % day.date)
			self.db.rollback()
			return False


	def CreateEvent(self, event):
		if self.LoadDataOrNo == False:
			self.LoadData()
		if len(self.mEvents) == 0:
			key = 0
		else:
			key = max(self.mEvents.keys()) + 1
		event.id = key
		self.mEvents[key] = event

		sql = "INSERT INTO Events (idEvent, idDay, nameEvent, timeEvent, mandatoryEvent) VALUES (%d, %d, '%s', '%s', %i)" % (
			event.id, event.idDay, event.name, event.time, event.mandatory)
		try:
			self.cursor.execute(sql)
			self.db.commit()
			print("Івент %s успішно доданий!" % event.name)
			return True
		except:
			print("ПОМИЛКА! Івент %s не доданий!" % event.name)
			self.db.rollback()
			return False

	def EditDay(self, dayId):
		if self.LoadDataOrNo == False:
			self.LoadData()
		if(self.SearchDay(dayId, False)):
			day_copy = self.mDays[dayId]
			print("Введіть нову дату (dayDate): ")
			dayDate = input()
			day_copy.date = dayDate
			self.mDays[dayId] = day_copy

			sql = "UPDATE Days SET dateDay = '" + dayDate + "'"+ \
				  " WHERE idDay = " + str(dayId)
			try:
				self.cursor.execute(sql)
				self.db.commit()
				print("День id = %d успішно відредагований!" % dayId)
				return True
			except:
				print("ПОМИЛКА! День id = %d не відредагований!" % dayId)
				self.db.rollback()
				return False


	def EditEvent(self, eventId):
		if self.LoadDataOrNo == False:
			self.LoadData()
		if(self.SearchEvent(eventId, False)):
			event_copy = self.mEvents[eventId]
			print("Що змінити? \n" +
						"1 - название івенту \n" +
						"2 - час івенту \n" +
						"3 - оплату івенту")

			sql = "UPDATE Events SET "
			command = int(input())
			if command == 1:
				eventName = input("Введіть нове ім'я:")
				event_copy.name = eventName
				sql = sql + "nameEvent = '" + eventName + "'"
			elif command == 2:
				eventTime = input("Введіть новий час:")
				event_copy.time = eventTime
				sql = sql + "timeEvent = '" + eventTime + "'"
			elif command == 3:
				eventmandatory = input("Івент платний:")
				event_copy.mandatory = eventmandatory
				sql = sql + "mandatoryEvent = '" + str(eventmandatory) + "'"
			else :
				print("Unknown command")
				return
			sql = sql + " WHERE idEvent = " + str(eventId)
			self.mEvents[eventId] = event_copy
			try:
				self.cursor.execute(sql)
				self.db.commit()
				print("Івент id = %d успішно відредагований!" % eventId)
				return True
			except:
				print("ПОМИЛКА! Івент id = %d не відредагований!" % eventId)
				self.db.rollback()
				return False


	def DeleteDay(self, dayId):
		deldate = self.mDays[dayId].date
		eventIdSet = set()
		for eventId in self.mEvents:
			if self.mEvents[eventId].idDay == dayId:
				eventIdSet.add(eventId)

		for eventId in eventIdSet:
			self.DeleteEvent(self.mEvents[eventId].id)
		del self.mDays[dayId]


		if (self.SearchDay(dayId, False)):
			sql = "DELETE FROM Days WHERE idDay = %d" % dayId
			try:
				self.cursor.execute(sql)
				self.db.commit()
				print("День %s успішно видалений!" % deldate)
				return True
			except:
				print("ПОМИЛКА при видаленні дня %s" % deldate)
				self.db.rollback()
				return False


	def DeleteEvent(self, eventId):
		delname = self.mEvents[eventId].name

		if(self.SearchEvent(eventId, False)):
			sql = "DELETE FROM Events WHERE idEvent = %d" % eventId
			try:
				self.cursor.execute(sql)
				self.db.commit()
				del self.mEvents[eventId]
				print("Івент %s успішно видалений!" % delname)
				return True
			except:
				print("ПОМИЛКА при видаленні івенту %s" % delname)
				self.db.rollback()
				return False


	def SearchDay(self, dayId, boolPrintOrNo):
		try:
			sql = "SELECT * FROM Days WHERE idDay = %d" % dayId
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			if len(results) == 0:
				print("Немає дня з таким id = " + str(dayId))
			for row in results:
				idDay = row[0]
				dateDay = row[1]
				if boolPrintOrNo:
					print("Day id: " + str(idDay) + ", date: " + dateDay)
				return True
		except:
			print("ПОМИЛКА при пошуку дня %d" % dayId)
			self.db.rollback()
			return False

	def SearchEvent(self, eventId, boolPrintOrNo):
		try:
			sql = "SELECT * FROM Events WHERE idEvent = %d" % eventId
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			if len(results) == 0:
				print("Немає івенту з таким id = " + str(eventId))
			for row in results:
				idEvent = row[0]
				idDay = row[1]
				nameEvent = row[2]
				timeEvent = row[3]
				mandatoryEvent = row[4]
				if boolPrintOrNo:
					print("Event id: " + str(idEvent) + ", Day id: " + str(idDay) + ", name: " + nameEvent +
							", time: " + str(timeEvent) + ", mandatory: " + str(mandatoryEvent))
				return True
		except:
			print("ПОМИЛКА при івенту продукту %d" % eventId)
			self.db.rollback()
			return False


	def PrintListOfDays(self):
		sql = "SELECT idDay, dateDay FROM Days"
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		if len(results) == 0:
			print("Список пуст")

		for row in results:
			idDay = row[0]
			dateDay = row[1]
			print("Day id: " + str(idDay) + ", date: " + dateDay)
		return True

	def PrintListOfEventsInDay(self, dayId):

		if self.SearchDay(dayId, True):
			sql = "SELECT * FROM Events WHERE idDay = %d" % dayId
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			if len(results) == 0:
				print("Список пуст")
			for row in results:
				idEvent = row[0]
				idDay = row[1]
				nameEvent = row[2]
				timeEvent = row[3]
				mandatoryEvent = row[4]
				print("	Event id: " + str(idEvent) + ", Day id: " + str(idDay) + ", name: " + nameEvent +
							", time: " + str(timeEvent) + ", mandatory: " + str(mandatoryEvent))
		return True