from consolemenu import *
from consolemenu.items import *


class View:
    def print(self, data):
        columns, rows = data
        lineLen = 30 * len(columns)

        self.printSeparator(lineLen)
        self.printRow(columns)
        self.printSeparator(lineLen)

        for row in rows:
            self.printRow(row)
        self.printSeparator(lineLen)

    def printRow(self, row):
        for col in row:
            print(str(col).rjust(26, ' ') + '   |', end='')
        print('')

    def printSeparator(self, length):
        print('-' * length)

