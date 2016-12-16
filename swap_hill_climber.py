from process_data import *
from iteration_manager import *

from random import randint, choice, random
from operator import itemgetter
from optparse import OptionParser


def swap_hill_climber(im, noProgressLimit, startRandom):
    print("Starting swap hill climber...")

    noProgressCounter = 0

    while noProgressCounter != noProgressLimit:
        changed_lectures = []

        if im.i == 0 and startRandom:
            for lecture in im.lectures:
                changed_lectures.append(
                    im.randomLocation(lecture, no_overlap=True))

            im.addChanges(changed_lectures)
            im.i += 1

        else:
            rLecture = choice(im.lectures)
            rClassroom = choice(im.classrooms)
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

            im.addChanges(changed_lectures)

            if im.iteration_dct[im.i]["score"] > \
               im.iteration_dct[im.i - 1]["score"]:

                im.plot.addScore(im.iteration_dct[im.i]["score"])

                if im.i % 10 == 0:
                    print(im.iteration_dct[im.i]["score"])

                    im.createBase()


                im.i += 1
                noProgressCounter = 0

            else:
                # Reset to previous state
                im.applyChanges(im.compileChanges(im.i - 1))
                noProgressCounter += 1



    best_iteration, score = im.compileBest()

    print("Best iteration: %s, Score: %s" % (best_iteration, round(score)))

    im.exportLectures("SHC%snPl%s" % (round(score), noProgressLimit))

parser = OptionParser()

parser.add_option("-r", "--startRandom", dest="startRandom", default=True,
    help="start at a random location, default True")

parser.add_option("-n", "--noProgressLimit", dest="noProgressLimit",
    default=1000, help="The number of times the algorithm cannot progress")

(options, args) = parser.parse_args()

if not bool(options.startRandom):
    print("Algorithm will not start with random timetable")
    iteration_manager.importLectures(input("Timetable name: "))

swap_hill_climber(iteration_manager,
    int(options.noProgressLimit), startRandom=bool(options.startRandom))
