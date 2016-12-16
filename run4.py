from swap_hill_climber import swap_hill_climber
from process_data import *

from optparse import OptionParser
from multiprocessing import Process

def run4_swap_hill_climber(nIterations, noProgressLimit=1000):
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

if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option("-i", "--nIterations", dest="nIterations",
        default=100, help="The number of timetables that need to be created")


    parser.add_option("-n", "--noProgressLimit", dest="noProgressLimit",
        default=1000, help="The number of times the algorithm cannot progress")

    (options, args) = parser.parse_args()

    run4_swap_hill_climber(int(options.nIterations),
        int(options.noProgressLimit))
