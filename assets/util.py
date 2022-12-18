from random import randint

def generate_random_number(initial_value, final_value):
    result = randint(initial_value, final_value)
    return result

# for i in range(10):print(generate_random_number(10,20))