from process_data import *
from iteration_manager import *
from random import randint, choice, random
from operator import itemgetter
from math import exp

def swap_simulated_annealing(im, startRandom, Tmax=1000,
                             Tmin = 1, ding=100):

    print("Starting swap simulated annealing...")

    temp = Tmax
    nIteration = 0

    while True:
        changed_lectures = []

        if im.i == 0 and startRandom:
            for lecture in im.lectures:
                lecture.day = randint(0, 4)
                lecture.timeslot = randint(0, 3)
                lecture.classroom = choice(classrooms)

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

            # Simulated Annealing from here
            temp *= 0.9999

            acception_rate = exp(-(im.iteration_dct[im.i - 1]["score"] - im.iteration_dct[im.i]["score"]) / temp)

            if nIteration % 100000 == 0:
                print(im.iteration_dct[im.i]["score"])
                print(nIteration / ding)
                print(temp)
                print(acception_rate)
                im.createBase()


            r = random()

            if im.iteration_dct[im.i]["score"] > im.iteration_dct[im.i - 1]["score"]:
                im.i += 1
                nIteration += 1

            elif acception_rate >= r:
                im.i += 1
                nIteration += 1

            else:
                # Reset to previous state
                im.applyChanges(im.compileChanges(im.i - 1))
                nIteration += 1

            if nIteration % 1 == 0:
                print(str(acception_rate >= r) + " " + str(int(temp)) + " " + str(im.iteration_dct[im.i-1]["score"]))


        if temp <= Tmin or im.iteration_dct[im.i-1]["score"] >= 1440:
            break


    best_iteration = max([(i, im.iteration_dct[i]["score"]) for i in im.iteration_dct.keys()], key=itemgetter(1))
    print("Best iteration: %s, Score: %s" % (best_iteration[0], best_iteration[1]))

    im.applyChanges(im.compileChanges(best_iteration[0]))

    im.exportLectures("SSA%sTmax%s" % (best_iteration[1], Tmax))


startRandom = True
if input("Do you want to start from a previously made timetable [Y/N]: ").lower() == 'y':
    iteration_manager.importLectures(input("Timetable name: "))
    iteration_manager.exportTimetable()
    startRandom = False

swap_simulated_annealing(iteration_manager, startRandom=startRandom)
