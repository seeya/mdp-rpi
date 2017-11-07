import serial
import time

class SerialServer(object):
    def __init__(self):
        self.port = "/dev/ttyACM0"
        self.baud_rate = 9600
        self.s = None

    def getService(self):
        return "Serial"

    def readData(self):
        try:
            if self.s:
                data = self.s.readline()
                if data != "":
                    if data[:3] == "ACK":
                        return data.split("ACK")[1]
                    if data[:3] == "CAL":
                        return
                else:
                    return
            else:
                self.createLink()
        except AttributeError, a:
            print("Serial disconnected")
            self.createLink()

    def sendData(self, data):
        if data != "":
            self.s.write(data) 

    def createLink(self):
        try:
            self.s = serial.Serial(self.port, self.baud_rate)
            print("Serial connected")
        except:
            print("Awaiting Serial")
            time.sleep(5)
            self.createLink()
