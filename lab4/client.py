import Pyro4
from day import Day
from event import Event
from notebook import Notebook
import socket

def decodeListOfDays(days):
    days = days.split('|')
    for day in days:
        element = day.split(',')
        if len(element) == 2:
            print("Day id: " + element[0] + ", date: " + element[1])

def decodeListOfEvents(events):
    events = events.split('|')
    for event in events:
        element = event.split(',')
        if len(element) == 5:
            print("Event id: " + element[0] + ", Day id: " + element[1] + ", name: " + element[2] +
							", time: " + element[3] + ", mandatory: " + element[4])

def scenario():
    ns = Pyro4.locateNS()
    uri = ns.lookup('notebook')
    notebook = Pyro4.Proxy(uri)
    notebook.CreateDay('01.01.2022')
    notebook.CreateDay('03.03.2022')
    notebook.CreateEvent(0, 'birthday', '9:23', False)
    notebook.CreateEvent( 1, 'pre-part', '11:00', False)
    notebook.CreateEvent(1, 'party', '12:00', True)
    decodeListOfDays(notebook.ListOfDays())
    decodeListOfEvents(notebook.ListOfEvents())
    print('===========================================================')
    print('Number of events in day ' + '1:' + str(notebook.NumberOfEventsInDay(1)))
    decodeListOfEvents(notebook.ListOfEventsInDay(1))
    print('===========================================================')
    notebook.EventChangeDate(2,0)
    decodeListOfDays(notebook.ListOfDays())
    decodeListOfEvents(notebook.ListOfEvents())

    print('===========================================================')

    notebook.DeleteEvent(2)
    decodeListOfEvents(notebook.ListOfEvents())
    print('===========================================================')

    notebook.DeleteDay(0)
    notebook.DeleteDay(1)
    decodeListOfDays(notebook.ListOfDays())
    decodeListOfEvents(notebook.ListOfEvents())

if __name__=='__main__':
    scenario()