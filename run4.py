from swap_hill_climber import swap_hill_climber
from student_optimization import lecture_students_swap
from process_data import *

from optparse import OptionParser
from multiprocessing import Process
import re


def run4_swap_hill_climber(nIterations, noProgressLimit):
    nIterations = round(nIterations / 4)

    while nIterations != 0:
        # Create the 4 processes of swap_hill_climber
        plist = [Process(target=swap_hill_climber,
                         args=(create_im(classrooms, subjects, students),
                                noProgressLimit, True))
                    for x in range(4)]

        for p in plist:
            p.start()

        for p in plist:
            p.join()

        nIterations -= 1

def run4_improve(nImproveTimetables, noProgressLimit,
                    student_optimization=False):

    ints = {x: list(map(int, re.findall(r"\d+", x)))
                for x in os.listdir("Timetable/Lectures")}

    # Dct with score as key and timetable as value if not same noProgressLimit
    # as function to prevent same timetables from being improved
    timetables = {ints[x][0]: x for x in os.listdir("Timetable/Lectures")
                    if x[1] != noProgressLimit}


    # Delete already student optimized timetables
    if student_optimization:
        deletion_lst = []
        for key, value in timetables.items():
            if "STUDENT_OPTIMIZED" in value:
                deletion_lst.append(key)

        for key in deletion_lst:
            del timetables[key]


    # Get the best timetables
    best_scores = sorted(timetables.keys(), reverse=True)[:nImproveTimetables]

    nImproveTimetables = round(len(best_scores) / 4)

    while nImproveTimetables != 0:
        plist = []

        for x in range(4):
            if best_scores:
                im = create_im(classrooms, subjects, students)

                # Import one of the best lectures
                im.importLectures(timetables[best_scores.pop()])

                if not student_optimization:
                    plist.append(Process(target=swap_hill_climber,
                        args=(im, noProgressLimit, False)))

                else:
                    plist.append(Process(target=lecture_students_swap,
                        args=(im, noProgressLimit)))

        for p in plist:
            p.start()

        for p in plist:
            p.join()

        nImproveTimetables -= 1

if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option("-i", "--nIterations", dest="nIterations",
        default=100,
        help="The number of timetables that need to be created or improved")

    parser.add_option("-n", "--noProgressLimit", dest="noProgressLimit",
        default=1000, help="The number of times the algorithm cannot progress")

    parser.add_option("-p", "--improve", dest="improve",
        default=False,
        help="Create new timetables then False, want to improve existing True",
        action="store_true")

    parser.add_option("-s", "--student_optimization",
        dest="student_optimization", default=False,
        help="Use student_optimization if improve is also used",
        action="store_true")

    (options, args) = parser.parse_args()

    if not options.improve:
        run4_swap_hill_climber(int(options.nIterations),
            int(options.noProgressLimit))
    else:
        run4_improve(int(options.nIterations),
            int(options.noProgressLimit),
            options.student_optimization)
