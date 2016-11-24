from process_data import *
from iteration_manager import *
from random import randint, choice, random
from operator import itemgetter

def simple_hill_climber(im, noProgressCounterLimit, classroomWeigth, timeslotWeigth, dayWeigth, startRandom=True):
    print("Starting simple hill climber...")

    weight = 1 / (classroomWeigth + timeslotWeigth + dayWeigth)

    classroomWeigth = classroomWeigth * weight
    timeslotWeigth = timeslotWeigth * weight
    dayWeigth = dayWeigth * weight

    noProgressCounter = 0

    while noProgressCounter != noProgressCounterLimit:
        changed_lectures = []

        if im.i == 0 and startRandom:
            for lecture in im.lectures:
                lecture.day = randint(0, 4)
                lecture.timeslot = randint(0, 3)
                lecture.classroom = choice(im.classrooms)

                changed_lectures.append(lecture)

            im.addChanges(changed_lectures)
            im.i += 1

        else:
            lecture = choice(im.lectures)
            r = random()

            if r < classroomWeigth:
                # Classroom
                lecture.classroom = choice(im.classrooms)
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

    im.applyChanges(im.compileChanges(best_iteration[0]))

    im.exportLectures("HC%snPl%sc%.1ft%.1fd%.1f" % (best_iteration[1], noProgressCounterLimit, classroomWeigth, timeslotWeigth, dayWeigth))

startRandom = True
if input("Do you want to start from a previously made timetable [Y/N]: ").lower() == 'y':
    iteration_manager.importLectures(input("Timetable name: "))
    startRandom = False

simple_hill_climber(iteration_manager, 100, 1, 1, 1, startRandom=startRandom)
