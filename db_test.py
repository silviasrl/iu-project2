from system import *


class TestHabit:

    def test_add_new_habit(self):
        """Tests the integration of a new habit utilizing the “AddHabit” class."""
        habit = AddHabit()
        habit.add_habit(name='swimming', category='hobby', frequency='daily', duration='1 month',
                        file_db="datafiles/predefined_habits.db")

    def test_edit_habit(self):
        """Tests the functionality of editing habits within the “EditHabit” class."""
        habit = EditHabit(habit_name="reading", choice="duration", new_value="3 months")
        habit.edit(file_db="datafiles/predefined_habits.db")

    def test_analyse_habit(self):
        """Tests the analysis features available in the “AnalyzeHabit” class."""
        habit = AnalyzeHabit()
        habit.check_off(name="reading", file_db="datafiles/predefined_habits.db")
        habit.report(purpose='all habits', file_db="datafiles/predefined_habits.db")

    def test_delete(self):
        """Tests the deletion capability within the “DeleteHabit” class."""
        habit = DeleteHabit()
        habit.delete_the_habit(name="reading", file_db="datafiles/predefined_habits.db")
