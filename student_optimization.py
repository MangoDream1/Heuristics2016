from process_data import *
from iteration_manager import *

from random import choice, random
from operator import itemgetter
from optparse import OptionParser


def find_problem_lectures(lectures):
    problem_lectures = []

    # Only take the lectures that have siblings otherwise cannot change a thing
    lectures = [l for l in lectures if l.siblings]

    # Checks for every lectures if there is a student that has overlap because
    # of that lecture
    for l in lectures:
        for s in l.students:
            if s.score != 0 and len(s.timetable[l.day][l.timeslot]) > 1:
                problem_lectures.append(l)
                break

    return problem_lectures

def lecture_students_swap(im, noProgressLimit):
    noProgressCounter = 0

    while noProgressCounter != noProgressLimit:
        changed_lectures = []

        # Select random lecture from problem lectures
        rLecture = choice(find_problem_lectures(im.lectures))

        # Choice random student from lecture
        rStudent = choice(rLecture.students)

        rLecture.students.remove(rStudent)

        # Choice new lecture location from siblings
        nLecture = choice(rLecture.siblings)

        # Add if enough space otherwise swap with other student
        if nLecture.maxStud > len(nLecture.students):
            nLecture.students.append(rStudent)
        else:
            swapStudent = choice(nLecture.students)
            nLecture.students.remove(swapStudent)

            nLecture.students.append(rStudent)
            rLecture.students.append(swapStudent)

        changed_lectures.append(rLecture)
        changed_lectures.append(nLecture)

        im.addChanges(changed_lectures, withStudents=True)


        if im.iteration_dct[im.i]["score"] > \
           im.iteration_dct[im.i - 1]["score"]:

            im.plot.addScore(im.iteration_dct[im.i]["score"])

            if im.i % 10 == 0:
                print(im.iteration_dct[im.i]["score"])

                im.createBase()

            im.i += 1
            noProgressCounter = 0
            problem_list = [s for s in im.students if s.score != 0]

        else:
            # Reset to previous state
            im.applyChanges(im.compileChanges(im.i - 1))
            noProgressCounter += 1

    best_iteration, score = im.compileBest()

    print("Best iteration: %s, Score: %s" % (best_iteration, round(score)))

    im.exportLectures("STUDENT_OPTIMIZED%snPl%s" % (round(score),
        noProgressLimit))

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-n", "--noProgressLimit", dest="noProgressLimit",
        default=1000, help="The number of times the algorithm cannot progress")

    (options, args) = parser.parse_args()

    iteration_manager.importLectures(input("Enter the timetable that "
                                           "needs optimization: "))

    lecture_students_swap(iteration_manager, options.noProgressLimit)
