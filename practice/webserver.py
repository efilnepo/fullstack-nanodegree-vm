#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 09:32:14 2021

@author: vagrant
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += """
                    <a href="/restaurants">Restaurants</a>
                """
                output += "</html></body>"
                self.wfile.write(output.encode())
                
            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                                
                session = DBSession()
                restaurants = session.query(Restaurant).all()
                
                output = ''
                output += "<html><body>"
                
                output += "<div><a href='restaurants/new'>Make new restaurant</a></div>"
                
                output += """
                    <div>Restaurants:</div> 
                """
                
                for restaurant in restaurants:
                    rest_id = restaurant.id
                    name = restaurant.name
                    output += f'<div>{name}</div>'
                    output += f'<a href="/restaurants/edit/{rest_id}">Edit</a>'
                    output += f'<a href="/restaurants/delete/{rest_id}">Delete</a>'
                
                output += "</body></html>"
                self.wfile.write(output.encode())
                # print(output)
                return
            
            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                
                output +="""
                    <form method='POST' enctype='multipart/form-data' action='/restaurants/new'> 
                        <h2> Make new restaurant </h2>
                        <input type='text'   name='name'>
                        <input type='submit' value='Add'>
                    </form> 
                """
                
                output += "</body></html>"
                self.wfile.write(output.encode())
                # print(output)
                return

            if self.path.startswith('/restaurants/edit'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                rest_id = self.path.split('/')[3]
                output +=f"""
                    <form method='POST' enctype='multipart/form-data' action='/restaurants/edit/{rest_id}'> 
                        <h2> Edit restaurant </h2>
                        <input type='text'   name='new_name'>
                        <input type='submit' value='Rename'>
                    </form> 
                """
                
                output += "</body></html>"
                self.wfile.write(output.encode())
                # print(output)
                return
            
            if self.path.startswith('/restaurants/delete'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                rest_id = self.path.split('/')[3]
                output +=f"""
                    <form method='POST' enctype='multipart/form-data' action='/restaurants/delete/{rest_id}'> 
                        <h2> Delete restaurant </h2>
                        <input type='submit' value='Delete'>
                    </form> 
                """
                
                output += "</body></html>"
                self.wfile.write(output.encode())
                # print(output)
                return
            
        except IOError:
            print('error')
            self.send_error(404, f"File not found {self.path}".encode())
            
    def do_POST(self):
        print('posting')
        if True:
            if self.path.endswith('/restaurants/new'):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                
                ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
                pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
                content_len = int(self.headers.get('Content-length'))
                pdict['CONTENT-LENGTH'] = content_len
        
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    message_content = fields.get('name')
                
                new_restaurant = Restaurant(name=message_content[0])
                session = DBSession()
                session.add(new_restaurant)
                session.commit()
                session.close()

                return
                
            if self.path.startswith('/restaurants/edit'):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                
                ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
                pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
                content_len = int(self.headers.get('Content-length'))
                pdict['CONTENT-LENGTH'] = content_len
        
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    message_content = fields.get('new_name')
                
                session = DBSession()
                print(self.path.split('/'))
                restaurant = session.query(Restaurant).filter_by(id=self.path.split('/')[3]).one()
                restaurant.name = message_content[0]
                print(message_content[0])
                session.add(restaurant)
                session.commit()
                session.close()

                return
                    
            if self.path.startswith('/restaurants/delete'):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                
                ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
                pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
                content_len = int(self.headers.get('Content-length'))
                pdict['CONTENT-LENGTH'] = content_len
        
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    # message_content = fields.get('new_name')
                
                session = DBSession()
                print(self.path.split('/'))
                restaurant = session.query(Restaurant).filter_by(id=self.path.split('/')[3]).one()
                # print(message_content[0])
                session.delete(restaurant)
                session.commit()
                session.close()

                return
            
        # except:
        #     print(Exception.__class__)

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