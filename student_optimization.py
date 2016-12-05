from process_data import *
from iteration_manager import *
from random import choice
from operator import itemgetter


def lecture_students_swap(im, noProgressCounterLimit):
    noProgressCounter = 0

    while noProgressCounter != noProgressCounterLimit:
        changed_lectures = []

        rLecture = choice(im.lectures)

        # If no siblings than no improvements can be made here
        if not rLecture.siblings:
            continue

        # Choice random student from lecture and remove from pool
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

        else:
            # Reset to previous state
            im.applyChanges(im.compileChanges(im.i - 1))
            noProgressCounter += 1

    best_iteration = max([(i, im.iteration_dct[i]["score"])
                            for i in im.iteration_dct.keys()],
                            key=itemgetter(1))

    print("Best iteration: %s, Score: %s" % (best_iteration[0],
                                             best_iteration[1]))

    im.applyChanges(im.compileChanges(best_iteration[0]))

    im.exportLectures("STUDENT_OPTIMIZED%snPl%s" % (best_iteration[1],
        noProgressCounterLimit))


iteration_manager.importLectures(input("Enter the timetable that "
                                       "needs optimization: "))
iteration_manager.exportTimetable()


lecture_students_swap(iteration_manager, 1000)
