from process_data import *

from random import randint, choice
from optparse import OptionParser


def update_progress(workdone, text='Progress:'):
    print("\r{0} [{1:50s}] {2:.1f}%".format(text, '#' * int(workdone * 50),
    workdone*100), end="", flush=True)

    if workdone == 1:
        print('\n')

def random_timetables(im, nPlannedIterations, no_overlap):
    print("Starting random timetables with %s iterations..."
            % nPlannedIterations)

    while im.i != nPlannedIterations:
        changed_lectures = []

        for lecture in im.lectures:
            changed_lectures.append(
                im.randomLocation(lecture, no_overlap=no_overlap))

        im.addChanges(changed_lectures)

        # Makes all base since its all random anyways
        im.createBase()

        im.plot.addScore(im.iteration_dct[im.i]["score"])

        im.i += 1
        update_progress(im.i/nPlannedIterations)

        im.resetTimetables()

    best_iteration, score = im.compileBest()

    average = sum([im.iteration_dct[i]["score"]
                    for i in im.iteration_dct.keys()]) / nPlannedIterations

    print("Best iteration: %s, Score: %s, Average Score: %s" %
                (best_iteration, round(score), round(average)))

    im.exportLectures("RT%si%sa%s" % (round(score),
        nPlannedIterations, round(average)))

    return im.lecture_dct

parser = OptionParser()

parser.add_option("-i", "--iterations", dest="nPlannedIterations",
    default=1000, help="The number of timetables created")

parser.add_option("-o", "--no_overlap", dest="no_overlap", default=True,
    help="Removal of overlap for every random timetable. True of False")

(options, args) = parser.parse_args()

random_timetables(iteration_manager,
    int(options.nPlannedIterations), bool(options.no_overlap))
