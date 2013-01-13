import pygame, sys
from pygame.locals import *
import random
import unittest

RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
TRANSPARENT = pygame.Color(0, 0, 0, 0)

FPS = 60
WINDOW_SIZE_X = 800
assert(WINDOW_SIZE_X % 2 == 0)
WINDOW_SIZE_Y = 600
assert(WINDOW_SIZE_X % 2 == 0)
OFFSET_X = WINDOW_SIZE_X / 2
OFFSET_Y = WINDOW_SIZE_Y / 2


PLAYER_DIMENSION_X = 40
PLAYER_DIMENSION_Y = 40
STEP_SIZE = 3

class GenericSurface(object):
    """The most basic surface 
    
    Since all visible objects need to be on a surface, made this generic class for everything to be built on
    
    """
    def __init__(self, width, height, color, x=0, y=0):
        self.surface_width = width
        self.surface_height = height
        self.surface_color = color
        self.x = x
        self.y = y
        self.surface = pygame.Surface((self.surface_width, self.surface_height))
        self.surface = self.surface.convert_alpha()
        self.surface.fill(self.surface_color)
        self.changed = True
    
    def get_surface(self):
        """Return this objects surface so it can be drawn"""
        return self.surface
    
    def should_redraw_surface(self):
        return self.changed
    
    def set_change(self, val = True):
        self.changed = val
    
class GenericTimedSurface(GenericSurface):
    """ A basic surface that also has a timer functionality """
    def __init__(self, timer_interval, width, height, color, x=0, y=0):
        super(GenericTimedSurface, self).__init__(width, height, color, x, y)
        self.timer_interval = timer_interval
        self.last_timer_fire = 0
    
    def start_timer(self):
        """ Start up the timer """
        self.last_timer_fire = pygame.time.get_ticks() + self.timer_interval
    
    def timer_fire(self):
        """ Check enough time has passed """
        if(self.last_timer_fire != 0):
            if( pygame.time.get_ticks() > self.last_timer_fire ):
                self.last_timer_fire = 0
                return True
        return False
    
class TimedTest(unittest.TestCase):
    """ unit tests for timed surfaces """
    def setUp(self):
        pygame.init()
        self.timer = GenericTimedSurface(100, 0, 0, RED)
    
    def tearDown(self):
        self.timer = None
        
    def testTimerFire(self):
        self.timer.start_timer()
        self.assertFalse(self.timer.timer_fire(), "Timer should not have fired")
        pygame.time.delay(200)
        self.assertTrue(self.timer.timer_fire(), "Timer did not fire")
        self.assertEqual(self.timer.last_timer_fire, 0, "Timer did not reset") 