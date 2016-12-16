from process_data import *
from iteration_manager import *

from random import randint, choice, random
from optparse import OptionParser

def simple_hill_climber(im, noProgressLimit, classroomWeigth,
                        timeslotWeigth, dayWeigth, startRandom=True):
    print("Starting simple hill climber...")

    weight = 1 / (classroomWeigth + timeslotWeigth + dayWeigth)

    classroomWeigth = classroomWeigth * weight
    timeslotWeigth = timeslotWeigth * weight
    dayWeigth = dayWeigth * weight

    noProgressCounter = 0

    while noProgressCounter != noProgressLimit:
        changed_lectures = []

        if im.i == 0 and startRandom:
            for lecture in im.lectures:
                changed_lectures.append(
                    im.randomLocation(lecture, no_overlap=True))

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
            elif r > (timeslotWeigth + classroomWeigth) and \
                 r < (timeslotWeigth + classroomWeigth + dayWeigth):

                # Day
                lecture.day = randint(0, 4)

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
                im.applyChanges(im.compileChanges(im.i - 1))
                noProgressCounter += 1

    best_iteration, score = im.compileBest()

    print("Best iteration: %s, Score: %s" % (best_iteration, round(score)))

    im.exportLectures("HC%snPl%sc%.1ft%.1fd%.1f" %
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
        iteration_manager.importLectures(input("Timetable name: "))

    simple_hill_climber(iteration_manager,
        int(options.noProgressLimit),
        int(options.classroomWeigth),
        int(options.timeslotWeigth),
        int(options.dayWeigth),
        startRandom=options.startRandom)
