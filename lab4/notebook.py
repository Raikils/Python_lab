import MySQLdb
import Pyro4
from day import Day
from event import Event

@Pyro4.expose
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

	@Pyro4.expose
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
				print("Event id: " + str(idEvent) + ", Day id: " + str(idDay) + ", name: " + nameEvent +
							", time: " + str(timeEvent) + ", mandatory: " + str(mandatoryEvent))

		except:
			print("ПОМИЛКА при отриманні списку ")

	@Pyro4.expose
	def LoadData(self):
		self.Clean()

		sql = "SELECT * FROM Days"
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		for row in results:
			idDay = int(row[0])
			dateDay = row[1]
			day = Day(idDay, dateDay)
			self.mDays[idDay] = day

		sql = "SELECT * FROM Events"
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		for row in results:
			idEvent = int(row[0])
			idDay = int(row[1])
			nameEvent = row[2]
			timeEvent = row[3]
			mandatoryEvent = row[4]
			event = Event(idEvent, idDay, nameEvent, timeEvent, mandatoryEvent)
			self.mEvents[idEvent] = event

		self.LoadDataOrNo = True
		self.PrintData()
		return 0

	@Pyro4.expose
	def CreateDay(self, dataDay):
		if self.LoadDataOrNo == False:
			self.LoadData()
		if len(self.mDays) == 0:
			key = 0
		else:
			key = max(self.mDays.keys()) + 1
		id = key
		self.mDays[key] = Day(id, dataDay)

		sql = "INSERT INTO Days (idDay, dateDay) VALUES (%d, '%s')" % (id, dataDay)
		try:
			self.cursor.execute(sql)
			self.db.commit()
			print("День %s успішно додан!" % dataDay)
			return True
		except:
			print("ПОМИЛКА! День %s не додан !" % dataDay)
			self.db.rollback()
			return False

	@Pyro4.expose
	def CreateEvent(self, idDay, nameEvent, timeEvent, mandatoryEvent):
		if self.LoadDataOrNo == False:
			self.LoadData()
		if len(self.mEvents) == 0:
			key = 0
		else:
			key = max(self.mEvents.keys()) + 1
		id = key
		self.mEvents[key] = Event(id, int(idDay), nameEvent, timeEvent, mandatoryEvent)

		sql = "INSERT INTO Events (idEvent, idDay, nameEvent, timeEvent, mandatoryEvent) VALUES (%d, %d, '%s', '%s', %i)" % (
			id, int(idDay), nameEvent, timeEvent, bool(mandatoryEvent))
		try:
			self.cursor.execute(sql)
			self.db.commit()
			print("Івент %s успішно доданий!" % nameEvent)
			return True
		except:
			print("ПОМИЛКА! Івент %s не доданий!" % nameEvent)
			self.db.rollback()
			return False

	@Pyro4.expose
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

	@Pyro4.expose
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

	@Pyro4.expose
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

	@Pyro4.expose
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

	@Pyro4.expose
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

	@Pyro4.expose
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
			print("ПОМИЛКА при івенту %d" % eventId)
			self.db.rollback()
			return False

	@Pyro4.expose
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

	@Pyro4.expose
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

	@Pyro4.expose
	def NumberOfEventsInDay(self, dayId):
		result = 0
		for event in self.mEvents.values():
			if event.idDay == dayId:
				result += 1
		return result

	@Pyro4.expose
	def ListOfEvents(self):
		result = ''
		for event in self.mEvents.values():
			result += str(event.id) + ',' + str(event.idDay) + ',' + str(event.name) + ',' + str(event.time) + ',' + str(event.mandatory) + '|'
		if not len(result):
			result = result[:-1]
		return result

	@Pyro4.expose
	def ListOfDays(self):
		result = ''
		for day in self.mDays.values():
			result += str(day.id) + ',' + str(day.date) + '|'
		if not len(result):
			result = result[:-1]
		return result

	@Pyro4.expose
	def ListOfEventsInDay(self, dayID):
		result = ''
		for event in self.mEvents.values():
			if event.idDay == dayID:
				result += str(event.id) + ',' + str(event.idDay) + ',' + str(event.name) + ',' + str(event.time) + ',' + str(event.mandatory) + '|'
		if not len(result):
			result = result[:-1]
		return result

	def EventChangeDate(self, eventId, dayId):
		try:
			sql = "SELECT * FROM Events WHERE idEvent = %d" % int(eventId)
			self.cursor.execute(sql)
			event = self.cursor.fetchall()
			if len(event) == 0:
				print("Немає івенту з таким id = " + str(eventId))
				return
			sql = "SELECT * FROM Days WHERE idDay = %d" % dayId
			self.cursor.execute(sql)
			day = self.cursor.fetchall()
			if len(day) == 0:
				print("Немає дня з таким id = " + str(dayId))
				return
			self.DeleteEvent(int(event[0][0]))
			self.CreateEvent(int(dayId), event[0][2], event[0][3], event[0][4])
		except:
			print("ПОМИЛКА при івенту %d" % eventId)
			self.db.rollback()
			return False