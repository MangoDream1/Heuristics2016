from process_data import *
from score_system import *

# Two way dictionary for finding lectures
lectures = [lecture for subject in subjects for lecture in subject.lectures]
lecture_dct = {index: lecture for index, lecture in enumerate(lectures)}
lecture_dct = dict(lecture_dct.items() | dict(reversed(item) for item in lecture_dct.items()).items())

def addChanges(changed_lectures, i, iteration_dct, lecture_dct):
    iteration_dct[i] = {lecture_dct[x]:x.getChangingDataDict() for x in changed_lectures}
    iteration_dct[i]["base"] = False
    iteration_dct[i]["score"] = ScoreSystem(subjects, students, classrooms).score

    return iteration_dct

def compileChanges(i, iteration_dct):
    # Find nearest base
    base = 0
    for x in reversed(range(i)):
        if iteration_dct[i]["base"]:
            base = i
            break

    compiled_result = {}
    for x in range(base, i+1):
        for key, data in iteration_dct[i].items():
            if key != "base":
                compiled_result[key] = data

    return compiled_result

def createBase(i, iteration_dct):
    iteration_dct[i] = compileChanges(i, iteration_dct)
    iteration_dct[i]["base"] = True

    return iteration_dct

def applyChanges(compiled_changes, lecture_dct):
    for index, data in compiled_changes.items():
        if index not in ["base", "score"]:
            lecture = lecture_dct[index]

            lecture.day = data["day"]
            lecture.timeslot = data["timeslot"]
            lecture.classroom = classroom_dct[data["classroom"]]

    return lecture_dct
