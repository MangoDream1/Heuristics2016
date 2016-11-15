from score_system import *
from process_data import *

class IterationManager:
    def __init__(self, lecture_dct):
        self.iteration_dct = {}
        self.lecture_dct = lecture_dct

        self.i = 0

    def addChanges(self, changed_lectures):
        self.iteration_dct[self.i] = {self.lecture_dct[x]:x.getChangingDataDict()
                                    for x in changed_lectures}
        self.iteration_dct[self.i]["base"] = False

        for x in subjects + students + classrooms:
            x.clearLectures()

        for x in lecture_dct.keys():
            if type(x) != int:
                x.assignLecturetoAll()

        self.iteration_dct[self.i]["score"] = ScoreSystem(subjects, students, classrooms).score

        return self.iteration_dct

    def compileChanges(self, i):
        # Find nearest base
        base = 0
        for x in reversed(range(i)):
            if self.iteration_dct[i]["base"]:
                base = i
                break

        compiled_result = {}
        for x in range(base, i+1):
            for key, data in self.iteration_dct[i].items():
                if key != "base":
                    compiled_result[key] = data

        return compiled_result

    def createBase(self):
        self.iteration_dct[self.i] = self.compileChanges(self.i)
        self.iteration_dct[self.i]["base"] = True

        return self.iteration_dct

    def applyChanges(self, compiled_changes):
        for index, data in compiled_changes.items():
            if index not in ["base", "score"]:
                lecture = self.lecture_dct[index]

                lecture.day = data["day"]
                lecture.timeslot = data["timeslot"]
                lecture.classroom = classroom_dct[data["classroom"]]

        for x in subjects + students + classrooms:
            x.clearLectures()

        for x in lecture_dct.keys():
            if type(x) != int:
                x.assignLecturetoAll()

        return self.lecture_dct
