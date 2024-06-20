from consolemenu import *
from consolemenu.items import *


class View:
    def __init__(self):
        self.SEPARATOR_WIDTH = 30

    def print_entities(self, table_name, data):
        separator_line = '-' * self.SEPARATOR_WIDTH

        print(f'Table :  `{table_name}`', end='\n\n')
        for entity in data:
            print(entity)

