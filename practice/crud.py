#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 08:18:51 2021

@author: vagrant
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

#%% Create

myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()

cheezepizza = MenuItem(name = "Cheeze Pizza",
                       description = "ingridients",
                       price = "$8.99",
                       restaurant = myFirstRestaurant)
session.add(cheezepizza)
session.commit()

#%% Read
firstResult = session.query(Restaurant).first()

a = session.query(MenuItem)

items = session.query(MenuItem).all()
for item in items:
    print(item.name)
    
#%% Update

veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for vb in veggieBurgers:
    print(vb.id)
    print(vb.price)
    print(vb.restaurant.name)
    print('\n')
    
UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 10).one()
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit

#%% Delete

spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
session.delete(spinach)
session.commit()