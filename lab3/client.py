from day import Day
from event import Event
from notebook import Notebook
import socket

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
    s = socket.socket()
    host = socket.gethostname()
    port = 12345
    s.connect((host, port))

    command = '1|0|01.01.2022'
    s.send(command.encode())
    result = s.recv(1024).decode().split('|')
    print('Correct') if int(result[0]) else print('Failed')

    command = '1|1|02.02.2022'
    s.send(command.encode())
    result = s.recv(1024).decode().split('|')
    print('Correct') if int(result[0]) else print('Failed')

    command = '3|0|0|party|9:00|True'
    s.send(command.encode())
    result = s.recv(1024).decode().split('|')
    print('Correct') if int(result[0]) else print('Failed')

    command = '3|1|1|pre-party|9:00|False'
    s.send(command.encode())
    result = s.recv(1024).decode().split('|')
    print('Correct') if int(result[0]) else print('Failed')

    command = '3|2|1|party|10:00|True'
    s.send(command.encode())
    result = s.recv(1024).decode().split('|')
    print('Correct') if int(result[0]) else print('Failed')

    command = '8'
    s.send(command.encode())
    result = s.recv(1024).decode().split('|')
    print('Correct') if int(result[0]) else print('Failed')
    decodeListOfDays(result[1:])

    command = '7'
    s.send(command.encode())
    result = s.recv(1024).decode().split('|')
    print('Correct') if int(result[0]) else print('Failed')
    decodeListOfEvents(result[1:])

    command = '6|1'
    s.send(command.encode())
    result = s.recv(1024).decode().split('|')
    print('Correct') if int(result[0]) else print('Failed')
    print('Number of events in day ' + '1:' + result[1])

    command = '9|1'
    s.send(command.encode())
    result = s.recv(1024).decode().split('|')
    print('Correct') if int(result[0]) else print('Failed')
    decodeListOfEvents(result[1:])

    command = '5|2|0'
    s.send(command.encode())
    result = s.recv(1024).decode().split('|')
    print('Correct') if int(result[0]) else print('Failed')

    command = '7'
    s.send(command.encode())
    result = s.recv(1024).decode().split('|')
    print('Correct') if int(result[0]) else print('Failed')
    decodeListOfEvents(result[1:])

    command = '2|0'
    s.send(command.encode())
    result = s.recv(1024).decode().split('|')
    print('Correct') if int(result[0]) else print('Failed')

    command = '2|1'
    s.send(command.encode())
    result = s.recv(1024).decode().split('|')
    print('Correct') if int(result[0]) else print('Failed')

    command = '8'
    s.send(command.encode())
    result = s.recv(1024).decode().split('|')
    print('Correct') if int(result[0]) else print('Failed')
    decodeListOfDays(result[1:])

    command = '7'
    s.send(command.encode())
    result = s.recv(1024).decode().split('|')
    print('Correct') if int(result[0]) else print('Failed')
    decodeListOfEvents(result[1:])

    command = '10'
    s.send(command.encode())

def scenario1():
    s = socket.socket()
    host = socket.gethostname()
    port = 12345
    s.connect((host, port))

    command = '10'
    s.send(command.encode())




if __name__=='__main__':
    scenario()