# This is a sample Python script.
import serial
from serial.tools import list_ports
import time
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

ports = list(serial.tools.list_ports.comports())
select = ""
for port in ports:
    if port[0].startswith("/dev/cu.usbmod"):
        select = port[0]
print(select)
heartbeat = 0.1
board = serial.Serial(port=select, baudrate=115200)
time.sleep(1)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:

        board.write(b'a/3/0\n')
        time.sleep(heartbeat)
        board.write(b'a/4/0\n')

        time.sleep(heartbeat)
        board.write(b'a/5/0\n')

        time.sleep(heartbeat)
        board.write(b'a/6/0\n')

        time.sleep(heartbeat)
        board.write(b'a/7/0\n')

        time.sleep(heartbeat)
        board.write(b'a/8/0\n')

        time.sleep(heartbeat)
        board.write(b'a/9/0\n')

        time.sleep(heartbeat)
        board.write(b'a/10/0\n')
        #msg = board.readline()
        #print(msg)
        time.sleep(heartbeat)

        board.write(b'a/3/1\n')

        time.sleep(heartbeat)
        board.write(b'a/4/1\n')

        time.sleep(heartbeat)
        board.write(b'a/5/1\n')

        time.sleep(heartbeat)
        board.write(b'a/6/1\n')

        time.sleep(heartbeat)
        board.write(b'a/7/1\n')

        time.sleep(heartbeat)
        board.write(b'a/8/1\n')

        time.sleep(heartbeat)
        board.write(b'a/9/1\n')

        time.sleep(heartbeat)
        board.write(b'a/10/1\n')
        #msg = board.readline()
        #print(msg)
        time.sleep(heartbeat)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
