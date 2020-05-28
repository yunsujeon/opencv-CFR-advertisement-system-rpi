# -*- coding: utf-8 -*-
import random

rand=random.randrange(0,5) #0~4까지

if rand == 0:
    moviepath = '/home/pi/Downloads/boat.jpg'
    moviename = 'boat'
elif rand == 1:
    moviepath = '/home/pi/Downloads/bus.jpg'
    moviename = 'bus'
elif rand == 2:
    moviepath = '/home/pi/Downloads/coffee.jpg'
    moviename = 'coffee'
elif rand == 3:
    moviepath = '/home/pi/Downloads/cup.jpg'
    moviename = 'cup'
elif rand == 4:
    moviepath = '/home/pi/Downloads/melon.jpg'
    moviename = 'melon'
