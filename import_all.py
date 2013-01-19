import pygame, sys
from pygame.locals import *
import random
import unittest
import logging
import datetime

#initiate the log file
file_name = 'logs//' + datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S') + '.log'
logging.basicConfig(format='%(levelname)s:%(filename)s:%(lineno)d:%(message)s',filename=file_name, level=logging.DEBUG)
logging.info('Program launched')

RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
ORANGE = pygame.Color(255, 165, 0)
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
    
    def __repr__(self):
        return 'GenericSurface(width=%r, height=%r, color=%r, x=%r, y=%r)' % (self.surface_width, self.surface_height, self.surface_color, self.x, self.y)
    
    def __str__(self):
        return 'GenericSurface-w:{0} h:{1} base_color:{2} x:{3} y:{4}'.format(self.surface_width, self.surface_height, self.surface_color, self.x, self.y)
    
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
    
    def __repr__(self):
        s = super(GenericTimedSurface, self).__repr__()
        return 'GenericTimedSurface(timer_interval=%r)||%s' % (self.timer_interval, s)
    
    def __str__(self):
        s = super(GenericTimedSurface, self).__str__()
        return 'GenericTimedSurface-timer_interval:{0}||{1}'.format(self.timer_interval, s)
    
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