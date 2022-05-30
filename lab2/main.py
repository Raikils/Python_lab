from notebook import Notebook
from day import Day
from event import Event

def scenario():
    notebook = Notebook()
    notebook.CreateDay(Day(0, '01.01.2022'))
    notebook.CreateDay(Day(1, '03.03.2022'))
    notebook.CreateEvent(Event(0, 0, 'birthday', '9:23', False))
    notebook.CreateEvent(Event(1, 1, 'pre-part', '11:00', False))
    notebook.CreateEvent(Event(2, 1, 'party', '12:00', True))
    notebook.PrintData()
    print('===========================================================')

    notebook.EditDay(0)
    notebook.EditEvent(1)
    notebook.EditEvent(2)
    notebook.PrintData()
    print('===========================================================')

    notebook.PrintListOfEventsInDay(1)

    print('===========================================================')

    notebook.DeleteEvent(2)
    notebook.PrintData()
    print('===========================================================')

    notebook.DeleteDay(0)
    notebook.DeleteDay(1)
    notebook.PrintData()


if __name__=='__main__':
    scenario()
