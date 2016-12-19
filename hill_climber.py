from process_data import *
from data_manager import *

from random import randint, choice, random
from optparse import OptionParser

def simple_hill_climber(dm, noProgressLimit, classroomWeigth,
                        timeslotWeigth, dayWeigth, startRandom=True):
    print("Starting simple hill climber...")

    weight = 1 / (classroomWeigth + timeslotWeigth + dayWeigth)

    classroomWeigth = classroomWeigth * weight
    timeslotWeigth = timeslotWeigth * weight
    dayWeigth = dayWeigth * weight

    noProgressCounter = 0

    while noProgressCounter != noProgressLimit:
        changed_lectures = []

        if dm.i == 0 and startRandom:
            for lecture in dm.lectures:
                changed_lectures.append(
                    dm.randomLocation(lecture, no_overlap=True))

                changed_lectures.append(lecture)

            dm.addChanges(changed_lectures)
            dm.i += 1

        else:
            lecture = choice(dm.lectures)
            r = random()

            if r < classroomWeigth:
                # Classroom
                lecture.classroom = choice(dm.classrooms)
            elif r > classroomWeigth and r < (timeslotWeigth + classroomWeigth):
                # Timeslot
                lecture.timeslot = randint(0, 3)
            elif r > (timeslotWeigth + classroomWeigth) and \
                 r < (timeslotWeigth + classroomWeigth + dayWeigth):

                # Day
                lecture.day = randint(0, 4)

            dm.addChanges(changed_lectures)

            if dm.iteration_dct[dm.i]["score"] > \
               dm.iteration_dct[dm.i - 1]["score"]:

                dm.plot.addScore(dm.iteration_dct[dm.i]["score"])

                if dm.i % 10 == 0:
                    print(dm.iteration_dct[dm.i]["score"])


                    dm.createBase()

                dm.i += 1
                noProgressCounter = 0

            else:
                dm.applyChanges(dm.compileChanges(dm.i - 1))
                noProgressCounter += 1

    best_iteration, score = dm.compileBest()

    print("Best iteration: %s, Score: %s" % (best_iteration, round(score)))

    dm.exportLectures("HC%snPl%sc%.1ft%.1fd%.1f" %
                        (round(score), noProgressLimit,
                         classroomWeigth, timeslotWeigth, dayWeigth))

if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-n", "--noProgressLimit", dest="noProgressLimit",
    default=1000, help="The number of times the algorithm cannot progress")

    parser.add_option("-r", "--startRandom", dest="startRandom", default=True,
        help="start at a random location", action="store_false")

    parser.add_option("-wc", "--classroomWeigth", dest="classroomWeigth",
        default=1,
        help="The weight that is given to classrooms in random changes")

    parser.add_option("-wt", "--timeslotWeigth", dest="timeslotWeigth",
        default=1,
        help="The weight that is given to timeslots in random changes")

    parser.add_option("-wd", "--dayWeigth", dest="dayWeigth", default=1,
        help="The weight that is given to days in random changes")

    (options, args) = parser.parse_args()

    if not options.startRandom:
        print("Algorithm will not start with random timetable")
        data_manager.importLectures(input("Timetable name: "))

    simple_hill_climber(data_manager,
        int(options.noProgressLimit),
        int(options.classroomWeigth),
        int(options.timeslotWeigth),
        int(options.dayWeigth),
        startRandom=options.startRandom)
