import time
import socket

class MySocketServer(object):
    def __init__(self):
        self.ip = ""
        self.port = 1338 
        self.createLink()
        self.pause = False
        
    def shouldPause(self, status):
        self.pause = status

    def readData(self):
        try: 
            if self.client:
                if self.pause:
                    return

                data = self.client.recv(1024).strip()
                if data != "":
                    return data
        except:
            print("Algo Disconnected")
            self.client.close()
            self.createLink()
 
    def sendData(self, data):
        try:
            if self.client:
                self.client.sendall(data)
        except:
            print("Algo Disconnected")
            self.client.close()
            self.createLink()

    def getService(self):
        return "Socket"

    def createLink(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Awaiting Algorithm")
        # If port is unclosed by previous script, reuse it
        self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.conn.bind((self.ip, self.port))
        self.conn.listen(1) # Make it a server 
        self.client, self.addr = self.conn.accept()
        print("Algorithm: " +  str(self.addr[0]) + ":" + str(self.addr[1]))
