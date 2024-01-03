import sqlite3
from tabulate import tabulate

def get_db(name):
    """
    This function establishes a connection with the specified database file.
    :param name: The filename of the database.
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db

def create_tables(db):
    """
    This function ensures the existence of necessary tables in the specified database.
    :param db: The database connection object.
    """
    
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habit_data (
            name varchar(255) NOT NULL, 
            category text, 
            frequency text, 
            duration varchar(255) NOT NULL, 
            start_day varchar(255) NOT NULL,
            marked_off INTEGER, 
            last_completed_day varchar(250) NOT NULL, 
            streak_days INTEGER, 
            longest_streak_days INTEGER
        )
    """)
    db.commit()

def create_habits(db, name: str, category: str, frequency: str, start_date: str, duration: str,
                  marked_off: int, last_completed_day: str, streak_days: int, longest_st_days: int):
    """
    This function inserts data related to habits into the specified database.
    :param db: The database connection object.
    :param name: The name of the habit.
    :param category: The category of the habit.
    :param frequency: The frequency of the habit.
    :param start_date: The starting date of the habit.
    :param duration: The duration of the habit.
    :param marked_off: The count of habit performances.
    :param last_completed_day: The date when the habit was last marked as completed.
    :param streak_days: The count of consecutive streak days.
    :param longest_st_days: The count of the longest streak days.
    """
    cur = db.cursor()
    cur.execute(f"""
        INSERT INTO habit_data VALUES (
            '{name}', '{category}', '{frequency}', '{duration}',
            '{start_date}', '{marked_off}', '{last_completed_day}',
            '{streak_days}', '{longest_st_days}'
        )
    """)
    db.commit()

def get_table(db, thing, value):
    """
    This function retrieves and formats habit-related data from the specified database into a table.
    :param db: The database connection object.
    :param thing: The column name in the table.
    :param value: The value of the column.
    :return: Formatted habit data table.
    """
    cursor = db.cursor()

    if thing is None and value is None:
        rows = cursor.execute(f"SELECT * FROM habit_data;")
        db.commit()
    else:
        rows = cursor.execute(f"SELECT * FROM habit_data WHERE {thing} = '{value}';")
        db.commit()

    def table(l_rows):
        first_row = ['Name', 'Category', 'Frequency', 'Duration', 'Start Date', 'Marked off',
                     'Last Completed Day', 'Streak Days', 'Ln. Streak Days']
        rows_listed = [list(row) for row in l_rows]
        rows_listed.insert(0, first_row)
        return tabulate(rows_listed, headers='firstrow', tablefmt='pretty')

    table = table(l_rows=rows)
    return table

   

    
