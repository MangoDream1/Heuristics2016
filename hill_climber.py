from process_data import *
from score_system import *
from iteration_management import *
from random import randint, choice, random
from operator import itemgetter

iteration = 0
iteration_dct = {}

noProgressCounter = 0

classroomWeigth = 0.333
timeslotWeigth = 0.333
dayWeigth = 0.333


while noProgressCounter != 1000:
    changed_lectures = []

    if iteration == 0:
        for lecture in lectures:
            lecture.day = randint(0, 4)
            lecture.timeslot = randint(0, 3)
            lecture.classroom = choice(classrooms)

            changed_lectures.append(lecture)

        iteration_dct = addChanges(changed_lectures, iteration, iteration_dct, lecture_dct)
        iteration += 1

    else:
        lecture = choice(lectures)
        r = random()

        if r < classroomWeigth:
            # Classroom
            lecture.classroom = choice(classrooms)
        elif r > classroomWeigth and r < (timeslotWeigth + classroomWeigth):
            # Timeslot
            lecture.timeslot = randint(0, 3)
        elif r > (timeslotWeigth + classroomWeigth) and r < (timeslotWeigth + classroomWeigth + dayWeigth):
            # Day
            lecture.day = randint(0, 4)

        iteration_dct = addChanges(changed_lectures, iteration, iteration_dct, lecture_dct)

        #print((iteration, noProgressCounter, iteration_dct[iteration]["score"],  iteration_dct[iteration - 1]["score"]))

        if iteration % 10 == 0:
            print(iteration_dct[iteration]["score"])

            iteration_dct = createBase(iteration, iteration_dct)

        if iteration_dct[iteration]["score"] > iteration_dct[iteration - 1]["score"]:
            iteration += 1
            noProgressCounter = 0
        else:
            lecture_dct = applyChanges(compileChanges(iteration - 1, iteration_dct), lecture_dct)
            noProgressCounter += 1



lecture_dct = applyChanges(compileChanges(iteration, iteration_dct), lecture_dct)

best_iteration = max([(i, iteration_dct[i]["score"]) for i in iteration_dct.keys()], key=itemgetter(1))
print("Best iteration: %s, Score: %s" % (best_iteration[0], best_iteration[1]))

for x in subjects + students + classrooms:
    x.clearLectures()

for x in lectures:
    x.assignLecturetoAll()

for x in subjects + students + classrooms:
    x.exportTimetable()
