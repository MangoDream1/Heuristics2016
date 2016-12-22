from process_data import *
from data_manager import *

from random import randint, choice, random
from optparse import OptionParser

def simple_hill_climber(dm, noProgressLimit, classroomWeigth,
                        timeslotWeigth, dayWeigth, startRandom=True):
    """ Choice a random lecture and based on the weights choice an attribute.
        Randomly change this attribute to another value and then check score.
        If score is better continue else throw away and try again. Try as many
        times as noProgressLimit allows.
    """
    
    print("Starting simple hill climber...")

    # Find the weight of all between 0 and 1
    weight = 1 / (classroomWeigth + timeslotWeigth + dayWeigth)

    classroomWeigth = classroomWeigth * weight
    timeslotWeigth = timeslotWeigth * weight
    dayWeigth = dayWeigth * weight

    noProgressCounter = 0

    while noProgressCounter != noProgressLimit:
        changed_lectures = []

        # For the first create random timetables with no overlap
        if dm.i == 0 and startRandom:
            for lecture in dm.lectures:
                changed_lectures.append(
                    dm.randomLocation(lecture, no_overlap=True))

                changed_lectures.append(lecture)

            dm.addChanges(changed_lectures)
            dm.i += 1

        else:
            # Choice a random lecture
            lecture = choice(dm.lectures)

            # Create random value between 0 and 1 and select between classrooms,
            # timeslot and days and make random change in the selected lecture
            r = random()
            if r < classroomWeigth:
                # Classroom
                lecture.classroom = choice(dm.classrooms)
            elif r > classroomWeigth and r < (timeslotWeigth + classroomWeigth):
                # Timeslot
                lecture.timeslot = randint(0, NUMBER_OF_SLOTS - 1)
            elif r > (timeslotWeigth + classroomWeigth) and \
                 r < (timeslotWeigth + classroomWeigth + dayWeigth):

                # Day
                lecture.day = randint(0, NUMBER_OF_DAYS - 1)

            # Add changes to dct and calculate score
            dm.addChanges(changed_lectures)

            # If higher than last one, save score and reset noProgressCounter
            if dm.iteration_dct[dm.i]["score"] > \
               dm.iteration_dct[dm.i - 1]["score"]:

                dm.plot.addScore(dm.iteration_dct[dm.i]["score"])

                # Create a base for every 10
                if dm.i % 10 == 0:
                    dm.createBase()

                dm.i += 1
                noProgressCounter = 0

            # If lower than last score go back to previous state and add one
            # to noProgressCounter. Also since dm.i isn't increased these
            # changes will be overwritten next iteration
            else:
                dm.applyChanges(dm.compileChanges(dm.i - 1))
                noProgressCounter += 1

    # Add last obtained score so that the plot shows how long was searched for
    # a beter score
    dm.plot.addScore(dm.iteration_dct[dm.i]["score"])

    # Compile the best out of the dict
    best_iteration, score = dm.compileBest()

    print("Best iteration: %s, Score: %s" % (best_iteration, round(score)))

    # Export the lecture package
    dm.exportLectures("HC%snPl%sc%.1ft%.1fd%.1f" %
                        (round(score), noProgressLimit,
                         classroomWeigth, timeslotWeigth, dayWeigth))

if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-n", "--noProgressLimit", dest="noProgressLimit",
    default=1000, help="The number of times the algorithm is allowed not to progress")

    parser.add_option("-l", "--loadFromOld", dest="startRandom", default=True,
        help="start from old timetable", action="store_false")

    parser.add_option("-c", "--classroomWeigth", dest="classroomWeigth",
        default=1,
        help="The weight that is given to classrooms in random changes")

    parser.add_option("-t", "--timeslotWeigth", dest="timeslotWeigth",
        default=1,
        help="The weight that is given to timeslots in random changes")

    parser.add_option("-d", "--dayWeigth", dest="dayWeigth", default=1,
        help="The weight that is given to days in random changes")

    (options, args) = parser.parse_args()

    if not options.startRandom:
        print("Algorithm will not start with random timetable")
        data_manager.importLectures(input("Timetable name: "))

    # Start the algorithm with correct values
    simple_hill_climber(data_manager,
        int(options.noProgressLimit),
        int(options.classroomWeigth),
        int(options.timeslotWeigth),
        int(options.dayWeigth),
        startRandom=options.startRandom)
