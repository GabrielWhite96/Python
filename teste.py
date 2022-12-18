from assets.util import *

receive_answer = lambda: input("Digite o código dos dados (numero de dados + letra d + valor do dado): ")

def format_answer(answer):
    result = answer.replace(' ', '').lower().split('d')
    dices = {
        'number_dices': int(result[0]),
        'value_dices': int(result[1])
    }
    return dices

def roll_dice(value_dice):
    return generate_random_number(1, value_dice)
    
def roll_dices(dice):
    return [roll_dice(dice['value_dices']) for _ in range(dice['number_dices'])]
        
def format_result(formated_dices, dices):
    dices_str = [str(n) for n in dices]
    print(str(formated_dices['number_dices']) + 'd' + str(formated_dices['value_dices']) , ' = {' , ', '.join(dices_str) , '} = ' , sum(dices))

def menu_dice():
    formated_dices = format_answer(receive_answer())
    dices = roll_dices(formated_dices)
    format_result(formated_dices, dices)
    return sum(dices)
    
menu_dice()    