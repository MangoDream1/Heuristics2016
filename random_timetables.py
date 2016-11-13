from process_data import *
from score_system import *
from iteration_management import *
from random import randint, choice
from operator import itemgetter

iteration = 0
iteration_dct = {}


while iteration != 1000:
    changed_lectures = []

    for lecture in lectures:
        lecture.day = randint(0, 4)
        lecture.timeslot = randint(0, 3)
        lecture.classroom = choice(classrooms)

        changed_lectures.append(lecture)

    iteration_dct = addChanges(changed_lectures, iteration, iteration_dct, lecture_dct)

    # Makes all base since its all random anyways
    iteration_dct = createBase(iteration, iteration_dct)

    iteration += 1

best_iteration = max([(i, iteration_dct[i]["score"]) for i in iteration_dct.keys()], key=itemgetter(1))

print("Best iteration: %s, Score: %s" % (best_iteration[0], best_iteration[1]))

compiled_changes = compileChanges(best_iteration[0], iteration_dct)
lecture_dct = applyChanges(compiled_changes, lecture_dct)

for x in subjects + students + classrooms:
    x.clearLectures()

for x in lectures:
    x.assignLecturetoAll()

for x in subjects + students + classrooms:
    x.exportTimetable()
