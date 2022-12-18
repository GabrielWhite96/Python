from assets.util import *

class Dice:
    
    def __init__(self, value_dice):
        self.__value_dice = value_dice
        self.__rolled_dice = None
    
    def roll_dice(self):
        self.__rolled_dice = generate_random_number(1, self.__value_dice)
    
    def dice(self):
        return str(self.__rolled_dice)
    
    @property
    def rolled_dice(self):
        return self.__rolled_dice
    
if __name__ == '__main__':
    dice = Dice(6)
    print(dice.dice())
