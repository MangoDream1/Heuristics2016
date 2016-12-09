from process_data import *
from iteration_manager import *
from random import randint, choice
from operator import itemgetter

def update_progress(workdone, text='Progress:'):
    print("\r{0} [{1:50s}] {2:.1f}%".format(text, '#' * int(workdone * 50),
    workdone*100), end="", flush=True)

    if workdone == 1:
        print('\n')

def random_location(lecture, im, no_overlap=False):
    overlap = True

    while overlap:
        lecture.day = randint(0, 4)
        lecture.timeslot = randint(0, 3)
        lecture.classroom = choice(im.classrooms)

        if no_overlap:
            slot = lecture.classroom.timetable[lecture.day][lecture.timeslot]
            slot.append(lecture)

            overlap = lecture.classroomOverlap()

            if overlap:
                slot.remove(lecture)
        else:
            overlap=False

    return lecture

def random_timetables(im, nPlannedIterations, no_overlap):
    print("Starting random timetables with %s iterations..."
            % nPlannedIterations)

    while im.i != nPlannedIterations:
        changed_lectures = []

        for lecture in im.lectures:
            changed_lectures.append(
                random_location(lecture, im, no_overlap=no_overlap))

        im.addChanges(changed_lectures)

        # Makes all base since its all random anyways
        im.createBase()

        im.i += 1
        update_progress(im.i/nPlannedIterations)

        for x in im.subjects + im.students + im.classrooms:
            x.timetable = {x: {y: [] for y in range(NUMBER_OF_SLOTS)} for x in range(5)}

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

random_timetables(iteration_manager, 1000, True)
