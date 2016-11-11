from process_data import *
from score_system import *
from random import randint, choice

for x in subjects:
    for y in x.lectures:
        y.classroom = classrooms[0]
        classrooms[0].lectures.append(y)

        y.day = randint(0, 4)
        y.timeslot = randint(0, 3)
        y.classroom = choice(classrooms)

        y.assignLecturetoClassroom()


    x.exportTimetable()

for x in students:
    x.exportTimetable()

for x in classrooms:
    x.exportTimetable()


print(Score(subjects, students, classrooms).score)
