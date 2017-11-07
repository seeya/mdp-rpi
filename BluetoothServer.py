from bluetooth import *

class BluetoothServer(object):
    def __init__(self):
        self.uuid = "00001101-0000-1000-8000-00805F9B34FB"
        self.createLink()
        self.hasStart = False

    def getService(self):
        return "Bluetooth"

    def createLink(self):
        try:
            self.server_sock = BluetoothSocket(RFCOMM)
            self.server_sock.bind(("",PORT_ANY))
            self.server_sock.listen(1)
            self.port = self.server_sock.getsockname()[1]

            advertise_service(self.server_sock, "BTServer",
                               service_id = self.uuid,
                               service_classes = [self.uuid, SERIAL_PORT_CLASS],
                               profiles = [SERIAL_PORT_PROFILE])

            print("Awaiting Bluetooth Connection on port: %d" % self.port)
            self.client_sock, self.client_info = self.server_sock.accept()
            print("Bluetooth Connected from ", self.client_info)
        except:
            print("Reconnecting Bluetooth")

    
    # Thread this function and loop it to get new data 
    def readData(self):
        try:
            data = self.client_sock.recv(1024)
            if data != "":
                print(data)
                return data
        except IOError:
            print("Bluetooth Disconnected")
            self.client_sock.close()
            self.server_sock.close()
            self.createLink()

    def sendData(self, data):
        if data != "":
            if data == "E" and self.hasStart == False:
                self.hasStart = True
                self.client_sock.send(data)
            else:
                self.client_sock.send(data)
