from import_all import *

class GenericAnimal(GenericSurface):
    """ Contains the basic mechanisms for animals, namely health and mass """
    def __init__(self, max_health, current_size, width, height, base_color, x=0, y=0):
        super(GenericAnimal, self).__init__(width, height, base_color, x, y)
        self.max_health = max_health
        self.current_health = max_health
        self.current_mass = 0
        self.size_level = current_size
        
    def eat_food(self, food_qty):
        """ Food will first regen health, and then if any is left over add it to mass """
        if(food_qty > 0):
            if(self.current_health != self.max_health):
                dif = self.max_health - self.current_health
                if(dif >= food_qty):
                    self.current_health += food_qty
                    food_qty = 0
                else:
                    self.current_health = self.max_health
                    food_qty -= dif
            self.current_mass += food_qty
            print("health {0} mass {1}".format(self.current_health, self.current_mass))
            
    def get_health(self):
        """ Return the current and max health """
        return self.current_health, self.max_health
    
    def get_mass(self):
        """ Return current mass """
        return self.current_mass
    
    def get_size(self):
        """ Return current size """
        return self.size_level
    

class AnimalsTests(unittest.TestCase):
    """ unit tests for animals """
    def setUp(self):
        pygame.init()
        self.animal = GenericAnimal(100, 1, 0,0, RED)
        self.animal.current_health = 80
    
    def tearDown(self):
        self.animal = None
        
    def testNoFood(self):
        self.animal.eat_food(0)
        current_health, max_health = self.animal.get_health()
        self.assertEqual(max_health, self.animal.max_health, "Somehow max health changed")
        self.assertEqual(current_health, 80, "Did not add a little health")
        self.assertEqual(self.animal.get_mass(), 0, "Mass was added when it should not")
        
    def testSomeHealth(self):
        self.animal.eat_food(10)
        current_health, max_health = self.animal.get_health()
        self.assertEqual(max_health, self.animal.max_health, "Somehow max health changed")
        self.assertEqual(current_health, 90, "Did not add a little health")
        self.assertEqual(self.animal.get_mass(), 0, "Mass was added when it should not")
    
    def testAllHealth(self):
        self.animal.eat_food(20)
        current_health, max_health = self.animal.get_health()
        self.assertEqual(max_health, self.animal.max_health, "Somehow max health changed")
        self.assertEqual(current_health, 100, "Did not add a little health")
        self.assertEqual(self.animal.get_mass(), 0, "Mass was added when it should not")
        
    def testHealthAndMass(self):
        self.animal.eat_food(50)
        current_health, max_health = self.animal.get_health()
        self.assertEqual(max_health, self.animal.max_health, "Somehow max health changed")
        self.assertEqual(current_health, 100, "Did not add a little health")
        self.assertEqual(self.animal.get_mass(), 30, "Wrong mass added")
        
    def testOnlyAddMass(self):
        self.animal.current_health = self.animal.max_health
        self.animal.eat_food(50)
        current_health, max_health = self.animal.get_health()
        self.assertEqual(max_health, self.animal.max_health, "Somehow max health changed")
        self.assertEqual(current_health, 100, "Wrong Health")
        self.assertEqual(self.animal.get_mass(), 50, "Wrong Mass")
    