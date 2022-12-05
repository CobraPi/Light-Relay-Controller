from time import sleep
from serial.tools import list_ports
import PyCmdMessenger
import random
import threading

minMax = [0,0]
flagRandomCycle = False

def random_cycle():
    """
    Each run through of this loop randomly sets the attributes of one light

    This routine is as follows:
        1. Generate a random value for:
            a. current light - light to be modified
            b. pattern (currently only breathe and strobe)
            c. pattern time - different values set for strobe and breathe
            d. pattern delay - time to hold a specific lighting pattern

        2. Increment counter - check for conditions below
            i.) if counter % 32 == 0 -  10 second break to re-initalize all lights to on
            ii.) if counter % 128 == 0 - 6 minute pattern break, re-initalize all lgiths to on
    """
    counter = 0
    while flagRandomCycle:
        # Generating the random values
        light = random.randrange(0, 16)
        pat = random.randrange(4,6)
        if pat == 3:
            minMax[0] = 1
            minMax[1] = 10
        elif pat == 4:
            minMax[0] = 100
            minMax[1] = 700
        time = random.randrange(minMax[0], minMax[1])
        acceleration = random.randrange(3, 50)
        patternDelay = random.randrange(1, 15)
        # Apply those random values to a randomly specified light
        lst = [light, pat, time, acceleration]
        ser.send("CMD_SET_LIGHT", *lst)
        cmd, data, time = ser.receive()
        counter += 1
        print(counter, end=" | ")
        print(cmd, data)
        sleep(patternDelay)

        # 6 minute break every 128 cycles
        if counter % 128 == 0:
            print("6 Minute break")
            ser.send("CMD_INIT_ALL")
            sleep(1)
            ser.send("CMD_ALL_OFF")
            sleep(2)
            ser.send("CMD_ALL_ON")
            #counter = 0
            sleep(360)

        # 15 second break to reset
        elif counter % 32 == 0:
            waitTime = random.randrange(15, 300)
            print(str(waitTime) + " Second Break")
            ser.send("CMD_INIT_ALL")
            sleep(1)
            ser.send("CMD_ALL_OFF")
            sleep(2)
            ser.send("CMD_ALL_ON")
            sleep(waitTime)

    print(str(counter),"pattern cycles completed")

#if __name__ == "__main__":


ports = list(list_ports.comports())
port = ""
for p in ports:
    print(str(p))
    if p[0].startswith("/dev/cu.usb"):
        port = p[0]
pattern = {
    "INIT":0,
    "OFF":1,
    "ON":2,
    "TIMED_PULSE":3,
    "TIMED_BREATHE":4,
    "TIMED_STROBE":5
}

commands = [
    ["CMD_INIT_ALL",""],
    ["CMD_INIT",""],
    ["CMD_SET_LIGHT","iiii"],
    ["CMD_ALL_ON", ""],
    ["CMD_ALL_OFF", ""],
    ["CMD_GET_LIGHT_DATA", "b"*240]
]

arduino = PyCmdMessenger.arduino.ArduinoBoard(device=port, baud_rate=115200)
ser = PyCmdMessenger.CmdMessenger(arduino, commands)
ser.send("CMD_INIT_ALL")

while True:
    usrInput = input("Cmd: ")

    if usrInput == "start":
        ser.send("CMD_ALL_ON")
        flagRandomCycle = True
        patternThread = threading.Thread(target=random_cycle)
        patternThread.daemon = True
        patternThread.start()

    elif usrInput == "stop":
        flagRandomCycle = False
        ser.send("CMD_INIT_ALL")

    elif usrInput == "on":
        ser.send("CMD_ALL_ON")

    elif usrInput == "off":
        ser.send("CMD_ALL_OFF")

    elif usrInput == "init":
        ser.send("CMD_INIT_ALL")

    elif usrInput == "range":
        minMax[0] = int(input("Enter min time value: "))
        minMax[1] = int(input("Enter max time value"))

    elif usrInput == "set":
        light = int(input("Enter light number: "))
        pat = int(input("Enter pattern: "))
        time = int(input("Enter time for pattern: "))
        multiplier = int(input("Enter breath rate multiplier: "))
        ser.send("CMD_SET_LIGHT", light, pat, time, multiplier)

    elif usrInput == "data":
        ser.send("CMD_GET_LIGHT_DATA")
        cmd, msg, time = ser.receive()
        lst = [int(i) for i in msg]
        print(cmd, lst)
