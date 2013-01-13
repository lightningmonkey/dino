from import_all import *
from scenery import *
from xml.etree import ElementTree as etree

MAX_TREE_FOOD_DEFAULT = 100
TREE_RESPAWN_TIME_DEFAULT = 10000 #Time in milliseconds
TREE_FRUIT_NUMBER_DEFAULT = 10

class Map(object):
    def __init__(self,  file_name):
        file = open(file_name, 'r')
        tree = etree.parse(file)
        self.root = tree.getroot()
        self.objects = []
        self.parse()
         
    def parse(self):
        cur = self.root.find('Width')
        self.PLAYABLE_DIMENSION_X = int(cur.text)
        cur = self.root.find('Height')
        self.PLAYABLE_DIMENSION_Y = int(cur.text)
        self.BACKGROUND_DIMENSION_X = OFFSET_X*2 + self.PLAYABLE_DIMENSION_X
        self.BACKGROUND_DIMENSION_Y = OFFSET_Y*2 + self.PLAYABLE_DIMENSION_Y
        objects = self.root.find('Objects')
        for parent in objects.getiterator():
            for child in parent:
                if child.tag == 'Tree':
                    cur = child.find('MaxFood')
                    max_food = int(cur.text) if cur.text != None else MAX_TREE_FOOD_DEFAULT
                    cur = child.find('FoodRespawn')
                    food_respawn = int(cur.text) if cur.text != None else TREE_RESPAWN_TIME_DEFAULT
                    cur = child.find('FruitNumber')
                    fruit_number = int(cur.text) if cur.text != None else TREE_FRUIT_NUMBER_DEFAULT
                    dimension = int(child.find('Dimension').text)
                    x = int(child.find('X').text)
                    y = int(child.find('Y').text)
                    cur = child.find('BaseColor')
                    base_color_r = int(cur.find('Red').text)
                    base_color_g = int(cur.find('Green').text)
                    base_color_b = int(cur.find('Blue').text)
                    base_color = pygame.Color(base_color_r, base_color_g, base_color_b)
                    cur = child.find('FoodColor')
                    food_color_r = int(cur.find('Red').text)
                    food_color_g = int(cur.find('Green').text)
                    food_color_b = int(cur.find('Blue').text)
                    food_color = pygame.Color(food_color_r, food_color_g, food_color_b)
                    cur = child.find('NoFoodColor')
                    no_food_color_r = int(cur.find('Red').text)
                    no_food_color_g = int(cur.find('Green').text)
                    no_food_color_b = int(cur.find('Blue').text)
                    no_food_color = pygame.Color(no_food_color_r, no_food_color_g, no_food_color_b)
                    tree = Tree(base_color, food_color, no_food_color, x, y, max_food, food_respawn, fruit_number, dimension)
                    self.objects.append(tree)
                    
class MapTests(unittest.TestCase):
    """ unit tests for animals """
    def setUp(self):
        pygame.init()
        self.map = Map("map_definitions/test1.xml")

    def tearDown(self):
        self.map = None
        
    def testTree1(self):
        self.assertEqual(self.map.PLAYABLE_DIMENSION_X, 1000)
        self.assertEqual(self.map.PLAYABLE_DIMENSION_Y, 8000)
        tree = self.map.objects[0]
        self.assertEqual(tree.max_food, MAX_TREE_FOOD_DEFAULT)
        self.assertEqual(tree.timer_interval, TREE_RESPAWN_TIME_DEFAULT)
        self.assertEqual(tree.fruit_number, TREE_FRUIT_NUMBER_DEFAULT)
        self.assertEqual(tree.surface_width, 300)
        self.assertEqual(tree.surface_height, 300)
        self.assertEqual(tree.x, 200)
        self.assertEqual(tree.y, 250)
        self.assertEqual(tree.surface_color, pygame.Color(46, 139, 87))
        self.assertEqual(tree.food_color, pygame.Color(255, 0, 0))
        self.assertEqual(tree.no_food_color, pygame.Color(50, 205, 50))
        
  
    def testTree2(self):
        self.assertEqual(self.map.PLAYABLE_DIMENSION_X, 1000)
        self.assertEqual(self.map.PLAYABLE_DIMENSION_Y, 8000)
        tree = self.map.objects[1]
        self.assertEqual(tree.max_food, 1)
        self.assertEqual(tree.timer_interval, 2)
        self.assertEqual(tree.fruit_number, 3)
        self.assertEqual(tree.surface_width, 4)
        self.assertEqual(tree.surface_height, 4)
        self.assertEqual(tree.x, 5)
        self.assertEqual(tree.y, 6)
        self.assertEqual(tree.surface_color, pygame.Color(7, 8, 9))
        self.assertEqual(tree.food_color, pygame.Color(10, 11, 12))
        self.assertEqual(tree.no_food_color, pygame.Color(13, 14, 15))
        