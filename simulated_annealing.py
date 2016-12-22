from process_data import *
from data_manager import *

from random import randint, choice, random
from operator import itemgetter
from math import exp
from optparse import OptionParser


def swap_simulated_annealing(dm, startRandom, Tmax=1000, Tmin=1,
    linear=False, exponential=True, sigmoidal=False):

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
            if linear:
                temp -= 0.1
            elif exponential:
                temp *= 0.9999
            elif sigmoidal:
                temp = Tmax / (1 + exp(0.05 * (dm.i-Tmax/10)))

            print("TEMP", temp)


            acception_rate = exp((dm.iteration_dct[dm.i]["score"] - \
                                   dm.iteration_dct[dm.i - 1]["score"]) / temp)

            if nIteration % 1000 == 0:
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

    dm.exportLectures("SSA%sTmax%sl%se%ss%s" % (round(score), Tmax, linear, exponential, sigmoidal))

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-o", "--loadFromOld", dest="startRandom", default=True,
        help="start from old timetable", action="store_false")

    parser.add_option("-t", "--startTemp", dest="temp", default=1000,
        help="define the default temp")

    parser.add_option("-l", "--linear", dest="linear", default=False,
        help="Activate linear cooling function", action="store_true")

    parser.add_option("-e", "--exponential", dest="exponential", default=True,
        help="Activate exponential cooling function", action="store_true")

    parser.add_option("-s", "--sigmoidal", dest="sigmoidal", default=False,
        help="Activate sigmoidal cooling function", action="store_true")

    (options, args) = parser.parse_args()

    if options.linear or options.sigmoidal:
        options.exponential = False

    if sum([options.linear, options.exponential, options.sigmoidal]) > 1:
        print("Too many cooling schemes selected, try again")

    else:
        if not options.startRandom:
            print("Algorithm will not start with random timetable")
            data_manager.importLectures(input("Timetable name: "))

        swap_simulated_annealing(data_manager, startRandom=options.startRandom,
            Tmax=int(options.temp), linear=options.linear,
            exponential=options.exponential, sigmoidal=options.sigmoidal)
