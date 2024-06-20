from consolemenu import SelectionMenu

from model import Model
from view import View
import time;

TABLES_NAMES = ['buyer', 'order_item', 'order', 'product']
TABLES = {
'buyer': ['id', 'email', 'name', 'hashed_password', 'city', 'postal_code'],
'order_item': ['id', 'order_id', 'amount', 'product_id'],
'order': ['id', 'date', 'buyer_id'],
'product': ['id', 'name', 'description', 'price', 'total_quantity']
}

def getInput(msg, tableName = ''):
    print(msg)
    if tableName:
        print(' | '.join(TABLES[tableName]), end='\n\n')
    return input()

def getInsertInput(msg, tableName):
    print(msg)
    print(' | '.join(TABLES[tableName]), end='\n\n')
    return input(), input()

def pressEnter():
    input()

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def show_init_menu(self, msg=''):
        selectionMenu = SelectionMenu(
        TABLES_NAMES + ['Fill table "product" by random data (10 items)', 'Find buyers by criteria',
        'Find orders by criteria', 'Find products by criteria'], title='Select the table to work with | command:', subtitle=msg)
        selectionMenu.show()

        index = selectionMenu.selected_option
        if index < len(TABLES_NAMES):
            tableName = TABLES_NAMES[index]
            self.show_entity_menu(tableName)
        elif index == 4:
            self.fillByRandom()
        elif index == 5:
            self.searchByersByCriteria()
        elif index == 6:
            self.searchOrdersByCriteria()
        elif index == 7:
            self.searchProductsByCriteria()
        else:
            print('Exiting...')

    def show_entity_menu(self, tableName, msg=''):
        options = ['Get', 'Delete', 'Update', 'Insert']
        functions = [self.get, self.delete, self.update, self.insert]

        selectionMenu = SelectionMenu(options, f'Name of table: {tableName}',
        exit_option_text='Back', subtitle=msg)
        selectionMenu.show()
        try:
            function = functions[selectionMenu.selected_option]
            function(tableName)
        except IndexError:
            self.show_init_menu()

    def get(self, tableName):
        try:
            condition = getInput(
            f'GET {tableName}\nEnter condition (SQL) or leave empty:', tableName)
            data = self.model.get(tableName, condition)
            self.view.print(data)
            pressEnter()
            self.show_entity_menu(tableName)
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def insert(self, tableName):
        try:
            columns, values = getInsertInput(
            f"INSERT {tableName}\nEnter columns divided with commas, then do the same for values in format: ['value1', 'value2', ...]", tableName)
            self.model.insert(tableName, columns, values)
            self.show_entity_menu(tableName, 'Insert is successful!')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def delete(self, tableName):
        try:
            condition = getInput(
            f'DELETE {tableName}\n Enter condition (SQL):', tableName)
            self.model.delete(tableName, condition)
            self.show_entity_menu(tableName, 'Delete is successful')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def update(self, tableName):
        try:
            condition = getInput(
            f'UPDATE {tableName}\nEnter condition (SQL):', tableName)
            statement = getInput(
            "Enter SQL statement in format [<key>='<value>']", tableName)

            self.model.update(tableName, condition, statement)
            self.show_entity_menu(tableName, 'Update is successful')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def searchByersByCriteria(self):
        try:
            city = getInput(
            'Find buyers from city that begins on: \nEnter city:')
            name = getInput(
                'with name that begins on: \nEnter name:')
            amount = getInput(
                'Find buyers that have order with amount of product more than: \nEnter product amount:')

            time_start = time.perf_counter()
            data = self.model.searchByersByCriteria(city, name, amount)
            time_end = time.perf_counter()
            self.view.print(data)
            print(f'\ntime elapsed: {time_end-time_start:0.4f} seconds')
            pressEnter()
            self.show_init_menu()
        except Exception as err:
            self.show_init_menu(str(err))

    def searchOrdersByCriteria(self):
        try:
            city = getInput(
            'Find orders from buyers from city that begins on: \nEnter city:')
            postal_code = getInput(
                'with postal code: \nEnter postal code:')
            name = getInput(
                'with this buyers name starting on: \nEnter name:')

            time_start = time.perf_counter()
            data = self.model.searchOrdersByCriteria(city, name, postal_code)
            time_end = time.perf_counter()
            self.view.print(data)
            print(f'\ntime elapsed: {time_end - time_start:0.4f} seconds')
            pressEnter()
            self.show_init_menu()
        except Exception as err:
            self.show_init_menu(str(err))

    def searchProductsByCriteria(self):
        try:
            price = getInput(
            'Find orders of product that have price more than: \nEnter price:')
            total_quantity = getInput(
                'with total quantity of that product more than: \nEnter total quantity:')
            amount = getInput(
                'And amount of product in order is more than: \nEnter product amount:')

            time_start = time.perf_counter()
            data = self.model.searchProductsByCriteria(price, amount, total_quantity)
            time_end = time.perf_counter()
            self.view.print(data)
            print(f'\ntime elapsed: {time_end - time_start:0.4f} seconds')
            pressEnter()
            self.show_init_menu()
        except Exception as err:
            self.show_init_menu(str(err))

    def fillByRandom(self):
        try:
            self.model.fillProductByRandomData()
            self.show_init_menu('Generated successfully')

        except Exception as err:
            self.show_init_menu(str(err))
