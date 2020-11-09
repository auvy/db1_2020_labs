import psycopg2
import menu_ops

con = psycopg2.connect(
  database="postgres", 
  user="postgres", 
  password="PASSWORD", 
  host="127.0.0.1", 
  port="5432"
)

print("Database opened successfully")

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
    chosen_table = menu_ops.table_choice(cursor)
    columns = menu_ops.show_columns(chosen_table, cursor)
    vals = menu_ops.column_data_input(columns, cursor)
    menu_ops.insert_new_values(chosen_table, columns, vals, con)
    
    input("Seems that the insertion was successful. Press any key.") 
    menu = '0'
    continue
  #

  #
  elif menu == '2':
    os.system('clear')
    
    print("[2] Editing existing row")  
    chosen_table = menu_ops.table_choice(cursor)
    columns = menu_ops.show_columns(chosen_table, cursor)
    row = menu_ops.choosing_row(cursor, chosen_table)
    if row != -1:
      values = menu_ops.row_data_edit(row, columns, chosen_table)
      if len(values) > 0:  
        menu_ops.updating_row(con, values, chosen_table)
        choice = input("Success!. Press any key.")
      else:
        print("There was nothing to change. Press any key.")
    
    input()
    menu = '0'
    continue
  #

  #
  elif menu == '3':
    os.system('clear')
    
    print("[3] Removing existing row")  
    chosen_table = menu_ops.table_choice(cursor)
    columns = menu_ops.show_columns(chosen_table, cursor)
    row = menu_ops.choosing_row(cursor, chosen_table)
    if row != -1:
      menu_ops.row_removal(row[0], chosen_table, con)
    
    input()
    menu = '0'
    continue
  #


  #
  elif menu == '4':
    os.system('clear')
    print("[4] Random values generation")  
    chosen_table = menu_ops.table_choice(cursor)
    columns = menu_ops.show_columns(chosen_table, cursor)
    gen = menu_ops.get_generation_amount()

    menu_ops.table_row_generation(gen, chosen_table, con, columns)


    input()
    menu = '0'
    continue
  #

  #
  elif menu == '5':
    os.system('clear')
    print("[5] Formulating search request")  
    chosen_table = menu_ops.table_choice(cursor)
    columns = menu_ops.show_columns(chosen_table, cursor)
    search = menu_ops.search_request(chosen_table, columns)
    menu_ops.search_table(search, cursor)

    input("Press any button")
    menu = '0'
    continue
  #

  else:
    instance = False
#
con.close()
        
