from random import randint

# Random Number Generator
def rng(x):
    return randint(1, x)

# Main class for terrain creation and time control
class Terrain(object):
    def __init__(self, x, y, creatures):
        self.x = x
        self.y = y
        self.creatures = {} #Dict for all the creatures in the terrain
        self.cells = [] #List for all the terrain cells
        #Generating and storing the terrain cells
        for cell_rol in range(x):
            cell_placeholder = []
            for cell_col in range(y):
                cell_placeholder.append(TerrainCell(cell_rol, cell_col))
            self.cells.append(cell_placeholder)
        #Generating and storing the creatures
        for creature in range(creatures):
            rand_rol = rng(x - 1)
            rand_col = rng(y - 1)
            creature_type = rng(3)
            if creature_type == 1:
                self.creatures[creature] = Herbivore(x = rand_rol, y = rand_col, ide = creature)
                self.cells[rand_rol][rand_col].creatures[creature] = self.creatures[creature]
            elif creature_type == 2:
                self.creatures[creature] = Carnivore(x = rand_rol, y = rand_col, ide = creature)
                self.cells[rand_rol][rand_col].creatures[creature] = self.creatures[creature]
            else:
                self.creatures[creature] = Scavenger(x = rand_rol, y = rand_col, ide = creature)
                self.cells[rand_rol][rand_col].creatures[creature] = self.creatures[creature]
                
    #Main method for the passing of time
    def play(self):
        for creature in self.creatures:
            if self.creatures[creature].status == "ALIVE":
                if self.creatures[creature].is_hungry():
                    self.creatures[creature].look_for_food(self)
                self.creatures[creature].age += 1
                self.creatures[creature].starving_check()
                
    #Checks if there are alive animals in the terrain
    def has_alive_animals(self):
        for creature in self.creatures:
            if self.creatures[creature].status == "ALIVE":
                return True
            else:
                print("Everyone is DEAD!")
                return False
            
#Main class for terrain cells
class TerrainCell(object):
    def __init__(self, x, y):
        self.coords = {"x": x, "y": y}
        self.creatures = {}
        terrain_type = {1: "WATER", 2: "DESERT", 3: "MOUNTAIN", 4: "GRASS"}
        self.cell_type = terrain_type[rng(4)]

#Main class for the creatures
class Creature(object):
    def __init__(self, x, y, ide):
        self.cell = {"x": x, "y": y}
        self.ide = ide
        self.hunger = 7
        self.status = "ALIVE"
        self.age = 1
    #Makes the decision of what direction the creature will take
    def move(self, terrarium):
        direction = rng(4)
        move = 1
        # Directions: 1 = Left, 2 = Right, 3 = Up, 4 = Down
        while move == 1:
            if direction == 1:
                if self.cell["y"] == 0:
                    direction = 2
                else: #The "print"'s are a placeholder
                    print("LEFT")
                    del terrarium.cells[self.cell["x"]][self.cell["y"]].creatures[self.ide]
                    self.cell["y"] -= 1
                    terrarium.cells[self.cell["x"]][self.cell["y"]].creatures[self.ide] = terrarium.creatures[self.ide]
                    move = 0

            elif direction == 2:
                if self.cell["y"] == terrarium.y - 1:
                    direction = 1
                else:
                    print("RIGHT")
                    del terrarium.cells[self.cell["x"]][self.cell["y"]].creatures[self.ide]
                    self.cell["y"] += 1
                    terrarium.cells[self.cell["x"]][self.cell["y"]].creatures[self.ide] = terrarium.creatures[self.ide]
                    move = 0

            elif direction == 3:
                if self.cell["x"] == 0:
                    direction = 4
                else:
                    print("UP")
                    del terrarium.cells[self.cell["x"]][self.cell["y"]].creatures[self.ide]
                    self.cell["x"] -= 1
                    terrarium.cells[self.cell["x"]][self.cell["y"]].creatures[self.ide] = terrarium.creatures[self.ide]
                    move = 0

            elif direction == 4:
                if self.cell["x"] == terrarium.x-1:
                    direction = 3
                else:
                    print("DOWN")
                    del terrarium.cells[self.cell["x"]][self.cell["y"]].creatures[self.ide]
                    self.cell["x"] += 1
                    terrarium.cells[self.cell["x"]][self.cell["y"]].creatures[self.ide] = terrarium.creatures[self.ide]
                    move = 0
        if terrarium.cells[self.cell["x"]][self.cell["y"]].cell_type == "WATER":
            self.status = "DEAD"
    #Checks if the creature is hungry
    def is_hungry(self):
        if self.hunger < 5:
            return True
    #Checks if the creature is starving
    def starving_check(self):
        self.hunger -= 1
        if self.hunger == 0:
            self.status = "DEAD"
    #The creature eats			
    def eat(self):
        self.hunger += 5
        if self.hunger > 10:
            self.hunger = 10

#Sub-class for carnivorous creatures
class Carnivore(Creature):
    def look_for_food(self, terrarium):
        for creature in terrarium.cells[self.cell["x"]][self.cell["y"]].creatures:
            if terrarium.cells[self.cell["x"]][self.cell["y"]].creatures[creature].ide != self.ide:
                if terrarium.cells[self.cell["x"]][self.cell["y"]].creatures[creature].status == "ALIVE":
                    self.eat()
                    terrarium.cells[self.cell["x"]][self.cell["y"]].creatures[creature].status = "DEAD"
                    return
        self.move(terrarium)
        
				
#Sub-class for Herbivore creatures
class Herbivore(Creature):
    def look_for_food(self, terrarium):
        if terrarium.cells[self.cell["x"]][self.cell["y"]].cell_type == "GRASS":
            self.eat()
        else:
            self.move(terrarium)

#Sub-class for Scavenger creatures
class Scavenger(Creature):
    def look_for_food(self, terrarium):
        for creature in terrarium.cells[self.cell["x"]][self.cell["y"]].creatures:
            if terrarium.cells[self.cell["x"]][self.cell["y"]].creatures[creature].status == "DEAD":
                self.eat()
                terrarium.cells[self.cell["x"]][self.cell["y"]].creatures[creature].status = "EATEN"
                return
        self.move(terrarium)

    

def main():
    terrain = Terrain(5, 5, 20)
    day = 1

    while terrain.has_alive_animals() and day <= 50:
        print("Day:", day)
        terrain.play()
        day += 1
        

if __name__ == '__main__':
    main()







