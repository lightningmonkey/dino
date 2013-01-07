from import_all import *

MAX_TREE_FOOD = 100
TREE_RESPAWN_TIME = 10000 #Time in milliseconds
TREE_SIZE_X = 100
TREE_SIZE_Y = 100
TREE_FRUIT_NUMBER = 10
assert(TREE_SIZE_X == TREE_SIZE_Y) #assume tree's are square for now

class GenericScenery(GenericTimedSuface):
    """ Contains the basic mechanisms for scenery, mainly food """
    def __init__(self, max_food, respawn_time, width, height, base_color, x=0, y=0):
        super(GenericScenery, self).__init__(respawn_time, width, height, base_color, x, y)
        self.max_food = max_food
        self.current_food = max_food
        
    def food_respawn(self):
        """ If enough time has passed, respawn the food """
        if(self.timer_fire()):
            self.current_food = self.max_food
            self.redraw()
            return True
        return False
                
    def get_food(self):
        """ Eat the food by returning all the food the object has, and redraw """
        current = 0
        if(self.current_food > 0): #Only reset the timer if the food has been eaten
            current = self.current_food
            self.current_food = 0
            self.start_timer()
            self.redraw()
        return current

    def redraw(self):
        print("YOU MUST IMPLEMENT THIS IN DERIVED CLASSES")
    
class Tree(GenericScenery):
    """It's a tree! This will be scattered around the map for food and protection"""
    def __init__(self, base_color, food_color, no_food_color, x, y):
        assert( TREE_SIZE_X == TREE_SIZE_Y)
        super(Tree, self).__init__(MAX_TREE_FOOD, TREE_RESPAWN_TIME, TREE_SIZE_X, TREE_SIZE_Y, base_color, x, y)
        self.food_color = food_color
        self.no_food_color = no_food_color
        self.fruit_size = TREE_SIZE_X/10
        self.fruit_number = TREE_FRUIT_NUMBER
        self.fruit_list = []
        self.draw_tree()
    
    def draw_tree(self):
        """The tree is a square, because it makes things easier then a circle"""
        color = self.food_color if 0 != self.current_food else self.no_food_color
        random.seed()
        for i in range(self.fruit_number):
            x = random.randint(0, self.surface_width - self.fruit_size)
            y = random.randint(0, self.surface_height - self.fruit_size)
            self.fruit_list.append((x,y))
            pygame.draw.rect(self.surface, color, (x, y, self.fruit_size, self.fruit_size))
    
    def redraw(self):
        color = self.food_color if 0 != self.current_food else self.no_food_color
        for point in self.fruit_list:
            pygame.draw.rect(self.surface, color, (point[0], point[1], self.fruit_size, self.fruit_size))
            
class SceneryTests(unittest.TestCase):
    """ unit tests for animals """
    def setUp(self):
        pygame.init()
        self.scenery = GenericScenery(100, 1000, 0, 0, RED)
    
    def tearDown(self):
        self.scenery = None
        
    def testGenericGetFood(self):
        food_qty = self.scenery.get_food()
        self.assertEqual(food_qty, MAX_TREE_FOOD, "Wrong food qty")
        self.assertEqual(self.scenery.current_food, 0, "There should be no food left")
        pygame.time.delay(1500)
        self.scenery.food_respawn()
        self.assertEqual(self.scenery.current_food, 100, "There should be no food left")
  
    def testTreeGetFood(self):
        self.scenery = Tree(RED, RED, RED, 0, 0)
        food_qty = self.scenery.get_food()
        self.assertEqual(food_qty, 100, "Wrong food qty")
        self.assertEqual(self.scenery.current_food, 0, "There should be no food left")
        pygame.time.delay(TREE_RESPAWN_TIME + 100)
        self.scenery.food_respawn()
        self.assertEqual(self.scenery.current_food, 100, "There should be all the food")
        
        