from process_data import *
from data_manager import *

from random import choice, random
from operator import itemgetter
from optparse import OptionParser


def find_problem_lectures(lectures):
    """ Find the lectures that have a student that has overlap because of it.
        This will speedup the process. Otherwise perfectly fine lectures will
        also be chosen where no improvements can be made anyway.
    """

    problem_lectures = []

    # Only take the lectures that have siblings otherwise cannot change a thing
    lectures = [l for l in lectures if l.siblings]

    for l in lectures:
        # Checks for every lectures if there is a student that has overlap because
        # of that lecture
        for s in l.students:
            if s.score != 0 and len(s.timetable[l.day][l.timeslot]) > 1:
                problem_lectures.append(l)
                break

        # If not 20 then subject score is not perfectly distributed, might be
        # increased here
        if int(l.subject.score) != 20:
            print(l.subject, l.subject.score)
            problem_lectures.append(l)

    return problem_lectures

def lecture_students_swap(dm, noProgressLimit):
    """ Hill climber with swap just as in swap_hill_climber. Now will find
        students in lectures and will swap with other students in sibling
        lectures to find best spread of students. Will continue searching until
        noProgressCounter reached noProgressLimit.
    """

    noProgressCounter = 0

    while noProgressCounter != noProgressLimit:
        changed_lectures = []

        # Select random lecture from problem lectures
        rLecture = choice(find_problem_lectures(dm.lectures))

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

        # Save new and old lectures
        changed_lectures.append(rLecture)
        changed_lectures.append(nLecture)

        dm.addChanges(changed_lectures, withStudents=True)

        # If higher then save otherwise discard
        if dm.iteration_dct[dm.i]["score"] > \
           dm.iteration_dct[dm.i - 1]["score"]:

            dm.plot.addScore(dm.iteration_dct[dm.i]["score"])

            if dm.i % 10 == 0:
                print(dm.iteration_dct[dm.i]["score"])

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

    dm.exportLectures("STUDENT_OPTIMIZED%snPl%s" % (round(score),
        noProgressLimit))

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-n", "--noProgressLimit", dest="noProgressLimit",
        default=1000, help="The number of times the algorithm is allowed not to progress")

    (options, args) = parser.parse_args()

    data_manager.importLectures(input("Enter the timetable that "
                                           "needs optimization: "))

    lecture_students_swap(data_manager, options.noProgressLimit)
