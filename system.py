import datetime as dt
import questionary
from db import *
import sqlite3


def habit_names_from_data(file_db, marked_off):
    """Retrieves the names of habits from the specified database file.
    :param file_db: The name of the database file.
     """
    connection = sqlite3.connect(file_db)
    cursor = connection.cursor()

    if marked_off == 2:
        rows = cursor.execute("SELECT name FROM habit_data")
    else:
        rows = cursor.execute(f"SELECT name FROM habit_data WHERE marked_off = '{marked_off}'")
    listed_rows = [list(row)[0] for row in rows]

    return listed_rows


class AddHabit:
    """
        Class to create and store a new habit in the 'db_file.db' database.
    """

    def add_habit(self, name: str, category: str, frequency: str, duration: str, file_db):

        """
        :param name: The name of the habit.
        :param category: The category of the habit.
        :param frequency: The frequency of the habit.
        :param duration: The duration of the habit.
        :param file_db: The database file name.
        """

        start_date = dt.datetime.now().strftime('%Y/%m/%d')

        db = get_db(file_db)
        create_habits(db=db, name=name, category=category, frequency=frequency, duration=duration,
                      start_date=start_date, marked_off=0, last_completed_day="-",
                      streak_days=0, longest_st_days=0)


class EditHabit:
    """
       Class to edit habit details such as name, category, or frequency.

            Explanation:
                habit_name->the name of the habit that needs to be edited
                choice->the user's choice of what should be edited in habit (name or category or frequency)
                new->value: the new value that the users input.  

    """

    def __init__(self, habit_name: str, choice: str, new_value: str):
        """
        Init Function

        :param habit_name: The name of the habit to be edited.
        :param choice: The selected attribute to edit (name/category/frequency).
        :param new_value: The new value to be set.
        """
        self.habit_name = habit_name
        self.purpose = choice
        self.new_value = new_value

    def edit(self, file_db):
        """ Modifies the name or category or frequency of the specified habit in the database.
        :param file_db: The database file name. """

        db = get_db(file_db)

        db.execute(f"UPDATE habit_data SET {self.purpose} = '{self.new_value}'"
                   f"WHERE name = '{self.habit_name}';")
        db.commit()

    @staticmethod   #harus pakai decorator staticmethod supaya bisa digunakan di menu selain edit!!!
    def uncomplete_habit(name: str, file_db: str):
        connection = sqlite3.connect(file_db)
        cursor = connection.cursor()
        cursor.execute(f"SELECT marked_off FROM habit_data WHERE name = '{name}';")
        completed = list(cursor.fetchone())[0]
        cursor.execute(f"UPDATE habit_data SET marked_off = '{completed - 1}', last_completed_day = '-' WHERE name = '{name}';")
        connection.commit()


class AnalyzeHabit:
    """
    Class to track and analyze habits' completion and streaks.

        Methods:
            check_off(self, name: str, answer: str, file_db):
                This function is responsible for marking the habit after its completion.

            count_streak_days(self, habit_name: str, frequency: str, file_db):
                Counts streak days

            report(self, purpose: str, file_db):
                Gives information about habits
    """

    def check_off(self, name: str, file_db):

        connection = sqlite3.connect(file_db)
        cursor = connection.cursor()
        cursor.execute(f"SELECT marked_off FROM habit_data WHERE name = '{name}';")
        completed = list(cursor.fetchone())[0]
        cursor.execute(f"SELECT frequency FROM habit_data WHERE name = '{name}';")
        frequency = list(cursor.fetchone())[0]

        self.count_streak_days(name, frequency, file_db)

        now = dt.datetime.now().strftime("%Y/%m/%d")
        cursor.execute(f"UPDATE habit_data SET marked_off = '{completed + 1}', last_completed_day = '{now}'"
                       f"WHERE name = '{name}';")

        connection.commit()

    def count_streak_days(self, habit_name: str, frequency: str, file_db):
        connection = sqlite3.connect(file_db)
        cursor = connection.cursor()
        dif = ''

        if frequency == 'daily':
            dif = (dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y/%m/%d")

        elif frequency == 'weekly':
            dif = (dt.datetime.now() - dt.timedelta(weeks=1)).strftime("%Y/%m/%d")

        cursor.execute(f"SELECT last_completed_day FROM habit_data WHERE name = '{habit_name}';")
        last_completed_day = list(cursor.fetchone())[0]
        cursor.execute(f"SELECT streak_days FROM habit_data WHERE name = '{habit_name}';")
        streak_days = list(cursor.fetchone())[0]

        cursor.execute(f"SELECT longest_streak_days FROM habit_data WHERE name = '{habit_name}';")
        longest_st_days = list(cursor.fetchone())[0]

        if dif == last_completed_day:
            cursor.execute(f"UPDATE habit_data SET streak_days = '{streak_days + 1}'"
                           f"WHERE name = '{habit_name}';")
            connection.commit()

            if longest_st_days <= streak_days + 1:
                longest_st_days += 1
                cursor.execute(f"UPDATE habit_data SET longest_streak_days = '{longest_st_days}'"
                               f"WHERE name = '{habit_name}';")
                connection.commit()

        else:
            streak_days = 1
            cursor.execute(f"UPDATE habit_data SET streak_days = '{streak_days}'"
                           f"WHERE name = '{habit_name}';")
            connection.commit()

            if longest_st_days == 0:
                cursor.execute(f"UPDATE habit_data SET longest_streak_days = '{longest_st_days + 1}'"
                               f"WHERE name = '{habit_name}';")
                connection.commit()

    def report(self, purpose: str, file_db):
        table = ""
        db = get_db(file_db)

        if purpose == "all habits":
            table = get_table(db, thing=None, value=None)

        elif purpose == "all daily habits":
            table = get_table(db, thing='frequency', value='daily')

        elif purpose == "all weekly habits":
            table = get_table(db, thing='frequency', value='weekly')

        elif purpose == "one habit":
            name = questionary.select('Which habit do you want to report?',
                                      choices=habit_names_from_data(file_db)).ask()
            table = get_table(db, thing='name', value=f'{name}')

        print(table)


class PredefinedHabits:
    """
    The function of this class is to review all predefined habits
    """

    def report_predefined_habits(self, file_db):
        db = get_db(file_db)
        table = get_table(db, thing=None, value=None)
        print(table)


class DeleteHabit:
    """
    Class to delete a habit from the database.
    """

    def delete_the_habit(self, name: str, file_db):
        connection = sqlite3.connect(file_db)
        cursor = connection.cursor()

        cursor.execute(f"DELETE FROM habit_data "
                       f"WHERE name='{name}'")
        connection.commit()
