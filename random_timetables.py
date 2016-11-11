from process_data import *
from score_system import *
from random import randint, choice

for x in subjects:
    for y in x.lectures:
        y.classRoom = classRooms[0]
        classRooms[0].lectures.append(y)

        y.day = randint(0, 4)
        y.timeslot = randint(0, 3)
        y.classRoom = choice(classRooms)

        y.assignLecturetoClassroom()


    x.exportTimetable()

for x in students:
    x.exportTimetable()

for x in classRooms:
    x.exportTimetable()


print(Score(subjects, students, classRooms).score)
