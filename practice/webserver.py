#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 09:32:14 2021

@author: vagrant
"""

from http.server import BaseHTTPRequestHandler, HTTPServer

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = ''
                output += '<html><body>Hello!</body></html>'
                self.wfile.write(output.encode())
                print(output)
                return
        except IOError:
            self.send_error(404, f"File not found {self.path}".encode())

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