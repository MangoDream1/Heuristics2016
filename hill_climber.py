from process_data import *
from score_system import *
from iteration_manager import *
from random import randint, choice, random
from operator import itemgetter

def simple_hill_climber(classroomWeigth, timeslotWeigth, dayWeigth, lecture_dct):
    print("Starting simple hill climber...")

    weight = 1 / (classroomWeigth + timeslotWeigth + dayWeigth)

    classroomWeigth = classroomWeigth * weight
    timeslotWeigth = timeslotWeigth * weight
    dayWeigth = dayWeigth * weight

    im = IterationManager(lecture_dct)

    noProgressCounter = 0

    while noProgressCounter != 1000:
        changed_lectures = []

        if im.i == 0:
            for lecture in lectures:
                lecture.day = randint(0, 4)
                lecture.timeslot = randint(0, 3)
                lecture.classroom = choice(classrooms)

                changed_lectures.append(lecture)

            im.addChanges(changed_lectures)
            im.i += 1

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

            im.addChanges(changed_lectures)

            if im.iteration_dct[im.i]["score"] > im.iteration_dct[im.i - 1]["score"]:
                if im.i % 10 == 0:
                    print(im.iteration_dct[im.i]["score"])

                    im.createBase()

                im.i += 1
                noProgressCounter = 0

            else:
                im.applyChanges(im.compileChanges(im.i - 1))
                noProgressCounter += 1

    best_iteration = max([(i, im.iteration_dct[i]["score"]) for i in im.iteration_dct.keys()], key=itemgetter(1))
    print("Best iteration: %s, Score: %s" % (best_iteration[0], best_iteration[1]))

    im.lecture_dct = im.applyChanges(im.compileChanges(best_iteration[0]))

    for x in subjects + students + classrooms:
        x.exportTimetable()

simple_hill_climber(1, 5, 3, lecture_dct)
