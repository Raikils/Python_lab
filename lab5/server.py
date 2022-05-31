from day import Day
from event import Event
from notebook import Notebook
import pymqi

def executeCommand(received):
    reply = ""
    print(received)
    command = int(received[0])
    if command == 1:
        result = notebook.CreateDay(Day(int(received[1]), received[2]))
        if result:
            reply = '1'
        else:
            reply = '0'
    elif command == 2:
        result = notebook.DeleteDay(int(received[1]))
        if result:
            reply = '1'
        else:
            reply = '0'
    elif command == 3:
        result = notebook.CreateEvent(
            Event(int(received[1]), int(received[2]), received[3], received[4], bool(received[5])))
        if result:
            reply = '1'
        else:
            reply = '0'
    elif command == 4:
        result = notebook.DeleteEvent(int(received[1]))
        if result:
            reply = '1'
        else:
            reply = '0'
    elif command == 5:
        event = notebook.mEvents[int(received[1])]
        result1 = notebook.DeleteEvent(int(received[1]))
        event.idDay = int(received[2])
        result2 = notebook.CreateEvent(event)
        if result1 and result2:
            reply = '1'
        else:
            reply = '0'
    elif command == 6:
        number = notebook.NumberOfEventsInDay(int(received[1]))
        reply = '1|' + str(number)
    elif command == 7:
        reply = '1|' + notebook.ListOfEvents()
    elif command == 8:
        reply = '1|' + notebook.ListOfDays()
    elif command == 9:
        reply = '1|' + notebook.ListOfEventsInDay(int(received[1]))
    elif command == 10:
        exit()
    else:
        reply = "Unknown command"
    return reply

def processQuery():
    try:
        received = getq.get(gmo)
        reply = executeCommand(received)
        putq.put(reply)
        return True
    except:
        return False


if __name__ == '__main__':
    gmo = pymqi.GMO()
    gmo.Options = pymqi.CMQC.MQGMO_WAIT | pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING
    gmo.WaitInterval = 3000
    qmgr = pymqi.QueueManager('QM1')
    putq = pymqi.Queue(qmgr, 'SRV.Q')
    getq = pymqi.Queue(qmgr, 'CL.Q')

    notebook = Notebook()

    while (processQuery()):
        pass
    putq.close()
    getq.close()