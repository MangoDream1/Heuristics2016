from process_data import *
from iteration_manager import *
from random import randint, choice
from operator import itemgetter

def update_progress(workdone, text='Progress:'):
    print("\r{0} [{1:50s}] {2:.1f}%".format(text, '#' * int(workdone * 50),
    workdone*100), end="", flush=True)

    if workdone == 1:
        print('\n')

def random_timetables(im, nPlannedIterations):
    print("Starting random timetables with %s iterations..."
            % nPlannedIterations)

    while im.i != nPlannedIterations:
        changed_lectures = []

        for lecture in im.lectures:
            lecture.day = randint(0, 4)
            lecture.timeslot = randint(0, 3)
            lecture.classroom = choice(classrooms)

            changed_lectures.append(lecture)

        im.addChanges(changed_lectures)

        # Makes all base since its all random anyways
        im.createBase()

        im.i += 1
        update_progress(im.i/nPlannedIterations)

    best_iteration = max([(i, im.iteration_dct[i]["score"])
                            for i in im.iteration_dct.keys()],
                            key=itemgetter(1))

    average = sum([im.iteration_dct[i]["score"]
                    for i in im.iteration_dct.keys()]) / nPlannedIterations

    print("Best iteration: %s, Score: %s, Average Score: %s" %
                (best_iteration[0], round(best_iteration[1]), round(average)))

    compiled_changes = im.compileChanges(best_iteration[0])
    im.applyChanges(compiled_changes)

    im.exportLectures("RT%si%s" % (round(best_iteration[1]),
        nPlannedIterations))

    return im.lecture_dct

random_timetables(iteration_manager, 1000)
