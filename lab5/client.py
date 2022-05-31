from day import Day
from event import Event
from notebook import Notebook
import pymqi

def decodeListOfDays(days):
    for day in days:
        element = day.split(',')
        if len(element) == 2:
            print("Day id: " + element[0] + ", date: " + element[1])

def decodeListOfEvents(events):
    for event in events:
        element = event.split(',')
        if len(element) == 5:
            print("Event id: " + element[0] + ", Day id: " + element[1] + ", name: " + element[2] +
							", time: " + element[3] + ", mandatory: " + element[4])

def scenario():
    putq.put('1|0|01.01.2022')
    putq.put('1|1|02.02.2022')
    putq.put('3|0|0|party|9:00|True')
    putq.put('3|1|1|pre-party|9:00|False')
    putq.put('3|2|1|party|10:00|True')
    putq.put('7')
    putq.put('4|2')
    putq.put('7')
    putq.put('2|0')
    putq.put('2|1')
    putq.put('7')


def readResult():
    try:
        result = getq.get(gmo)
        result = result.split('|')
        print('Correct') if int(result[0]) else print('Failed')
        if len(result) > 1:
            decodeListOfEvents(result[1:])
        return True
    except:
        return False


if __name__=='__main__':
    gmo = pymqi.GMO()
    gmo.Options = pymqi.CMQC.MQGMO_WAIT | pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING
    gmo.WaitInterval = 3000

    qmgr = pymqi.QueueManager('QM1')
    getq = pymqi.Queue(qmgr, 'SRV.Q')
    putq = pymqi.Queue(qmgr, 'CL.Q')

    com = input('1.Відправити запит 2.Отримати результат')
    if com == 1:
        scenario()
    elif com == 2:
        while(readResult()):
            pass
    else:
        print('Error')
        exit()
