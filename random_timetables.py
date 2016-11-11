from process_data import *
from score_system import *
from random import randint, choice

for x in subjects:
    for y in x.lectures:
        y.day = randint(0, 4)
        y.timeslot = randint(0, 3)
        y.classroom = choice(classrooms)

        # Minimum score
        # y.day = 0
        # y.timeslot = 0
        # y.classroom = classrooms[2]

        y.assignLecturetoClassroom()


    x.exportTimetable()

for x in students:
    x.exportTimetable()

for x in classrooms:
    x.exportTimetable()


print(Score(subjects, students, classrooms).score)

# lecture_dct = {index: lecture for index, lecture in enumerate([lecture for subject in subjects for lecture in subject.lectures])}
