#!/usr/bin/env python

import socket
import select
import sys
import thread

class Server:
    def __init__(self):
        self.host = ""
        self.port = 12345
        self.backlog = 5
        self.size = 1024
    def run(self, userinput):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host,self.port))
        self.server.listen(self.backlog)
        inputlist = [self.server,userinput]
        outputlist = []
        self.running = 1
        while self.running:
            inputready, outputready, exceptready = select.select(inputlist,outputlist,[])
            for s in inputready:
                if s == self.server:
                    client, address = self.server.accept()
                    inputlist.append(client)
                    outputlist.append(client)
                elif s == userinput:
                    message = userinput.readline()
                    if message == "quit\n":
                        self.running = 0
                        self.server.close()
                        continue
                    for c in outputready:
                        c.send(message)
                else:
                    try:
                        data = s.recv(self.size)
                        if data == "roll\n":
                            print "someone wanted a roll"
                            s.send("no way jose\n")
                    except:
                        pass
s = Server()
s.run(sys.stdin)
