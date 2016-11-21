from process_data import *
from iteration_manager import *
from random import randint, choice, random
from operator import itemgetter

def swap_hill_climber(im, noProgressCounterLimit, startRandom):
    print("Starting swap hill climber...")

    noProgressCounter = 0

    while noProgressCounter != noProgressCounterLimit:
        changed_lectures = []

        if im.i == 0 and startRandom:
            for lecture in im.lectures:
                lecture.day = 0
                lecture.timeslot = 0
                lecture.classroom = im.classrooms[0]

                changed_lectures.append(lecture)

            im.addChanges(changed_lectures)
            im.i += 1

        else:
            rLecture = choice(im.lectures)
            rClassroom = choice(im.classrooms)
            rDay = randint(0, 4)
            rTimeslot = randint(0, 3)

            new_location = rClassroom.timetable[rDay][rTimeslot]
            old_location = rLecture.classroom.timetable[rLecture.day][rLecture.timeslot]

            if new_location == []:
                new_location.append(rLecture)
            elif len(new_location) == 1 and len(old_location) == 1:
                swapLecture = new_location.pop()

                swapLecture.classroom = rLecture.classroom
                swapLecture.day = rLecture.day
                swapLecture.timeslot = rLecture.timeslot

                changed_lectures.append(swapLecture)
            else:
                continue

            rLecture.classroom = rClassroom
            rLecture.day= rDay
            rLecture.timeslot = rTimeslot

            changed_lectures.append(rLecture)

            im.addChanges(changed_lectures)

            if im.iteration_dct[im.i]["score"] > im.iteration_dct[im.i - 1]["score"]:
                if im.i % 10 == 0:
                    print(im.iteration_dct[im.i]["score"])

                    im.createBase()

                im.i += 1
                noProgressCounter = 0

            else:
                # Reset to previous state
                im.applyChanges(im.compileChanges(im.i - 1))
                noProgressCounter += 1

    best_iteration = max([(i, im.iteration_dct[i]["score"]) for i in im.iteration_dct.keys()], key=itemgetter(1))
    print("Best iteration: %s, Score: %s" % (best_iteration[0], best_iteration[1]))

    im.applyChanges(im.compileChanges(best_iteration[0]))

    im.exportLectures("SHC%snPl%s" % (best_iteration[1], noProgressCounterLimit))


startRandom = True
if input("Do you want to start from a previously made timetable [Y/N]: ").lower() == 'y':
    iteration_manager.importLectures(input("Timetable name: "))
    iteration_manager.exportTimetable()
    startRandom = False

swap_hill_climber(iteration_manager, 1000, startRandom=startRandom)
