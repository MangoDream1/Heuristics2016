from process_data import *
from data_manager import *

from random import randint, choice, random
from operator import itemgetter
from math import exp
from optparse import OptionParser


def swap_simulated_annealing(dm, startRandom, Tmax=1000, Tmin = 1):

    print("Starting swap simulated annealing...")

    temp = Tmax
    nIteration = 0

    while True:
        changed_lectures = []

        if dm.i == 0 and startRandom:
            for lecture in dm.lectures:
                changed_lectures.append(
                    dm.randomLocation(lecture, no_overlap=True))

                changed_lectures.append(lecture)

            dm.addChanges(changed_lectures)
            dm.i += 1

        else:
            rLecture = choice(dm.lectures)
            rClassroom = choice(dm.classrooms)
            rDay = randint(0, 4)
            rTimeslot = randint(0, 3)

            new_location = rClassroom.timetable[rDay][rTimeslot]
            old_location = rLecture.classroom.\
                                    timetable[rLecture.day][rLecture.timeslot]

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

            dm.addChanges(changed_lectures)

            dm.plot.addScore(dm.iteration_dct[dm.i]["score"])

            # Simulated Annealing from here
            temp *= 0.9999

            acception_rate = exp((dm.iteration_dct[dm.i]["score"] - \
                                   dm.iteration_dct[dm.i - 1]["score"]) / temp)

            if nIteration % 1000 == 0:
                print(dm.iteration_dct[dm.i]["score"])
                print(temp)
                print(acception_rate)
                dm.createBase()

            r = random()

            if dm.iteration_dct[dm.i]["score"] > \
               dm.iteration_dct[dm.i - 1]["score"]:

                dm.i += 1
                nIteration += 1

            elif acception_rate >= r:
                dm.i += 1
                nIteration += 1

            else:
                # Reset to previous state
                dm.applyChanges(dm.compileChanges(dm.i - 1))
                nIteration += 1

        if temp <= Tmin or dm.iteration_dct[dm.i-1]["score"] >= 1400:
            break


    best_iteration, score = dm.compileBest()

    print("Best iteration: %s, Score: %s" % (best_iteration, round(score)))

    dm.exportLectures("SSA%sTmax%s" % (round(score), Tmax))

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-l", "--loadFromOld", dest="startRandom", default=True,
        help="start from old timetable", action="store_false")

    (options, args) = parser.parse_args()

    if not options.startRandom:
        print("Algorithm will not start with random timetable")
        data_manager.importLectures(input("Timetable name: "))

    swap_hill_climber(data_manager, startRandom=options.startRandom)
