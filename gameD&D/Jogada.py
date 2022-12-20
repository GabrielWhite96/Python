from Dice import Dice
from util import *

class Jogada:

    def __init__(self, user_answer):
        self.__user_answer = self.__format_answer(user_answer)
        self.__dices_list = self.__fill_dices_list()
        self.__roll_dices()

    @property
    def dices_list(self):
        text = "[ "
        for dice in self.__dices_list:
            text += dice.dice() 
        return text + " ]"
    
    @property
    def biggest_dice(self):
        biggest = self.__dices_list[0]
        for dice in self.__dices_list:
            if dice.rolled_dice > biggest.rolled_dice:
                biggest = dice
        return biggest

    @property
    def sum_dices(self):
        return sum([dice.rolled_dice for dice in self.__dices_list])

    def __format_answer(self, answer):
        result = answer.replace(' ', '').lower().split('d')
        return {
            'number_dices': int(result[0]),
            'value_dices': int(result[1])
        }

    def __fill_dices_list(self):
        return [Dice(self.__user_answer['value_dices']) for _ in range(self.__user_answer['number_dices'])]
    
    def __roll_dices(self):
        for dice in self.__dices_list:
            dice.roll_dice()


if __name__ == '__main__':
    aux = Jogada('4d20')
    print(aux.dices_list)