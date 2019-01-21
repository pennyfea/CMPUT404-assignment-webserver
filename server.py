#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):


    http_message = ""
    dir = "/www"
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8'))

        httpRequest = self.data.splitlines()
        httpRequestMethod = httpRequest[0].decode().split()

        print(httpRequestMethod)
        print("Request method: %s\n" % httpRequestMethod[0])

        if(httpRequestMethod[0] == "GET"):
            
            requestedFile =  httpRequestMethod[1]
            print(requestedFile)
            print("Requested File: ", requestedFile)

            path = os.path.abspath(os.getcwd() + self.dir + requestedFile)
            print("Real path: ", os.path.realpath(path))
            print("This is your path: ", path)

            if (os.path.exists(path) and os.path.isfile(path)):

                if(path.endswith('.css')):
                    self.http_message = ("HTTP/1.1/ 200 OK\n"+
                                        "Conten-Type: text/css\n\n"+
                                        open(path).read())
                
                                     
                elif(path.endswith('.html')):
                    self.http_message = ("HTTP/1.1/ 200 OK\n"+
                                        "Conten-Type: text/html\n\n"+
                                        open(path).read())
                
                else:
                    self.http_message = ("HTTP/1.1/ 404 Not found\n"+
                                    "Conten-Type: text/html\n\n"+ 
                                    "<!DOCTYPE html>\n"+
                                    "<html><body>404: Sorry, Not found\n"+
                                    "</body></html>")
        
            if(os.path.isdir(path)):
                print("dir: ", os.path.isdir(path))
                self.http_message = ("HTTP/1.1/ 200 OK\n"+
                    "Conten-Type: text/html\n\n"+
                    open(path+"/index.html").read()) 
            

        else:

            self.http_message = ("HTTP/1.1 405 Method Not Allowed\n"+
                        "Content-Type: text/html\n\n"+
                        "<!DOCTYPE html>\n"+
                        "<html><body>405: Method Not Allowed\n"+
                        "</body></html>")
        
        self.request.sendall(self.http_message.encode('utf-8'))
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
