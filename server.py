#!/usr/bin/env python3

#  coding: utf-8 
import socketserver
import os
import sys

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


#***************************************************************************************
#    Title: HTTP
#    Availability: https://developer.mozilla.org/en-US/
#     
#    Title: Common pathname manipulations
#    Availability: https://docs.python.org/3/library/os.path.html
#       
#    
#    Title: http.server — HTTP servers
#    Reason: Used for inspiration
#    Availability: https://docs.python.org/3/library/http.server.html
#
#
#    Title: Lab 2: TCP Proxy
#    Reason: Better understanding of assignment
#    Availability: https://uofa-cmput404.github.io/
#***************************************************************************************


class MyWebServer(socketserver.BaseRequestHandler):


    http_message = ""
    dir = "/www"
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8'))

        httpRequest = self.data.splitlines()
        httpRequestMethod = httpRequest[0].decode().split()

        # print(httpRequestMethod)
        # print("Request method: %s\n" % httpRequestMethod[0])

        if(httpRequestMethod[0] == "GET"):
            
            # Debugging: Useful terminal info
            ###########################################################
            requestedFile =  httpRequestMethod[1]

            # print(requestedFile)
            # print("Requested File: ", requestedFile)

            path = os.path.abspath(os.getcwd() + self.dir + requestedFile)
            # print("Real path: ", os.path.realpath(path))
            # print("This is your path: ", path)
            ###########################################################

            # Check if the path is a file and the requested path is in the realpath
            if (os.path.isfile(path) and requestedFile in os.path.realpath(path)):
                
                # Handles mime types
                if(path.endswith('.css')):
                    self.handle_200_status_codes(200, "css", path)
                                     
                elif(path.endswith('.html')):
                    self.handle_200_status_codes(200, "html", path)
                                   
            # If dir exsits and ends with a /
            elif(os.path.isdir(path)):
                if requestedFile[-1] != "/":
                    self.handle_301_status_codes(301, requestedFile + "/")
                else:
                    self.handle_200_status_codes(200, "html", path+"/index.html")
            


            # If it doesn't exisits
            else:
                self.handle_404_405_codes(404, "Not found")
        
        # If not GET method, 405 status code
        else:
            self.handle_404_405_codes(405, "Method Not Allowed")
        
    
    # Handles status error codes
    def handle_404_405_codes(self, status_code, message):
        self.http_message = ("HTTP/1.1 %d %s\r\n" % (status_code, message) +
                            "Content-Type: text/html\r\n"+
                            "Content-Length: %d\n\n" % (sys.getsizeof(message) + sys.getsizeof(int(status_code))) +
                            "<html><body><center><h1>%d %s</center></h1>\n" % (status_code, message)+
                            "</body></html>")

        self.request.sendall(self.http_message.encode('utf-8'))

    # Handles the 200 status codes
    def handle_200_status_codes(self,  status_code, file_type, path):
        self.http_message = ("HTTP/1.1/ %d OK\r\n"  % (status_code)+
                                        "Content-Type: text/%s\r\n" % (file_type)+
                                        "Content-Length: %d\n\n" % (os.path.getsize(path))+
                                        open(path).read()) 
        self.request.sendall(self.http_message.encode('utf-8'))
    
    # Handles the 301 status codes
    def handle_301_status_codes(self, status_code, path):
        self.http_message = ("HTTP/1.1 %d Moved Permanently\r\n" % (status_code) +
                             "Location: %s\n\n" % (path))
        
        self.request.sendall(self.http_message.encode('utf-8'))

   
        


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
