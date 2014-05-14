import rg, random


# That's me in the corner...
def ClosestCorner(self,game):
    corner1 = 5, 3
    corner2 = 5, 14
    corner3 = 14, 5
    corner4 = 14, 14


    if rg.wdist(self.location, corner1) < rg.wdist(self.location, corner2):
        if rg.wdist(self.location, corner1) < rg.wdist(self.location, corner3):
            if rg.wdist(self.location, corner1) < rg.wdist(self.location, corner4):
                return corner1
    if rg.wdist(self.location, corner2) < rg.wdist(self.location, corner1):
        if rg.wdist(self.location, corner2) < rg.wdist(self.location, corner3):
            if rg.wdist(self.location, corner2) < rg.wdist(self.location, corner4):
                return corner2
    if rg.wdist(self.location, corner3) < rg.wdist(self.location, corner1):
        if rg.wdist(self.location, corner3) < rg.wdist(self.location, corner2):
            if rg.wdist(self.location, corner3) < rg.wdist(self.location, corner4):
                return corner3
    else:
        return corner4

# Suicide, but only if its worth it, bro - Method borrowed from Khal Robo, borrowed from ExSpace
def HonorableDeath(self, game):
        # if there are 3+ enemies around, suicide! (code stolen from the ExSpace robot because this is my first day using python)
        aroundE = 0
        for loc, bot in game.robots.items():
            if bot.player_id != self.player_id:
                if rg.wdist(loc, self.location) <= 1:
                    aroundE += 1
        if aroundE >= 3 and self.hp < 41:
            print "kaboom (3+)"
            self.botSuicide += 1
            return True
        # if health is low, suicide for fewer enemies
        if aroundE == 2 and self.hp < 21:
            self.botSuicide += 1
            print "kaboom (2)"
            return True

# Is enemy in the center?
def IsCenterAvailable(self,game):
    for loc,bot in game.robots.items():
        if bot.player_id != self.player_id:
            if self.location == rg.CENTER_POINT:
                return False
            else:
                return True

# find closest enemy - Method from space-cadet
def GetClosestEnemy(self):
    for loc, bot in self.game.get('robots').items():
        if bot.player_id != self.player_id:
            if rg.wdist(loc, self.location) <= rg.wdist(self.location, self.closestEnemy):
                self.closestEnemy = loc
                #print "Enemy = %d, %d" %self.closestEnemy
    return self.closestEnemy


# find closest friend - Method from space-cadet
def GetClosestFriendly(self):
    for loc, bot in self.game.get('robots').items():
        if bot.player_id == self.player_id:
            if rg.wdist(loc, self.location) <= rg.wdist(self.location, self.closestFriend):
                self.closestFriend = loc
                #print "Friend = %d" %self.closestFriend
    return self.closestFriend

# Returns list of all enemy locations - Hat tip towards Khal Robo
def EnemyLocations(self,game):
    enemyLocs = []
    for loc, bot in game.robots.items():
        if bot.player_id != self.player_id:
            enemyLocs += loc
    #print enemyLocations
    return enemyLocs

# Run away!!!
def ItsNotWorthItBro(self,game):
    for loc,bot in game.robots.items():
        if bot.player_id == self.player_id:
            if self.hp < 20:
                if rg.wdist(loc, GetClosestEnemy(self)) <= 1:
                    if rg.wdist(loc, GetClosestFriendly(self)) > 1:
                        print "Just walk away bro, it's not worth it"
                        return True

# Returns a list of adjacent areas
def listOfGoodMoves(loc):
    GoodLocsAround = []
    GoodLocsAround = rg.locs_around(loc, filter_out=('invalid', 'obstacle'))
    #print "List of good locations to move to: ", GoodLocsAround
    return GoodLocsAround

# Just prints suicide stats
def SuicideStats(self,stat):
    print "%d bots died honorably" %stat


#TODO Get out of spawn better
#Check to see if bot is in spawn and spawn-turn coming up.
def SpawnKillCheck(self,game):
    if game.turn % 10 in [8, 9, 0] and 'spawn' in rg.loc_types(self.location) and game.turn < 95:
        return True

# Method that converts a bad move into a good one (think spin-move around defender in football/basketball)
def SpinMove(self,game,loc):
    randomMoveMod = [-1, 1]
    if self.location[0] == loc[0]:
        juke = loc[0], loc[1]+random.choice(randomMoveMod)
    else:
        juke = loc[0]+random.choice(randomMoveMod), loc[1]
    print "JUKED!"
    return juke


# Prediction method, returns a location that would be the shortest path between your bot and the closestEnemy
def TheForce(self,game,myLoc, enemyLoc):
    possibleMoves = []
    bestPrediction = 0
    bestMoveSoFar = 100
    possibleMoves = listOfGoodMoves(enemyLoc)
    for loc in possibleMoves:
        if rg.wdist(self.location, loc) < bestMoveSoFar:
            bestPrediction = loc
    return bestPrediction

# I love being a turtle!
def TurtleMode(self,game):
    for loc,bot in game.robots.items():
        if bot.player_id == self.player_id:
            if self.hp < 15:
                if rg.wdist(loc, GetClosestEnemy(self)) == 1:
                    if rg.wdist(loc, GetClosestFriendly(self)) > 1:
                        print "Bot at %d %d entered turtle mode" %self.location
                        return True

class Robot:

    botSuicide = 0
    def act(self, game):

        #Create list of enemy locations
        self.enemyLocations = EnemyLocations(self,game)

        #Initial vars for closestEnemy/Friend
        self.closestEnemy = (1000, 1000)
        self.closestFriend = (1000, 1000)
        self.game = game
        #print EnemyLocations(self,game)

        ####### Print Stats #######
        if game.turn == 99:
            SuicideStats(self,self.botSuicide)

        ####### Actions Prioritized Highest to Lowest #######

        # If spawn turn coming up, check if in spawn and make a good move toward center
        #(Old) If spawn turn coming up, try to go to Center
        if SpawnKillCheck(self,game):
            # first, check if move toward center is where an enemy is standing, SpinMove
            if ['move', rg.toward(self.location, rg.CENTER_POINT)] in self.enemyLocations:
                print "Don't spawn kill me, bro!"
                return ['move', rg.toward(self.location, SpinMove(rg.CENTER_POINT))]
            # if move is clear, just move
            else:
                return ['move', rg.toward(self.location, rg.CENTER_POINT)]

        #If low on health and close to enemy, suicide
        if HonorableDeath(self, game):
            return ['suicide']

        if TurtleMode(self,game):
            print "Don't hurt me, bro!"
            return ['guard']

        #If you think an enemy might move adjacent, attack the square

        #If an enemy is close, Attack
        #print "self.location, GetClosestEnemy", self.location, " ", GetClosestEnemy(self)
        if rg.wdist(self.location, GetClosestEnemy(self)) == 1:
            return ['attack', GetClosestEnemy(self)]

        # Get 1 square away from enemy, then attack square that enemy may move to.
        # Determine if enemy is 2 paces away (i.e., one pace before striking distance)
        # space-cadet, with prediction - 15-5, 12-6 | Without 10-3, 10-3
        # StarBot with - 18-8, 18-8| Without 11-4, 17-2
        if rg.wdist(self.location, GetClosestEnemy(self)) == 2:
            #determine most probable move enemy will take toward you
            print "Predicting enemy will move to  (%d %d)" %TheForce(self, game, self.location, GetClosestEnemy(self))
            return ['attack', rg.toward(self.location, TheForce(self, game, self.location, GetClosestEnemy(self)))]

        #If an enemy is not close, move towards one, or just move towards center if obstacle in the way
        #check if enemy is more than one pace away
        if rg.wdist(self.location, GetClosestEnemy(self)) > 1:
            #if step towards enemy is normal, make the move
            if rg.toward(self.location, GetClosestEnemy(self)) in listOfGoodMoves(self.location):
                print "Moving toward %d %d" %GetClosestEnemy(self)
                return ['move', rg.toward(self.location, GetClosestEnemy(self))]
            #if step is invalid, or obstacle, SpinMove will modify it one way or the other.
            else:
                if listOfGoodMoves(self.location)[0]:
                    return ['move', rg.toward(self.location, SpinMove(GetClosestEnemy(self)))]
                    #old return ['move', rg.toward(self.location, rg.CENTER_POINT)]
        print "Nothing to do, guarding"
        return ['guard']