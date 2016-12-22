from process_data import *
from data_manager import *

from random import randint, choice, random
from operator import itemgetter
from optparse import OptionParser


def swap_hill_climber(dm, noProgressLimit, startRandom):
    """

    """

    print("Starting swap hill climber...")

    noProgressCounter = 0

    while noProgressCounter != noProgressLimit:
        changed_lectures = []

        if dm.i == 0 and startRandom:
            for lecture in dm.lectures:
                changed_lectures.append(
                    dm.randomLocation(lecture, no_overlap=True))

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

            if dm.iteration_dct[dm.i]["score"] > \
               dm.iteration_dct[dm.i - 1]["score"]:

                dm.plot.addScore(dm.iteration_dct[dm.i]["score"])

                if dm.i % 10 == 0:
                    dm.createBase()


                dm.i += 1
                noProgressCounter = 0

            else:
                # Reset to previous state
                dm.applyChanges(dm.compileChanges(dm.i - 1))
                noProgressCounter += 1


    dm.plot.addScore(dm.iteration_dct[dm.i]["score"])
    best_iteration, score = dm.compileBest()

    print("Best iteration: %s, Score: %s" % (best_iteration, round(score)))

    dm.exportLectures("SHC%snPl%s" % (round(score), noProgressLimit))

if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-l", "--loadFromOld", dest="startRandom", default=True,
        help="start from old timetable", action="store_false")

    parser.add_option("-n", "--noProgressLimit", dest="noProgressLimit",
        default=1000, help="The number of times the algorithm is allowed not to progress")

    (options, args) = parser.parse_args()

    if not options.startRandom:
        print("Algorithm will not start with random timetable")
        data_manager.importLectures(input("Timetable name: "))

    swap_hill_climber(data_manager,
        int(options.noProgressLimit), startRandom=options.startRandom)
