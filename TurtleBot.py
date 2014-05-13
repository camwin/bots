import rg, random

#TODO Make bots more efficient killers - Redo attack closest enemy

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

# I love being a turtle!
def TurtleMode(self,game):
    for loc,bot in game.robots.items():
        if bot.player_id == self.player_id:
            if self.hp < 15:
                if rg.wdist(loc, GetClosestEnemy(self)) == 1:
                    if rg.wdist(loc, GetClosestFriendly(self)) > 1:
                        print "Bot at %d %d entered turtle mode" %self.location
                        return True

def GetSPF(self,game):
    return True

#Check to see if bot is in spawn and spawn-turn coming up.
def SpawnKillCheck(self,game):
    if game.turn % 10 in [8, 9, 0] and 'spawn' in rg.loc_types(self.location) and game.turn < 95:
        return True


class Robot:
    botSuicide = 0
    def act(self, game):
        self.closestEnemy = (1000, 1000)
        self.closestFriend = (1000, 1000)
        self.game = game

        ####### Print Stats #######
        if game.turn == 99:
            SuicideStats(self,self.botSuicide)

        ####### Actions Prioritized Highest to Lowest #######

        #Move to center right off the bat
        #if game.turn <= 5:
         #   if IsCenterAvailable(self,game):
          #     print "Moving toward center"
           #    return ['move', rg.toward(self.location, rg.CENTER_POINT)]

        #If spawn turn coming up, try to go to Center
        if SpawnKillCheck(self,game):
            print "Dont spawn kill me, bro!"
            return ['move', rg.toward(self.location, rg.CENTER_POINT)]

        #If low on health and close to enemy, suicide
        if HonorableDeath(self, game):
            return ['suicide']

        #if ItsNotWorthItBro(self,game):
         #   print "Limping to: " ClosestCorner(self,game)
          #  return ['move', rg.toward(self.location, ClosestCorner(self,game))]

        if TurtleMode(self,game):
            print "Don't hurt me, bro!"
            return ['guard']

        #If an enemy is close, Attack
        #print "self.location, GetClosestEnemy", self.location, " ", GetClosestEnemy(self)
        if rg.wdist(self.location, GetClosestEnemy(self)) == 1:
            return ['attack', GetClosestEnemy(self)]
        
        #If an enemy is not close, move towards one, or just move towards center if obstacle in the way
        if rg.wdist(self.location, GetClosestEnemy(self)) > 1:
            if rg.toward(self.location, GetClosestEnemy(self)) in listOfGoodMoves(self.location):
                print "Moving toward (%d %d)" %GetClosestEnemy(self)
                return ['move', rg.toward(self.location, GetClosestEnemy(self))]
            else:
                if listOfGoodMoves(self.location)[0]:
                    print "No good moves available. Moving to Center."
                    return ['move', rg.toward(self.location, rg.CENTER_POINT)]
        print "Nothing to do, guarding"
        return ['guard']