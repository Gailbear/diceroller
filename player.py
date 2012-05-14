#!/usr/bin/env python

import socket
import sys
import select

class Client:
    def __init__(self):
        self.host = "localhost"
        self.port = 12345
        self.size = 1024
    
    def run(self, userinput, useroutput):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host,self.port))
        self.client.setblocking(0)
        self.running = 1
        inputlist = [userinput, self.client]
        outputlist = [self.client]
        while self.running:
            inputready, outputready, exceptready = select.select(inputlist, outputlist, [])
            for s in inputready:
                if s == userinput:
                    try:
                        message = userinput.readline()
                        if message == "quit\n":
                            self.client.close()
                            self.running = 0
                            continue
                        else:
                            self.client.send(message)
                    except:
                        pass

            for s in outputready:
                try:
                    useroutput.write(s.recv(self.size))
                except:
                    pass

c = Client()
c.run(sys.stdin, sys.stdout)
