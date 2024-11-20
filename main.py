import random
class Unit:
    def __init__(self, name, health, sdamage, srecover, maxRecover):
        self.name = name
        self.health = health
        self.sdamage = sdamage
        self.srecover = srecover
        self.maxHealth = health
        self.maxBlock = sdamage
        self.action = "start"
        self.outDam = 0
        self.maxRecover = maxRecover
        self.recCounter = 0

    def toAtak(self):
        if self.isAlive():
            self.setAction("atak")
            self.outDam = self.sdamage
        return

    def toBlockAtak(self, dam):
        self.health = round(self.health - (dam - self.maxBlock), 1)
        self.setAction("block")
        self.maxBlock -= 0.1
        self.outDam = 0

    def toHeel(self):
        if self.isAlive():
            rec = round(self.health + self.srecover, 1)
            if rec < self.maxHealth / 2:
                self.health = round(rec, 1)
                self.setAction("recover")
                self.recCounter += 1
            elif rec > self.maxHealth / 2 > self.health:
                self.health = round(self.maxHealth / 2, 1)
                self.setAction("recover")
                self.recCounter += 1
            else:
                self.health = self.health
            self.outDam = 0
            return

    def isAlive(self):
        if self.health > 0:
            return True
        self.setAction("dead")
        self.outDam = 0
        return False

    def getDamaged(self, dam):
        self.health = round(self.health - dam, 1)
        return

    def setName(self, name):
        self.name = name
        return
    def getName(self):
        return self.name

    def setHealth(self, health):
        self.health = health
        return
    def getHealth(self):
        return self.health

    def setSDamage(self, sdamage):
        self.sdamage = sdamage
        return

    def getSDamage(self):
        return self.sdamage

    def setSRecover(self, srecover):
        self.srecover = srecover
        return
    def getSRecover(self):
        return  self.srecover

    def setMaxHealth(self, maxHealth):
        self.maxHealth = maxHealth
        return

    def getMaxHealth(self):
        return self.maxHealth

    def setMaxBlock(self, maxBlock):
        self.maxBlock = maxBlock
        return
    def getMaxBlock(self):
        return self.maxBlock

    def setAction(self, action):
        self.action = action
        return
    def getAction(self):
        return self.action

    def getRecCounter(self):
        return self.recCounter
    def setRecCounter(self, recCounter):
        self.recCounter = recCounter
        return
    def getMaxRec(self):
        return self.maxRecover
    def setMaxRec(self, maxRec):
        self.maxRecover = maxRec
        return

class Player(Unit):
    def Control(self, key, opponent):
        dam = opponent.outDam
        if self.isAlive():
            if key == '1':
                self.getDamaged(dam)
                self.toAtak()
            elif key == '2':
                self.toBlockAtak(dam)
            elif key == '3':
                self.getDamaged(dam)
                self.toHeel()
        print(self.name, self.getAction())
        return
                
class Bot(Unit):
    def __init__(self, name, health, sdamage, srecover, maxRecover, transition_matrix):
        super().__init__(name, health, sdamage, srecover, maxRecover)
        self.transition_matrix = transition_matrix
    def settransitionMatrix(self, transition_matrix):
        self.transition_matrix = transition_matrix
        return
    def getTransitionMatrixP(self, part):
        return self.transition_matrix[part]
    def gettransitionMatrix(self):
        return self.transition_matrix

    def play(self, opponent):
        dam = opponent.outDam
        if self.getAction() == "start":
            self.setAction("atak")
        if self.isAlive():
            if opponent.action == "atak":
                if self.getHealth() < self.getMaxHealth() / 2 and self.getRecCounter() <= self.getMaxRec():
                    if self.getAction() == "atak":
                        probabilities = self.transition_matrix[0]
                    elif self.getAction() == "block":
                        probabilities = self.transition_matrix[1]
                    else:
                        probabilities = self.transition_matrix[2]
                else:
                    if self.getAction() == "atak":
                        probabilities = self.transition_matrix[3]
                    elif self.getAction() == "block":
                        probabilities = self.transition_matrix[4]
                    else:
                        probabilities = self.transition_matrix[5]
            else:
                if self.getHealth() < self.getMaxHealth() / 2:
                    if self.getAction() == "atak":
                        probabilities = self.transition_matrix[6]
                    elif self.getAction() == "block":
                        probabilities = self.transition_matrix[7]
                    else:
                        probabilities = self.transition_matrix[8]
                else:
                    probabilities = self.transition_matrix[9]

            actions = ["atak", "block", "recover"]
            action = random.choices(actions, weights=probabilities)[0]
            if action == "atak":
                self.getDamaged(dam)
                self.toAtak()
            elif action == "block":
                self.toBlockAtak(dam)
            else:
                self.getDamaged(dam)
                self.toHeel()
        print(self.getName(), self.getAction())
        return


transition_matrix_E = [
    [0.6, 0.2, 0.2],
    [0.7, 0.1, 0.2],
    [0.9, 0.05, 0.05],
    [0.6, 0.4, 0],
    [0.7, 0.3, 0],
    [0.9, 0.1, 0],
    [0.6, 0, 0.4],
    [0.7, 0, 0.3],
    [0.9, 0, 0.1],
    [1, 0, 0]
]

transition_matrix_M = [
    [0.4, 0.3, 0.3],
    [0.5, 0.2, 0.3],
    [0.8, 0.1, 0.1],
    [0.5, 0.5, 0],
    [0.6, 0.4, 0],
    [0.8, 0.2, 0],
    [0.5, 0, 0.5],
    [0.6, 0, 0.4],
    [0.8, 0, 0.2],
    [1, 0, 0]
]

bot = Bot("computer", 10, 1, 1, 5, transition_matrix_E)
lflag = True
while lflag:
    level = input("Choose level 1, 2 or 3:")
    if level == '1':
        lflag = False
    elif level == '2':
        bot.settransitionMatrix(transition_matrix_M)
        lflag = False
    elif level == '3':
        bot.settransitionMatrix(transition_matrix_M)
        bot.setSRecover(2)
        lflag = False
    else:
        print("No such level")

player = Player("human", 10, 1, 2, 5)

flag = True
print("Bot health: ", bot.getHealth(), "/", bot.getMaxHealth())
print("Player health: ", player.getHealth(), "/", player.getMaxHealth())
while flag:
    flag1 = True
    bot.play(player)
    print("Bot health: ", bot.getHealth(), "/", bot.getMaxHealth())
    print("Player health: ", player.getHealth(), "/", player.getMaxHealth())
    if not bot.isAlive():
        print("You win!")
        flag = False
        flag1 = False
    while flag1:
        if (player.getHealth() < player.getMaxHealth() / 2 and player.getRecCounter() < player.getMaxRec()
                and bot.getAction() == "atak"):
            key = input("Press:\n1 - atak\t2 - block\t3 - recover: ")
            if key == '1' or key == '2' or key == '3':
                player.Control(key, bot)
                print("Bot health: ", bot.getHealth(), "/", bot.getMaxHealth())
                print("Player health: ", player.getHealth(), "/", player.getMaxHealth())
                flag1 = False
            else:
                print("Incorrect option!!!")
        elif (not bot.getAction() == "atak" and player.getHealth() < player.getMaxHealth() / 2
              and player.getRecCounter() < player.getMaxRec()):
            key = input("Press:\n1 - atak\t3 - recover: ")
            if key == '1' or key == '3':
                player.Control(key, bot)
                print("Bot health: ", bot.getHealth(), "/", bot.getMaxHealth())
                print("Player health: ", player.getHealth(), "/", player.getMaxHealth())
                flag1 = False
            else:
                print("Incorrect option!!!")
        elif (bot.getAction() == "atak" and not(player.getHealth() < player.getMaxHealth() / 2
              and player.getRecCounter() < player.getMaxRec())):
                key = input("Press:\n1 - atak\t2 - block: ")
                if key == '1' or key == '2':
                    player.Control(key, bot)
                    print("Bot health: ", bot.getHealth(), "/", bot.getMaxHealth())
                    print("Player health: ", player.getHealth(), "/", player.getMaxHealth())
                    flag1 = False
                else:
                    print("Incorrect option!!!")
        else:
            key = input("Press:\n1 - atak: ")
            if key == '1':
                player.Control(key, bot)
                print("Bot health: ", bot.getHealth(), "/", bot.getMaxHealth())
                print("Player health: ", player.getHealth(), "/", player.getMaxHealth())
                flag1 = False
            else:
                print("Incorrect option!!!")

    if not player.isAlive():
        print("Computer win!")
        flag = False
