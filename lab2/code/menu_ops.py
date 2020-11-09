import time
import datetime

def isTimeFormat(input):
    try:
        time.strptime(input, '%H:%M:%S')
        return True
    except ValueError:
        return False


def table_choice(cursor):
    cursor.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE (table_schema = 'public') ORDER BY table_schema, table_name;")
    tables = cursor.fetchall()

    integ = ''
    digit = False
    for table in tables:
      print(table[1])
    while digit == False:
        integ = input('Choose correctly table index: ')
        try: 
            integ = int(integ)
            if (int(integ) > len(tables) - 1 or int(integ) < 0) : digit = False
            else: digit = True
        except ValueError:
            digit = False

    chosen = tables[integ][1]
    # print(str(int(choice)))
    print("Chose " + str(chosen))
    return str(chosen)


def format_check(format, value):
    if format == 'integer' or format == 'bigint':
        return value.isdigit()
    elif format == 'character varying':
        return isinstance(value, str)
    elif format == 'boolean':
        return value == 'True' or value == 'False' or value == 'true' or value == 'false'
    elif format == 'time without time zone':
        return isTimeFormat(value)
    else: 
        return False


def get_generation_amount():
    digit = False
    integ = ''
    while digit == False:
        integ = input('Enter correctly amount of new rows: ')
        try: 
            integ = int(integ)
            digit = True
        except ValueError:
            digit = False
    return integ



def random_value_by_type(format):
    if format == 'integer' or format == 'bigint':
        return 'floor(random() * 100 + 1)::int'
    elif format == 'character varying':
        return 'substr(md5(random()::text), 0, floor(random() * 15)::int)'
    elif format == 'boolean':
        return '(round(random())::int)::boolean'
    elif format == 'time without time zone':
        return "time '20:00:00' + random() * (time '20:00:00' - time '10:00:00')"
    else: 
        return False  

def table_row_generation(amount, table, con, columns):
    #boolean
    #select (round(random())::int)::boolean
    
    #int
    #floor(random() * 100 + 1)::int

    #string
    #substr(md5(random()::text), 0, floor(random() * 15)::int)

    #time
    #time '20:00:00' + random() * (time '20:00:00' - time '10:00:00')
    request = 'INSERT INTO ' + table + ' ('
    names, types = zip(*columns)
    for name in names:
        request = request + name + ", "
    request = request[:-2]
    request = request + ") VALUES "

    valuelist = ''
    values = ''
    for _ in range(amount):
        values = ''
        for typ in types:
            value = random_value_by_type(typ)
            values = values + value + ', '
        values = values[:-2]
        values = "(" + values + ")"
        valuelist = valuelist + values + ",\n"
    valuelist = valuelist[:-2]
    valuelist = valuelist + ";"
    request = request + valuelist
    error_catching(request, con)



# INSERT INTO table_name (column_list)
# VALUES
#     (value_list_1),
#     (value_list_2),
#     ...
#     (value_list_n);


    #generating and appending X lists
    #lists composed by looking at columns and types
    #and checking with each type


    #after that appending to main string


def show_columns(tableName, cursor):    
    string = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = \'" + tableName + "\';"
    cursor.execute(string)
    columns = cursor.fetchall()
    print("Those are the columns:")
    for column in columns:
        print('[{0}] {1}'.format(column[1], column[0]), end=" | ")
    print();
    columns.pop(0)
    return columns

def get_column_names_only(columns):
    newlist = [] * len(columns)
    for entry in columns:
        newlist.append(entry[0])
    return newlist

def column_data_input(columns, cursor):
    correctFormat = True;
    data = ''
    receivedVals = [] * len(columns)
    for column in columns:
        data = input('Enter value of [{0}]: '.format(column[0]))
        correctFormat = format_check(str(column[1]), data)
        while correctFormat == False:
            data = input('Enter correct value of [{0}]: '.format(column[0]))
            correctFormat = format_check(str(column[1]), data)
        if str(column[1]) == 'time without time zone':
            data = "\'" + data + "\'::time"
        elif str(column[1]) == 'character varying':
            data = "\'" + data + "\'"
        receivedVals.append(data)

    return receivedVals


def print_all_values(tableName, cursor):
    string = "SELECT * FROM " + tableName + " ORDER BY id"
    cursor.execute(string)
    entries = cursor.fetchall()
    for entry in entries:
        print(print_row(entry))
    return entries

def print_row(row):
    string = "[" + str(row[0]) + "]"
    i = 1
    while i < len(row):
        string = string + " | " + str(row[i])
        i = i + 1
    return string


def form_string_from_list(listing):
    newstring = ""
    for element in listing:
        newstring = newstring + element + ", "
    newstring = newstring[:-2]
    return newstring


def insert_new_values(table, columns, values, con):
    column_names = form_string_from_list(get_column_names_only(columns))
    input_names = form_string_from_list(values)
    print(column_names)
    print(input_names)
    string = "INSERT INTO " + table + " (" + column_names + ")" + " VALUES (" + input_names + ")"
    error_catching(string, con)
    

def row_data_edit(rows, columns, table):
    correctFormat = True;
    data = ''
    row = list(rows)
    rowId = row[0]
    row.pop(0)
    receivedVals = [] * len(row)
    print("Leave input empty if you don't want to change anything.")
    i = 0
    columns2 = []

    for col in columns:
        columns2.append(col[0])

    for entry, column in zip(row, columns):
        data = input('Enter value of [{0}]: '.format(column[0]))
        if data == "": 
            columns2.pop(i)
        else:
            correctFormat = format_check(str(column[1]), data)
            while correctFormat == False:
                data = input('Enter correct value of [{0}]: '.format(column[0]))
                correctFormat = format_check(str(column[1]), data)
            if str(column[1]) == 'time without time zone':
                data = "\'" + data + "\'::time"
            elif str(column[1]) == 'character varying':
                data = "\'" + data + "\'"
            receivedVals.append(data)
            data = ''
            i = i + 1

    if len(receivedVals) > 0 and len(columns2) > 0:
        receivedVals.insert(0, rowId)
        columns2.insert(0, 'id')

    #UPDATE table_stations SET name = 'Oakenfold', availability = True WHERE id = 1
    tuples = list(zip(columns2, receivedVals))
    print(tuples)
    return tuples


def updating_row(con, values, table):
    rowId = values[0][1]
    values.pop(0)
    command = ''
    for entry in values:
        command = command + entry[0] + " = " + entry[1] + ", "
    command = command[:-2]
    command = "UPDATE " + table + " SET " + command + " WHERE id = " + str(rowId)
    error_catching(command, con)

def choosing_row(cursor, table):
    entries = print_all_values(table, cursor)
    rowId = input('Enter id of needed row or -1 to quit: ')
    if rowId == '-1': return -1
    found = False
    for entry in entries:
        if str(entry[0]) == rowId: 
            found = True
            return entry
    if found == False:
        kek = input("No such id was found. Returning.")
        return -1
    return -1

#-- INSERT into table_routes (trainId, departureId, arrivalId, departureTime, arrivalTime, lastStation) VALUES (321, 53, 123, '12:00:00'::time, '14:00:00'::time, 241)
#DELETE FROM table_stations WHERE id = 4;
def row_removal(rowId, table, con):
    data = input('Are you suure? (y/n) ')
    while data != 'y' and data != 'n':
        data = input('Be more responsible! (y/n) ')
    if data == 'y':
        command = "DELETE FROM " + table + " WHERE id = " + str(rowId)
        
        error_catching(command, con)
        print("Row removed!")
    else:
        print("Aight then! I won't touch that!")

def search_request(table, columns):
    #a cycle of requesting an attribute:
    columns.insert(0, ('id', 'bigint'))
    # print(columns)
    names, types = zip(*columns)
    #generating a list of tuples: name, format, value
    requests = []
    final_req = 'SELECT * FROM ' + table + ' WHERE '
    stop = False
    while stop == False:
        data = input('Proceed with formulating search request?\nPrint y or n: ')
        while data != 'y' and data != 'n':
            data = input('Be more responsible! (y/n) ')
        if data == 'n':
            stop = True
            continue

        found = False
        i = 0
        while found == False:
            data = input('Print correct name of any column: ')
            found = True
            # for entry in columns:
            try:
                i = names.index(data)
            except ValueError as e:
                found = False
        request = search_attributes(types[i], names[i])
        requests.append(request)
    i = 0
    if len(requests) > 0:
        for req in requests:
            if i == len(requests) - 1:
                final_req = final_req + req
            else:
                final_req = final_req + req + " AND "
            i = i + 1
    print(final_req)
    return final_req


def search_table(request, cursor):
    starttime = time.time()
    cursor.execute(request)  
    exeqtime = time.time() - starttime
    print(exeqtime)
    entries = cursor.fetchall()
    for entry in entries:
        print(print_row(entry))
    return entries



def error_catching(request, con):
    try:
        con.cursor().execute(request)
        con.commit()
    except Exception as err:
        print ("Oops! An exception has occured:", err)
        print ("Try again later.")



def search_attributes(format, name):
#SELECT * FROM table WHERE
    string = name
    #
    if format == 'integer' or format == 'bigint':
        int1 = -1
        digit = False
        while digit == False:
            int1 = input('Enter correctly the first integer: ')
            try: 
                int1 = int(int1)
                digit = True
            except ValueError:
                digit = False
        
        int2 = -1
        digit = False
        while digit == False:
            int2 = input('Enter correctly the second integer: ')
            try: 
                int2 = int(int2)
                digit = True
            except ValueError:
                digit = False
        
        integer = -1

        if int1 == int2:
            string = string + " = " + str(int1)
            return string
        elif int1 > int2: 
            integer = (int2, int1)
        else:
            integer = (int1, int2)
        string = string + " BETWEEN " + str(integer[0]) + " AND " + str(integer[1])
        return string
    #

    #
    elif format == 'character varying':
        data = ""
        while data == "":
            data = input('Enter non-empty string: ')
        data = "'%" + data + "%'"
        string = string + " ILIKE " + data
        return string
    #

    #
    elif format == 'boolean':
        data = ""
        while data != 'True' and data != 'False' and data != 'true' and data != 'false':
            data = input('Enter correct boolean string: ')
        string = string + " = " + data
        return string
    #

    #
    elif format == 'time without time zone':
        time1 = ""
        while isTimeFormat(time1) == False:
            time1 = input('Enter time1 in format HH:MM:SS : ')

        time2 = ""
        while isTimeFormat(time2) == False:
            time2 = input('Enter time2 in format HH:MM:SS : ')

        timestring1 = "'" + time1 + "'::time"
        timestring2 = "'" + time2 + "'::time"

        timeval = ()

        if time.strptime(time1, '%H:%M:%S') == time.strptime(time2, '%H:%M:%S'):
            string = string + " = " + timestring1
            return string
        elif time.strptime(time1, '%H:%M:%S') > time.strptime(time2, '%H:%M:%S'): 
            timeval = (timestring2, timestring1)
        else:
            timeval = (timestring1, timestring2)
        
        string = string + " BETWEEN " + timeval[0] + " AND " + timeval[1]
        return string
    #

    else: 
        return False