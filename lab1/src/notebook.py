from lxml import etree
import xml.etree.ElementTree as ET

class Day:
    def __init__(self, id, date):
        self.id = id
        self.date = date
        self.events = []

class Event:
    def __init__(self, id, name, time, mandatory):
        self.id = id
        self.name = name
        self.time = time
        self.mandatory = mandatory

class Notebook:
    days = []

    def __init__(self, filepath):
        self.filepath = filepath
        parser = etree.XMLParser(dtd_validation=True)
        tree = ET.parse(filepath, parser)
        root = tree.getroot()
        for day in root:
            id = day.attrib['id']
            self.days.append(Day(id, day.attrib['date']))
            for event in day:
                self.days[len(self.days) - 1].events.append(Event(event.attrib['id'], event.attrib['name'], event.attrib['time'], bool(event.attrib['mandatory'])))

    def getDay(self, id):
        try:
            for day in self.days:
                if day.id == id:
                    return day
            raise Exception('There is no day with this id')
        except Exception as error:
            print(error)

    def getDayInd(self, ind):
        try:
            if ind >= len(self.days):
                raise Exception('The number goes beyond the indexes of the array')
            return self.days[ind]
        except Exception as error:
            print(error)

    def countDays(self):
        return len(self.days)

    def saveToFile(self, filename):
        root = ET.Element('notebook')
        tree = ET.ElementTree(root)
        for day in self.days:
            dayiter = ET.SubElement(root, 'day')
            dayiter.set('id', day.id)
            dayiter.set('date', day.date)
            for event in day.events:
                eventiter = ET.SubElement(dayiter, 'event')
                eventiter.set('id', event.id)
                eventiter.set('time', event.time)
                eventiter.set('name', event.name)
                eventiter.set('mandatory', str(event.mandatory))
        with open(filename, 'wb') as f:
            tree.write(f, encoding='utf-8')

    def addDay(self, id, date):
        try:
            for day in self.days:
                if day.id == id:
                    raise Exception('There is day with that id')
            self.days.append(Day(id, date))
        except Exception as error:
            print(error)

    def deleteDay(self, id):
        try:
            find = False
            i = 0
            while i < len(self.days):
                if self.days[i].id == id:
                    self.days.pop(i)
                    find = True
                else:
                    i += 1
            if not find:
                raise Exception('There isn`t day with that id')
        except Exception as error:
            print(error)

    def addEvent(self, id, name, time, mandatory, dayId):
        try:
            for i in range(len(self.days)):
                if dayId == self.days[i].id:
                    self.days[i].events.append(Event(id, name, time, mandatory))
                    return
            raise Exception('There isn`t day with that id')
        except Exception as error:
            print(error)

    def deleteEvent(self, id):
        try:
            for j in range(len(self.days)):
                for i in range(len(self.days[j].events)):
                    if self.days[j].events[i].id == id:
                        self.days[j].events.pop(i)
                        return
            raise Exception('There isn`t event with that id')
        except Exception as error:
            print(error)

    def editDay(self, id):
        try:
            for i in range(len(self.days)):
                if self.days[i].id == id:
                    print('Print new date:')
                    date = input()
                    self.days[i].date = date
                    return
            raise Exception('There is no day with this id')
        except Exception as error:
            print(error)

    def editEvent(self, id):
        try:
            for i in range(len(self.days)):
                for j in range(len(self.days[i].events)):
                    if self.days[i].events[j].id == id:
                        print('1.Edit name\n 2.Edit time\n 3.Edit mandatory\n ')
                        command = int(input())
                        if command == 1:
                            self.days[i].events[j].name = input()
                        elif command == 2:
                            self.days[i].events[j].time = input()
                        elif command == 3:
                            self.days[i].events[j].mandatory = bool(input())
                        else:
                            print("Unknown command")
                        return
        except Exception as error:
            print(error)

    def __str__(self):
        for day in self.days:
            print('Id: ', day.id)
            print('Date: ', day.date)
            for event in day.events:
                print('    Id: ', event.id)
                print('    Name: ', event.name)
                print('    Time: ', event.time)
                print('    Mandatory: ', event.mandatory)
            print('==================================')


if __name__ == '__main__':
    print('Choose scenario(1-3)')
    scenario = int(input())
    if scenario == 1:
        notebook = Notebook('../data/notebook.xml')
        notebook.addDay('123', '2024-08-02')
        notebook.addEvent('aaa', 'birthday', '17:02:34', False, '123')
        notebook.addEvent('bbb', 'pre-paty', '14:02:34', False, '123')
        notebook.saveToFile('notebook.xml')
    elif scenario == 2:
        notebook = Notebook('../data/notebook.xml')
        notebook.deleteEvent('er84e9')
        notebook.deleteDay('ad896')
        notebook.saveToFile('notebook.xml')
    elif scenario == 3:
        notebook = Notebook('../data/notebook.xml')
        notebook.editDay('ad896')
        notebook.editEvent('er84e9')
        notebook.saveToFile('notebook.xml')
