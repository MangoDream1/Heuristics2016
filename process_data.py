import csv

from classes import *
from data_manager import *

# By importing timing start timer
import timing

print("Getting data...")

def importFromCSV(file_name):
    with open(file_name, 'r', encoding="latin8") as csvfile:
        r = csv.reader(csvfile, delimiter=',')

        # Skip title
        next(r, None)

        strip = lambda l: [x.strip() for x in l]

        return [strip(row) for row in r]

classrooms = importFromCSV("raw_data/classrooms.csv")
subjects = importFromCSV("raw_data/subjects.csv")
students = importFromCSV("raw_data/students.csv")

print("Transforming data...")

def create_dm(classrooms, subjects, students):

    classrooms = [Classroom(x[0], x[1]) for x in classrooms]

    subjects = [Subject(x[0], x[1], x[2], x[3], x[4], x[5]) for x in subjects]

    students = [Student(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])
                for x in students]

    return DataManager(classrooms, subjects, students)

data_manager = create_dm(classrooms, subjects, students)
