from process_data import *

from random import randint, choice
from optparse import OptionParser


def update_progress(workdone, text='Progress:'):
    """ Print the progress bar """

    print("\r{0} [{1:50s}] {2:.1f}%".format(text, '#' * int(workdone * 50),
    workdone*100), end="", flush=True)

    if workdone == 1:
        print('\n')

def random_timetables(dm, nPlannedIterations, no_overlap):
    """ Create nPlannedIterations of random timetables and then output the
        best one. If no_overlap is True it will not create any overlap
    """

    print("Starting random timetables with %s iterations..."
            % nPlannedIterations)

    while dm.i != nPlannedIterations:
        # For every lecture find a random location
        for lecture in dm.lectures:
            dm.randomLocation(lecture, no_overlap=no_overlap)

        # Every thing changes thus add all
        dm.addChanges(dm.lectures)

        # Makes all base since its all random anyways
        dm.createBase()

        dm.plot.addScore(dm.iteration_dct[dm.i]["score"])

        dm.i += 1
        update_progress(dm.i/nPlannedIterations)

        dm.resetTimetables()

    best_iteration, score = dm.compileBest()

    average = sum([dm.iteration_dct[i]["score"]
                    for i in dm.iteration_dct.keys()]) / nPlannedIterations

    print("Best iteration: %s, Score: %s, Average Score: %s" %
                (best_iteration, round(score), round(average)))

    dm.exportLectures("RT%si%sa%s" % (round(score),
        nPlannedIterations, round(average)), plot=False)

    dm.plot.plotHistogram("RT%si%sa%s" % (round(score),
        nPlannedIterations, round(average)))

    return dm.lecture_dct

if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-i", "--iterations", dest="nPlannedIterations",
        default=1000, help="The number of timetables created")

    parser.add_option("-o", "--keep_overlap", dest="keep_overlap", default=True,
        help="Removal of overlap for every random timetable.",
        action="store_false")

    (options, args) = parser.parse_args()

    random_timetables(data_manager,
        int(options.nPlannedIterations), options.keep_overlap)
