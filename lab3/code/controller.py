import psycopg2
import model

def row_addition(cursor, con):
    chosen_table = model.table_choice(cursor)
    columns = model.show_columns(chosen_table, cursor)
    
    vals = model.column_data_input(columns, cursor)
    model.insert_new_values(chosen_table, columns, vals, con)


def row_editing(cursor, con):
    chosen_table = model.table_choice(cursor)
    columns = model.show_columns(chosen_table, cursor)
    
    row = model.choosing_row(cursor, chosen_table)
    if row != -1:
      values = model.row_data_edit(row, columns, chosen_table)
      if len(values) > 0:  
        model.updating_row(con, values, chosen_table)
        choice = input("Success!. Press any key.")
      else:
        print("There was nothing to change. Press any key.")
    

def row_removal(cursor, con):
    chosen_table = model.table_choice(cursor)
    columns = model.show_columns(chosen_table, cursor)
    
    row = model.choosing_row(cursor, chosen_table)
    if row != -1:
      model.row_removal(row[0], chosen_table, con)

def random_gen(cursor, con):
    chosen_table = model.table_choice(cursor)
    columns = model.show_columns(chosen_table, cursor)
    
    gen = model.get_generation_amount()
    model.table_row_generation(gen, chosen_table, con, columns)


def value_search(cursor, con):
    chosen_table = model.table_choice(cursor)
    columns = model.show_columns(chosen_table, cursor)
    
    search = model.search_request(chosen_table, columns)
    model.search_table(search, cursor)



#ORM

def get(tableName, cursor):
    try:
        data = model.get(tableName, condition)
        view.print_entities(tableName, data)
        pressEnter()
        show_entity_menu(tableName)
    except Exception as err:
        show_entity_menu(tableName, str(err))

def insert(cursor, tableName):
    try:
        columns, values = getInsertInput(
            f"INSERT {tableName}\nEnter columns divided with commas, then do the same for values in format: ['value1', 'value2', ...]", tableName)
        model.insert(tableName, columns, values)
        show_entity_menu(tableName, 'Insert is successful!')
    except Exception as err:
        show_entity_menu(tableName, str(err))

def delete(cursor, tableName):
    try:
        condition = getInput(
            f'DELETE {tableName}\n Enter condition (SQL):', tableName)
        model.delete(tableName, condition)
        show_entity_menu(tableName, 'Delete is successful')
    except Exception as err:
        show_entity_menu(tableName, str(err))

def update(cursor, tableName):
    try:
        condition = getInput(
            f'UPDATE {tableName}\nEnter condition (SQL):', tableName)
        statement = getInput(
            "Enter SQL statement in format [<key>='<value>']", tableName)

        model.update(tableName, condition, statement)
        show_entity_menu(tableName, 'Update is successful')
    except Exception as err:
        show_entity_menu(tableName, str(err))



