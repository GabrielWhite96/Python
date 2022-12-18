from breeds.Elf import Elf
from breeds.Half_orc import Half_orc
from breeds.Human import Human

class Breed:
    
  def __init__(self):
    self.__selected_breed =  None 
    self.__select_breed()
    
  @property
  def selected_breed(self):
    return self.__selected_breed

  def __select_breed(self):
    user_choice = int(input("Informe a raça desejada: "))
    if user_choice == 1:
      self.__selected_class = Human()
    if user_choice == 2:
      self.__selected_class = Half_orc()
    if user_choice == 3:
      self.__selected_class = Elf()