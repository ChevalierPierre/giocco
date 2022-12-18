#!/usr/bin/env python

import pygame as pg
from data.main import main
import data.tools
import argparse

parser = argparse.ArgumentParser(description='Pong Arguments')
parser.add_argument('-c','--clean', action='store_true', 
    help='Remove all .pyc files and __pycache__ directories')
parser.add_argument('-f' , '--fullscreen', action='store_true',
    help='start program with fullscreen')
parser.add_argument('-s' , '--size', nargs=2, default=[800,600], metavar=('WIDTH', 'HEIGHT'),
    help='set window size to WIDTH HEIGHT, defualt is 800 600')
args = vars(parser.parse_args())

if __name__ == '__main__':    
    if args['size']:
        size = args['size']
        #print('window size: {}'.format(size))
        
    if args['clean']:
        data.tools.clean_files()
    else:
        main(args['fullscreen'], size)
    pg.quit()

