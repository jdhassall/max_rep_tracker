import sqlite3
import matplotlib.pyplot as plt
import sys
import traceback

def database_connection():
    try:
        connection = sqlite3.Connection('exercise_six_rep_max.db')
        return connection
    except sqlite3.Error as error:
        print('ERROR OCCURRED - See log file for more information.')
        error_logging(error)

def database_cursor(connection):
    try:
        cursor = connection.cursor()
        return cursor
    except sqlite3.Error as error:
        print('ERROR OCCURRED - See log file for more information.')
        error_logging(error)

def enter_new_exercise():
    exercise = ''
    while exercise == '':
        exercise = input('please enter the exercise you wish to add to the database: ')
        if exercise == '':
            exercise = input('please enter a valid exercise: ')
        return exercise

def new_database_table(connection, cursor, exercise):
    try:
        # Check if table already exists
        cursor.execute(f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{exercise}' ''')
        if cursor.fetchone()[0] == 1:
            print('Table already exists.')
        else:
            # Table doesnt exist so create new table
            create_table_string = f'''CREATE TABLE IF NOT EXISTS {exercise} (weight real, date text)'''
            cursor.execute(create_table_string)
            connection.commit()
    except sqlite3.Error as error:
        print('ERROR OCCURRED - See log file for more information.')
        error_logging(error)

def insert_new_data(connection, cursor, exercise):
    show_exercises(cursor)
    if exercise == '':
        exercise = input('What exercise would you like to enter data for? ')
    date = input('What is the date the PB was performed on? ')
    weight = input('What was the weight of the PB of the session for this exercise? ')
    weight = float(weight)
    sql_query = f'''INSERT INTO {exercise} VALUES (?,?)'''
    sql_data = (weight, date)
    try:
        cursor.execute(sql_query, sql_data)
        connection.commit()
    except sqlite3.Error as error:
        print('ERROR OCCURRED - See log file for more information.')
        error_logging(error)

def retrieve_data(cursor):
    date_data = []
    weight_data = []
    try:
        show_exercises(cursor)
        exercise = input('What exercise would you like to show data for? ')
        cursor.execute(f'''SELECT * FROM {exercise}''')
        rows = cursor.fetchall()
        for row in rows:
            weight_data.append(row[0])
            date_data.append(row[1])
        return weight_data, date_data, exercise
    except sqlite3.Error as error:
        print('ERROR OCCURRED - See log file for more information.')
        error_logging(error)

def show_exercises(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(f'{cursor.fetchall()}') # THIS IS SOMETIMES BEING CALLED AND THEN MOVING STRAIGHT ONTO THE WEIGHT WHEN ENTERING NEW EXERCISE: NEED TO FIX

def plot_data(weight_data, date_data, exercise):
    try:
        plt.plot(date_data, weight_data)
        plt.xlabel('Weight (kg)')
        plt.ylabel('Date')
        plt.title(f'Max weight for six reps for {exercise}')
        plt.show()
    except:
        print('ERROR OCCURRED - See log file for more information.')
        error_logging(sys.exc_info()[0])

def handle_database_operations(connection, cursor):
    more_operations = ''
    exercise = ''
    while more_operations != 'no':
        option = input("Do you want to:\n(A) Enter a new exercise into the database?\n(B) Add data new data to an "
                       "existing exercise?\n(C) No action.\n[A/B/C]: ")
        if option == 'A':
            # See if user wants to create a new database for a new exercise
            exercise = enter_new_exercise()
            new_database_table(connection, cursor, exercise)
            insert_new_data(connection, cursor, exercise)
        if option == 'B':
            insert_new_data(connection, cursor, exercise)
        more_operations = input('Do you wish to perform another database operation? [yes/no]: ')
            # See if user wants to delete a table
            # See if user wants to delete an entry

def handle_data_display_operations(connection, cursor):
    # See if the user wants to display data graphically for a single exercise
    data = retrieve_data(cursor)
    print(data[0])
    plot_data(data[0], data[1], data[2])
    # See if the user wants to display data tabularly for a single exercise
    # See if the user wants to display data graphically for multiple exercises
    # See if the user wants to display data tabularly for multiple exercises

def error_logging(error):
    exc_type, exc_value, exc_tb = sys.exc_info()
    string = 'SQLite error: %s' % (' '.join(error.args)), "\nException class is: ", error.__class__, '\nSQLite traceback: ' + traceback.format_exception(exc_type, exc_value, exc_tb)
    f = open("log.txt", "a")
    f.write(string)
    f.close()

def do_you_want_to_quit(continue_programme, connection, cursor):
    try:
        answer = input('Do you wish to continue or exit the programme? [yes/no]: ')
        if answer == 'yes':
            continue_programme = False
            cursor.close()
            connection.close()
        return continue_programme
    except answer != 'yes' or 'no':
        print('Invalid response - please only choose enter yes or no')
        do_you_want_to_quit(continue_programme)

def main():
    continue_programme = True
    while continue_programme:
        connection = database_connection()
        cursor = database_cursor(connection)
        handle_database_operations(connection, cursor)
        handle_data_display_operations(connection, cursor)
        continue_programme = do_you_want_to_quit(continue_programme, connection, cursor)

if __name__ == '__main__':
    main()