import rg, random

#TODO
# Figure out way to prevent more than one bot from locking up with an enemy. Derive way for
# bots to gang up effectively.

#TODO
# DEBUG THIS --> Add check for Friendly's blocking Friendly's SpawnCheck (and other Friendly blocks)

#TODO
# Last resort SUICIDE for those completely blocked in Spawn

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
            enemyLocs.append(loc)
    #print enemyLocations
    return enemyLocs

# Returns list of all Friendly locations
def FriendlyLocations(self,game):
    friendlyLocs = []
    for loc, bot in game.robots.items():
        if bot.player_id == self.player_id:
            friendlyLocs.append(loc)
    #print friendlyLocs
    return friendlyLocs

# Run away!!!
def ItsNotWorthItBro(self,game):
    #for loc,bot in game.robots.items():
    #    if bot.player_id == self.player_id:
    if self.hp < 20:
        if rg.wdist(self.location, GetClosestEnemy(self)) == 1:
            if rg.wdist(self.location, GetClosestFriendly(self)) > 1:
                print "Just walk away bro, it's not worth it (%d, %d)" %self.location
                return True
    else:
        return False

# Returns a list of adjacent areas
def listOfGoodMoves(loc):
    GoodLocsAround = []
    GoodLocsAround = rg.locs_around(loc, filter_out=('invalid', 'obstacle'))
    #print "List of good locations to move to: ", GoodLocsAround
    return GoodLocsAround

# Just prints suicide stats
def SuicideStats(self,stat):
    print "%d bots died honorably" %stat

#Check to see if bot is in spawn and spawn-turn coming up.
def SpawnKillCheck(self,game):
    if game.turn % 10 in [8, 9, 0] and 'spawn' in rg.loc_types(self.location) and game.turn < 95:
        return True

# Method that converts a bad move into a good one (think spin-move around defender in football/basketball)
def SpinMove(self,loc):
    randomMoveMod = [-1, 1]
    if self.location[0] == loc[0]:
        juke = loc[0]+random.choice(randomMoveMod), loc[1]
    else:
        juke = loc[0], loc[1]+random.choice(randomMoveMod)
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
    #for loc,bot in game.robots.items():
    #    if bot.player_id == self.player_id:
    if self.hp < 10:
        if rg.wdist(self.location, GetClosestEnemy(self)) == 1:
            if rg.wdist(self.location, GetClosestFriendly(self)) > 1:
                print "Bot at %d %d entered turtle mode" %self.location
                return True

class Robot:

    botSuicide = 0
    def act(self, game):

        #Create list of enemy locations
        self.enemyLocations = EnemyLocations(self,game)
        self.friendlyLocations = FriendlyLocations(self,game)

        #Initial vars for closestEnemy/Friend
        self.closestEnemy = (1000, 1000)
        self.closestFriend = (1000, 1000)
        self.game = game
        #print "Enemy List: " , self.enemyLocations
        #print "Friendly List: " , self.friendlyLocations

        ####### Print Stats #######
        if game.turn == 99:
            SuicideStats(self,self.botSuicide)

        ####### Actions Prioritized Highest to Lowest #######

        # If spawn turn coming up, check if in spawn and make a good move toward center
        #(Old) If spawn turn coming up, try to go to Center
        if SpawnKillCheck(self,game):

            # first, check if move toward center is where an enemy is standing, SpinMove
            if rg.toward(self.location, rg.CENTER_POINT) in self.enemyLocations:
                jukeAroundEnemyFromSpawn = rg.toward(self.location,SpinMove(self,rg.toward(self.location, rg.CENTER_POINT)))
                print "Enemy in the way, trying to juke to ", jukeAroundEnemyFromSpawn
                if jukeAroundEnemyFromSpawn in self.enemyLocations:
                    print "GET OFF ME BRO! Boxed in, attacking ", jukeAroundEnemyFromSpawn
                    return ['attack', jukeAroundEnemyFromSpawn]
                return ['move', jukeAroundEnemyFromSpawn]
            # next, check if move toward center is where a Friendly is standing, SpinMove
            if rg.toward(self.location, rg.CENTER_POINT) in self.friendlyLocations:
                jukeAroundFriendlyFromSpawn = rg.toward(self.location,SpinMove(self,rg.toward(self.location, rg.CENTER_POINT)))
                print "Friendly in the way, trying to juke to ", jukeAroundFriendlyFromSpawn
                return ['move', jukeAroundFriendlyFromSpawn]
            # if move is clear, just do it, bro
            else:
                print "Spawn coming up, dipping toward center from (%d, %d)" %self.location
                return ['move', rg.toward(self.location, rg.CENTER_POINT)]

        #If low on health and close to enemy, suicide
        if HonorableDeath(self, game):
            return ['suicide']

        # if no buddy is near and health is below 10 (changed from 15 5-14-14), go to guarding
        if TurtleMode(self,game):
            print "Don't hurt me, bro! (%d, %d)" %self.location
            return ['guard']

        #If an enemy is close and it's worth it, bro (you have a buddy close), Attack. Otherwise, waddle away
        #print "self.location, GetClosestEnemy", self.location, " ", GetClosestEnemy(self)
        if rg.wdist(self.location, GetClosestEnemy(self)) == 1: # ItsNotWorthItBro(self,game) == False:
            return ['attack', GetClosestEnemy(self)]

        # Get 1 square away from enemy, then attack square that enemy may move to.
        # Determine if enemy is 2 paces away (i.e., one pace before striking distance)
        # space-cadet, with prediction - 15-5, 12-6 | Without 10-3, 10-3
        # StarBot with - 18-8, 18-8| Without 11-4, 17-2
        if rg.wdist(self.location, GetClosestEnemy(self)) == 2:
            #determine most probable move enemy will take toward you
            print "Predicting enemy will move to  (%d, %d)" %TheForce(self, game, self.location, GetClosestEnemy(self))
            return ['attack', rg.toward(self.location, TheForce(self, game, self.location, GetClosestEnemy(self)))]

        #If an enemy is not close, move towards one
        #check if enemy is more than one pace away
        if rg.wdist(self.location, GetClosestEnemy(self)) > 1:
            #if step towards enemy is unblocked by friendly, make the move
            if rg.toward(self.location, GetClosestEnemy(self)) not in self.friendlyLocations:
                print "Moving toward nearest enemy via (%d, %d)" %rg.toward(self.location, GetClosestEnemy(self))
                return ['move', rg.toward(self.location, GetClosestEnemy(self))]
            #if step is blocked by friendly, SpinMove will modify it one way or the other.
            else:
                print "Friendly in the way, SpinMove around him at (%d, %d)" %rg.toward(self.location, GetClosestEnemy(self))
                return ['move', rg.toward(self.location,SpinMove(self,rg.toward(self.location, GetClosestEnemy(self))))]
                #old return ['move', rg.toward(self.location, rg.CENTER_POINT)]
        print "Nothing to do, guarding"
        return ['guard']