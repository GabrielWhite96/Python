from charactersClass.Barbarian import Barbarian
from charactersClass.Mage import Mage
from charactersClass.Ranger import Ranger

class Classe:

  def __init__(self):
    self.__selected_class = None 
    self.__select_class()
    
  @property
  def selected_class(self):
    return self.__selected_class
    
  def __select_class(self):
    user_choice = int(input("Informe a classe desejada: "))
    if user_choice == 1:
      self.__selected_class = Barbarian()
    elif user_choice == 2:
      self.__selected_class = Mage()
    elif user_choice == 3:
      self.__selected_class = Ranger()
      