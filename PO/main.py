def read_file(path):
    with open(path, 'r') as file:
        return file.read().split('/n')

def create_matrix(base_list: list):
    matrix = []
    for i, line in enumerate(base_list):
        cells = []