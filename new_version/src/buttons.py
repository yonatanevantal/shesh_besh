__author__ = 'yonatan'
import pygame


class Button():

    # button object -
    # an area meant to tell id the mouse is pressed in it

    def __init__(self, x, y, width, height, description=""):
        # constructor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.description = description
        self.released = True

    def is_in(self):
        # check if mouse is in the button area
        # returns a boolean value
        x_mouse, y_mouse = pygame.mouse.get_pos()
        return self.x < x_mouse < int(self.x+self.width) and self.y < y_mouse < int(self.y+self.height)

    def is_pressed(self, events):
        # checks if the button was pressed by the muse
        # return a boolean value
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.is_in():
                self.released = False
                return False
            elif event.type == pygame.MOUSEBUTTONUP and not self.is_in() and not self.released:
                self.released = True
                return False
            if event.type == pygame.MOUSEBUTTONUP and self.is_in() and not self.released:
                self.released = True
                return True
        return False

    def set_position(self, x, y):
        # set x and y variables
        self.x = x
        self.y = y

    def set_size(self, width, height):
        # set width and height variables
        self.width = width
        self.height = height

    def get_height(self):
        # returns height variable
        return self.height

    def get_width(self):
        # returns width variable
        return self.width


class ImageButton(Button):
    # image button object -
    # inherits from the button class its methods and varibales
    # gets an image to show on screen as the button

    def __init__(self, screen, x, y, image_released ,image_pressed, description=""):
        # constructor
        self.image_pressed = image_pressed
        self.image_released = image_released
        Button.__init__(self, x, y, self.image_released.get_width(), self.image_released.get_height(), description)
        self.screen = screen

    def show(self):
        # shows image surface on screen
        if self.released:
            self.screen.blit(self.image_released, (self.x, self.y))
        else:
            self.screen.blit(self.image_pressed, (self.x, self.y))

    def set_screen(self, screen):
        # set the screen (or surface) for the surface to be shown on
        self.screen = screen
