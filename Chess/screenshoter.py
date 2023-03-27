import pygame
from ChessGame import screen

class Screenshot:
    def __init__(self, name):
        self.name = name
        self.left_top_x = self.left_top_y = 0
        self.bottom_right_x = self.bottom_right_y = 0
        self.width = self.height = 0
        self.making_screenshot = False

    def set_left_top(self,x,y):
        self.left_top_x = x
        self.left_top_y = y

game_screenshot = Screenshot
