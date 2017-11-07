import time
import threading
from MySocketServer import MySocketServer
from BluetoothServer import BluetoothServer 
from SerialServer import SerialServer

ANDROID = "Bluetooth" 
ALGO = "Socket" 
ARDUINO = "Serial" 

class MainController(object):
    def __init__(self):
        print("Main Controller Initializing...")
        self.services = {} # Keep a reference of created objects 
        self.start_threads()
        self.keep_alive()

    def start_threads(self):
        self.init_thread(SerialServer(), ARDUINO, self.SerialHandler)
        self.init_thread(MySocketServer(), ALGO, self.SocketHandler) 
        self.init_thread(BluetoothServer(), ANDROID, self.BluetoothHandler)

    def init_thread(self, service, name, handler):
        self.services[name] = service
        t = threading.Thread(target=self.readData, args=[service, handler], name=name)
        t.daemon = True
        t.start()

    def readData(self, service, handler):
        while True:
            data = service.readData() 
            if data != None:
                handler(data) # Each service is handled by a handler
                print("[IN] " + service.getService() + "\n" + data)
                print("-------------------")

    def sendData(self, sender, receiver, data):
        try:
            self.services[receiver].sendData(str(data))
        except Exception, e:
            self.services[receiver].createLink()
            print(str(e) + ": not initialized")

        print(sender + " --> " + receiver + "\n" + data)

    def BluetoothHandler(self, data):
        if data == "F" or data == "L" or data == "R" or data == "B":
            self.sendData(ANDROID, ARDUINO, data)

        if data[:2] == "WP":
            self.sendData(ANDROID, ALGO, data[3:] + "\n")

        if data == "E" or data == "FP":
            self.sendData(ANDROID, ARDUINO, "S")
            self.sendData(ANDROID, ALGO, data + "\n")

    def SocketHandler(self, data):
        movement, position, explored, grid = data.split(";")
        position = position[4:]
        self.sendData(ALGO, ANDROID, "{ robotPosition: [" + position + "], explore: '" + explored + "', grid: '" + grid + "'}")
        if movement == "F" or movement == "L" or movement == "R": 
            self.sendData(ALGO, ARDUINO, movement)

    def SerialHandler(self, data):
        if data != "":
            self.sendData(ARDUINO, ALGO, data)

    def keep_alive(self):
        while True:
            time.sleep(1)

if __name__ == "__main__":
    MainController()
