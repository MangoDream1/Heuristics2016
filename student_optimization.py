from process_data import *
from iteration_manager import *
from random import choice
from operator import itemgetter


def lecture_students_swap(im, noProgressCounterLimit):
    noProgressCounter = 0

    problem_list = [s for s in im.students if s.score != 0]

    while noProgressCounter != noProgressCounterLimit:
        changed_lectures = []

        rLecture = choice(im.lectures)

        # If no siblings than no improvements can be made here
        if not rLecture.siblings:
            continue

        if problem_list:
            rLectureProblemStudents = [s for s in problem_list
                                        if s in rLecture.students]

            if rLectureProblemStudents:
                rStudent = choice(rLectureProblemStudents)
            else:
                continue
        else:
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
        noProgressCounterLimit))


iteration_manager.importLectures(input("Enter the timetable that "
                                       "needs optimization: "))
iteration_manager.exportTimetable()


lecture_students_swap(iteration_manager, 10000)
