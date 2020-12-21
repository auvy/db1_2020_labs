import psycopg2
import model

def insert(cursor, con):
    chosen_table = model.table_choice(cursor)
    columns = model.show_columns(chosen_table, cursor)
    
    vals = model.column_data_input(columns, cursor)
    model.insert_new_values(chosen_table, columns, vals, con)


def update(cursor, con):
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
    

def delete(cursor, con):
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