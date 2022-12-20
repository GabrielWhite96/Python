from breeds.Breed import Breed
from charactersClass.Barbarian import Barbarian
from charactersClass.Classe import Classe
from charactersClass.Mage import Mage
from charactersClass.Ranger import Ranger
from functionality.Dice import *
from functionality.Shot_dices import Shot_dices


class Character:

  def __init__(self):
    self.__Level = 0
    self.__name = ""
    self.__age = 0
    self.__height = 0
    self.__weight = 0
    self.__health = 0
    self.__lvl_armor = 0
    self.__strength = 0
    self.__dexterity = 0
    self.__constitution = 0
    self.__intelligence = 0
    self.__wisdom = 0
    self.__charisma = 0
    self.__Classe = Classe()
    self.__Breed = Breed()
    self.fill_infos()

  def fill_name(self):
    self.__name = input("Nome:")

  def fill_age(self):
    self.__age = input("Idade:")

  def fill_height(self):
    self.__height = input("Altura (em cm):")

  def fill_weight(self):
    self.__weight = input("Peso (em grama):")

  def fill_health(self):
    if type(self.__Classe.selected_class) == type(Barbarian()):
      self.__health = 12 + self.__constitution
    elif type(self.__Classe) == type(Mage()):
      self.__health = 6 + self.__constitution
    elif type(self.__Classe) == type(Ranger()):
      self.__health = 10 + self.__constitution
    
  def fill_lvl_armor(self):
    if type(self.__Classe.selected_class) == type(Barbarian()):
      self.__lvl_armor == 10 + self.__constitution + self.__dexterity
    else:
      self.__lvl_armor == 10 + self.__dexterity    
  
  def fill_strength(self, dices_list):
    user_choice = int(input("Dado para força: "))
    self.__strength = int(dices_list[user_choice])

  def __dice_list_to_list(self, dice_list):
    return dice_list.split(';')
  
  def fill_atributes(self):
    list_rolled_dices = Shot_dices('6d20')
    print(list_rolled_dices.dices_list)
    print(self.__dice_list_to_list(list_rolled_dices.dices_list))
    self.fill_strength(list_rolled_dices.dices_list)
    # self.fill_dexterity()
    # self.fill_constitution()
    # self.fill_intelligence()
    # self.fill_wisdom()
    # self.fill_charisma()

  def fill_infos(self):
    # self.fill_name()
    # self.fill_age()
    # self.fill_height()
    # self.fill_weight()
    # self.fill_health()
    # self.fill_lvl_armor()
    self.fill_atributes()

if __name__ == '__main__':

  aux = Character()