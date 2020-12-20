import psycopg2
import model
import controller

con = psycopg2.connect(
  database="postgres", 
  user="postgres", 
  password="PASSWORD", 
  host="127.0.0.1", 
  port="5432"
)

cursor = con.cursor()

import os

instance = True
menu = '0'
choice = ''
os.system('clear')
while instance == True:    
#
  choice = ''
  if menu == '0':
  #
    os.system('clear')
    print("\n[1] Add row")
    print("[2] Edit row")
    print("[3] Remove row")
    print("[4] Generate data")
    print("[5] Search for data")
    print("[Any button] Quit")
    
    menu = input("What would you like to do? ")
    
    os.system('clear')
  
  elif menu == '1':
  #
    os.system('clear')
    
    print("[1] Adding a new row")
    # chosen_table = model.table_choice(cursor)
    # columns = model.show_columns(chosen_table, cursor)
    # vals = model.column_data_input(columns, cursor)
    # model.insert_new_values(chosen_table, columns, vals, con)
    
    controller.row_addition(cursor, con)


    input("Seems that the insertion was successful. Press any key.") 
    menu = '0'
    continue
  #

  #
  elif menu == '2':
    os.system('clear')
    
    print("[2] Editing existing row")  
    # chosen_table = model.table_choice(cursor)
    # columns = model.show_columns(chosen_table, cursor)
    # row = model.choosing_row(cursor, chosen_table)
    # if row != -1:
    #   values = model.row_data_edit(row, columns, chosen_table)
    #   if len(values) > 0:  
    #     model.updating_row(con, values, chosen_table)
    #     choice = input("Success!. Press any key.")
    #   else:
    #     print("There was nothing to change. Press any key.")
    
    controller.row_editing(cursor, con)
    input()
    menu = '0'
    continue
  #

  #
  elif menu == '3':
    os.system('clear')
    
    print("[3] Removing existing row")  
    # chosen_table = model.table_choice(cursor)
    # columns = model.show_columns(chosen_table, cursor)
    # row = model.choosing_row(cursor, chosen_table)
    # if row != -1:
    #   model.row_removal(row[0], chosen_table, con)
    controller.row_removal(cursor, con)

    input()
    menu = '0'
    continue
  #


  #
  elif menu == '4':
    os.system('clear')
    print("[4] Random values generation")  
    # chosen_table = model.table_choice(cursor)
    # columns = model.show_columns(chosen_table, cursor)
    # gen = model.get_generation_amount()

    # model.table_row_generation(gen, chosen_table, con, columns)

    controller.random_gen(cursor, con)
    input()
    menu = '0'
    continue
  #

  #
  elif menu == '5':
    os.system('clear')
    print("[5] Formulating search request")  
    # chosen_table = model.table_choice(cursor)
    # columns = model.show_columns(chosen_table, cursor)
    # search = model.search_request(chosen_table, columns)
    # model.search_table(search, cursor)
    controller.value_search(cursor, con)

    input("Press any button")
    menu = '0'
    continue
  #

  else:
    instance = False
#
con.close()
        
