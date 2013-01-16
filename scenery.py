from import_all import *

TREE_SIZE_X = 300
TREE_SIZE_Y = 300
assert(TREE_SIZE_X == TREE_SIZE_Y) #assume tree's are square for now

class GenericScenery(GenericTimedSurface):
    """ Contains the basic mechanisms for scenery, mainly food """
    def __init__(self, max_food, respawn_time, width, height, base_color, x=0, y=0):
        super(GenericScenery, self).__init__(respawn_time, width, height, base_color, x, y)
        self.max_food = max_food
        self.current_food = max_food
        
    def __repr__(self):
        s = super(GenericScenery, self).__repr__()
        return 'GenericScenery(max_food=%r)||%s' % (self.max_food, s)
        
    def __str__(self):
        s = super(GenericScenery, self).__str__()
        return 'GenericScenery-max_food:{0}||{1}'.format(self.max_food, s)
        
    def food_respawn(self):
        """ If enough time has passed, respawn the food """
        if(self.timer_fire()):
            self.current_food = self.max_food
            self.redraw()
            self.set_change()
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
            self.set_change()
        return current

    def redraw(self):
        print("YOU MUST IMPLEMENT THIS IN DERIVED CLASSES")
    
class Tree(GenericScenery):
    """It's a tree! This will be scattered around the map for food and protection"""
    def __init__(self, base_color, food_color, no_food_color, x, y, max_food, respawn, fruit_number, dimension):
        super(Tree, self).__init__(max_food, respawn, dimension, dimension, base_color, x, y)
        self.food_color = food_color
        self.no_food_color = no_food_color
        self.fruit_size = dimension/10
        self.fruit_number = fruit_number
        self.fruit_list = []
        self.draw_tree()
    
    def __repr__(self):
        s = super(Tree, self).__repr__()
        return 'Tree(food_color=%r, no_food_color=%r, fruit_number=%r, dimension=%r)||%s' % (self.food_color, self.no_food_color, self.fruit_number, self.fruit_size*10, s)
        
    def __str__(self):
        s = super(Tree, self).__str__()
        return 'Tree-food_color:{0}, no_food_color:{1}, fruit_number:{2}, dimension:{3}||{4}'.format(self.food_color, self.no_food_color, self.fruit_number, self.fruit_size*10, s)
    
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
        self.set_change(False)
            
class SceneryTests(unittest.TestCase):
    """ unit tests for animals """
    def setUp(self):
        pygame.init()
        self.scenery = GenericScenery(100, 1000, 0, 0, RED)
    
    def tearDown(self):
        self.scenery = None
        
    def testGenericGetFood(self):
        food_qty = self.scenery.get_food()
        self.assertEqual(food_qty, 100, "Wrong food qty")
        self.assertEqual(self.scenery.current_food, 0, "There should be no food left")
        pygame.time.delay(1500)
        self.scenery.food_respawn()
        self.assertEqual(self.scenery.current_food, 100, "There should be no food left")
  
    def testTreeGetFood(self):
        #tree = Tree(base_color, food_color, no_food_color, x, y, max_food, food_respawn, fruit_number, dimension)
                    
        self.scenery = Tree(RED, RED, RED, 0, 0, 100, 100, 10, 0)
        food_qty = self.scenery.get_food()
        self.assertEqual(food_qty, 100, "Wrong food qty")
        self.assertEqual(self.scenery.current_food, 0, "There should be no food left")
        pygame.time.delay(200)
        self.scenery.food_respawn()
        self.assertEqual(self.scenery.current_food, 100, "There should be all the food")
        
        