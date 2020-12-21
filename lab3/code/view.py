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
    
    controller.insert(cursor, con)

    input("Seems that the insertion was successful. Press any key.") 
    menu = '0'
    continue
  #

  #
  elif menu == '2':
    os.system('clear')
    
    print("[2] Editing existing row")  
    
    controller.update(cursor, con)
    input()
    menu = '0'
    continue
  #

  #
  elif menu == '3':
    os.system('clear')
    
    print("[3] Removing existing row")  

    controller.delete(cursor, con)

    input()
    menu = '0'
    continue
  #


  #
  elif menu == '4':
    os.system('clear')
    print("[4] Random values generation")  

    controller.random_gen(cursor, con)
    input()
    menu = '0'
    continue
  #

  #
  elif menu == '5':
    os.system('clear')
    print("[5] Formulating search request")  

    controller.value_search(cursor, con)

    input("Press any button")
    menu = '0'
    continue
  #

  else:
    instance = False
#
con.close()
        
