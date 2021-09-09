#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 09:32:14 2021

@author: vagrant
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = ''
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += """
                    <form method='POST' enctype='multipart/form-data' action='/hello'> 
                        <h2> What would you like to say? </h2>
                        <input type='text'   name='message'>
                        <input type='submit' value='Submit'>
                    </form> 
                """
                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                # return
            if self.path.endswith('/hola'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = ''
                output += "<html><body>&#161Hola  <a href='/hello' >Back to Hello</a>"
                output += """
                    <form method='POST' enctype='multipart/form-data' action='/hello'> 
                        <h2> What would you like to say? </h2>
                        <input type='text'   name='message'>
                        <input type='submit' value='Submit'>
                    </form> 
                """
                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                # return
            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = ''
                output += "<html><body>"
                output += """
                    <div>Restaurants:</div> 
                """
                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                return
        except IOError:
            print('error')
            self.send_error(404, f"File not found {self.path}".encode())
            
    def do_POST(self):
        print('posting')
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
            pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
    
            if ctype == 'multipart/form-data':
                fields=cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
                
            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2>"
            output += f"<h1>{messagecontent[0]}</h1>"
            
            output += """
                <form method='POST' enctype='multipart/form-data' action='/hello'> 
                    <h2> What would you like to say? </h2>
                    <input type='text'   name='message'>
                    <input type='submit' value='Submit'>
                </form> 
            """
            self.wfile.write(output.encode())
            print(output)
            
        except:
            print(Exception.__class__)

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print(f'Web server is runnint on port {port}')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C entered, stopping web server ...')
        server.socket.close()
        
if __name__ == '__main__':
    main()