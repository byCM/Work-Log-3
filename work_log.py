import datetime
import sys
import csv
import os
import re
import json

def clear_screen():
    # Clears the screen after user enters the option that they would like to select
    os.system('cls' if os.name == 'nt' else 'clear')
    
def work_log():
    # Prints the opening menu, allows them to add new entry, search, or quit
    print("""
    Work Log
    What would you like to do?
    a) Add new entry
    b) Search in existing entries
    c) Quit program    
    """)
    x = input()
    clear_screen()
    
    
    if x == "a":
        new_entry()
    elif x == "b":
        search_entries()
    elif x == "c":
        sys.exit(0)
    else:
        print("That is not a valid option, please select a, b or c")
        
        
def new_entry():
    # Creates a new entry and enters it into the csv file.
    name = notes = date = time = None
    while not name or name.isspace():
        name = input("Enter the name of the task. (Press r to return to menu or x to quit) ")
    if name.lower() == "r":
        work_log()
    elif name.lower() == "x":
        sys.exit(0)
    
    date = datetime.datetime.now().strftime('%m/%d/%Y')
    
    while not time:
        try:
            time = input("Time spent on task: ")
        except ValueError:
            print("Please enter a valid number")
            
    notes = input("Enter any notes that you would like included with the task. (Optional) ")
    if notes.isspace():
        notes = None
                     
    with open('tasks.csv', 'a', newline='') as taskfile:
        fieldnames = ['name', 'date', 'time', 'notes']
        writer = csv.DictWriter(taskfile, fieldnames=fieldnames)
        
        if os.stat('tasks.csv').st_size == 0:
            writer.writeheader()
        writer.writerow({'name': name, 'date': date, 'time': time, 'notes': notes})
        
        
        clear_screen()
        print("\nTask was added!\n")
        print("Name: {} ".format(name))
        print("Time Spent: {} ".format(time))
        print("Date: {} ".format(date))
        print("Notes: {} ".format(notes))
        
    
        final_input = input("\n[D]elete, [A]dd Another, [R]eturn to search menu ")

        clear_screen()
        if final_input.lower() == 'd':
            delete_entry()
        elif final_input.lower() == 'a':
            new_entry()
        elif final_input.lower() == 'r':
            work_log()
            
            

def delete_entry():
    # Deletes entry
    edited = []
    with open('tasks.csv') as taskfile:
        reader = csv.DictReader(taskfile)
        for row in reader:
            if row == task_dict:
                continue
            else:
                edited.append(row)
    with open('tasks.csv', 'w', newline='') as taskfile:
        fieldnames = ['name', 'time', 'notes', 'date']
        writer = csv.DictWriter(taskfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in edited:
            writer.writerow({'name': row['name'], 'date': row['date'], 'time': row['time'], 'notes': row['notes']})
    print("\nEntry deleted!\n")
       

def search_entries():
    # Search option menu
    print("""
    What would you like to search by?
    a) Search by Range of Dates or a Single Date
    b) Exact Search
    c) Search by Regex Pattern
    d) Search by Time
    e) Return to Menu   
""")
    
    
    search_mode = None
    while not search_mode:
        search_mode = input('>>>').strip()
    clear_screen()
    if search_mode == "a":
        search_range()
    elif search_mode == "b":
        exact_search()
    elif search_mode == "c":
        regex_search()
    elif search_mode == "d":
        time_search()
    elif search_mode == "e":
        sys.exit()
    else:
        print("Please enter a, b, c, d or e.")
    
        

        
def input_date(date):
    while len(date) == 0:
        try:
            new_string = input('>>>')
            date.append(datetime.datetime.strptime(
                    new_string, '%m/%d/%Y'))
        except ValueError:
            print('That is not the correct format, format must be in MM/DD/YYYY. Please try again.')

            
                                               

def search_range():
    # Allows users to search for a certain date or a range of dates.
    search_date_one = []
    search_date_two = []
    search_mode = None
    while not search_mode:
        search_mode = input('Enter 1 to search a single date or 2 to search within a range of dates.\n>>>').strip()
        clear_screen()
        if search_mode not in ['1', '2']:
            print('Not a valid selection')
            search_mode = None
    print('Input {}date in format MM/DD/YYYY'.format(
          'start ' if search_mode == '2' else ''))
    input_date(search_date_one)
    if search_mode == '2':
        print('Input end date in format MM/DD/YYYY')
        while not search_date_two:
            input_date(search_date_two)
            if search_date_one[0].timestamp() > search_date_two[0].timestamp():
                print("First date can't be later than second date. Please enter the date again ")
                search_date_two = []
    # Searches 
    search_results = []
    with open('tasks.csv') as taskfile:
        reader = csv.DictReader(taskfile)
        if search_mode == '1':
            for row in reader:
                if (datetime.datetime.strptime(row['date'], '%m/%d/%Y') ==
                        search_date_one[0]):
                    search_results.append(row)
        else:
            for row in reader:
                if ((datetime.datetime.strptime(
                        row['date'], '%m/%d/%Y').timestamp() >=
                        search_date_one[0].timestamp()) and
                    (datetime.datetime.strptime(
                        row['date'], '%m/%d/%Y').timestamp() <=
                        search_date_two[0].timestamp())):
                    search_results.append(row)
    if len(search_results) == 0:
        print('\nNo results found.\n')
        search_entries()
    else:
        print(json.dumps(search_results))   


def exact_search():
    # Searches by exact keyword
    search_string = None
    search_results = []
    print("Enter text that you would like to search for ")
    while search_string is None or search_string.isspace():
        search_string = input()
        if search_string.strip() == '':
            print("Enter text that you would like searched. ")
            search_string = None
    with open('tasks.csv') as taskfile:
        reader = csv.DictReader(taskfile)
        for row in reader:
            if (row["name"].find(search_string) > -1 or
                    row["notes"].find(search_string) > -1):
                search_results.append(row)
    if len(search_results) == 0:
        print("That keyword was not found")
        search_entries()
    else:
        print(json.dumps(search_results))
        
                    

def regex_search():
    # Allows user to serch by expression
    reg_exp = None
    search_results = []
    print("Enter a valid regular expression.")
    while reg_exp is None:
        reg_exp = input('>>>')
        try:
            reg_exp = re.compile(reg_exp)
        except re.error:
            print("That is not a valid regular expression. Try again.")
            reg_exp = None
    with open('tasks.csv') as taskfile:
        reader = csv.DictReader(taskfile)
        for row in reader:
            if (re.search(reg_exp, row['name']) or
                re.search(reg_exp, row['time']) or
                re.search(reg_exp, row['notes']) or
                    re.search(reg_exp, row['date'])):
                search_results.append(row)
    if len(search_results) == 0:
        print("\nNo results found!")
        search_entries()
    else:
        print(json.dumps(search_results))
        
def time_search():
    time_results = None
    search_results = []
    print("Enter the time that you would like to search for in minutes")
    while time_results is None:
        time_results = input('>>>')
        try:
            time_results = int(time_results)
        except ValueError:
            print("Please enter a valid number")
            time_results = None
        else:
            time_results = str(time_results)
    with open('tasks.csv') as taskfile:
        reader = csv.DictReader(taskfile)
        for row in reader:
            if row['time'] == time_results:
                search_results.append(row)
        if len(search_results) == 0:
            print("No results found")
            search_entries()
        else:
            print(json.dumps(search_results))



if __name__ == "__main__":
    work_log()
