from score_system import *

class IterationManager:
    def __init__(self, classrooms, subjects, students):
        self.iteration_dct = {}

        self.classrooms = classrooms
        self.classroom_dct = {x.getId(): x for x in classrooms}

        self.subjects = subjects
        self.subject_dct = {x.getId(): x for x in subjects}

        self.students = students
        self.student_dct = {x.getId(): x for x in students}

        for student in self.students:
            student.assignSubjectToStudent(self.subject_dct)

        # Assign students to lectures
        for subject in self.subjects:
            subject.assignStudentsToLectures()

        self.score_system = ScoreSystem(self.subjects, self.students, self.classrooms)

        # Two way dictionary for finding lectures
        self.lectures = [lecture for subject in subjects for lecture in subject.lectures]
        self.lecture_dct = {index: lecture for index, lecture in enumerate(self.lectures)}
        self.lecture_dct = dict(self.lecture_dct.items() | dict(reversed(item) for item in self.lecture_dct.items()).items())

        self.i = 0


    def resetLectures(self):
        for x in self.subjects + self.students + self.classrooms:
            x.clearLectures()

        for x in self.lectures:
            x.assignLecturetoAll()


    def addChanges(self, changed_lectures, withStudents=False):
        self.iteration_dct[self.i] = {self.lecture_dct[l]:l.getChangingDataDict()
                                        for l in changed_lectures}

        if withStudents:
            for l in changed_lectures:
                dct = self.iteration_dct[self.i][self.lecture_dct[l]]
                dct["students"] = [s.getId() for s in l.students]


        self.iteration_dct[self.i]["base"] = False

        self.resetLectures()

        self.iteration_dct[self.i]["score"] = self.score_system.total_score()

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
            for key, data in self.iteration_dct[x].items():
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

                self.lecture_dct[index].day = data["day"]
                self.lecture_dct[index].timeslot = data["timeslot"]
                self.lecture_dct[index].classroom = self.classroom_dct[data["classroom"]]

                try:
                    self.lecture_dct[index].students = [self.student_dct[s]
                        for s in data["students"]]
                except KeyError:
                    pass

        self.resetLectures()

        return self.lecture_dct

    def exportLectures(self, file_name):
        export_dct = [x.toLongDict() for x in self.lectures]

        if not os.path.exists("Timetable/Lectures"):
            os.makedirs("Timetable/Lectures")

        with open("Timetable/Lectures/%s.json" % file_name, 'w') as f:
            json.dump(export_dct, f, indent=3)

        self.score_system.total_score()

        score_dct = {"classrooms":
                        {x.getId(): x.score for x in self.classrooms},
                     "subjects":
                        {x.getId(): x.score for x in self.subjects},
                     "students":
                        {x.getId(): x.score for x in self.students},
                     "totals":
                        {
                            "classroom": sum(x.score for x in self.classrooms),
                            "subjects": round(sum(x.score
                                for x in self.subjects)),
                            "students": sum(x.score for x in self.students)
                        }
                    }

        if not os.path.exists("Timetable/Scores"):
            os.makedirs("Timetable/Scores")

        with open("Timetable/Scores/%s.json" % file_name, 'w') as f:
            json.dump(score_dct, f, indent=3)

    def exportTimetable(self):
        for x in self.subjects + self.students + self.classrooms:
            x.exportTimetable()

    def importLectures(self, file_name):
        file_name = file_name.replace(".json", "")
        path = "Timetable/Lectures/%s.json" % file_name

        with open(path) as f:
            data_list = json.load(f)

        lectures = []

        for dct in data_list:
            l = Lecture(dct["name"], dct["lecture_number"],
                        self.subject_dct[dct["subject"]], dct["maxStud"])

            l.classroom = self.classroom_dct[dct["classroom"]]
            l.day = dct["day"]
            l.timeslot = dct["timeslot"]
            l.students = [self.student_dct[x] for x in dct["students"]]
            l.group = dct["group"]

            lectures.append(l)

        self.lectures = lectures
        self.lecture_dct = {index: lecture for index, lecture in enumerate(self.lectures)}
        self.lecture_dct = dict(self.lecture_dct.items() | dict(reversed(item) for item in self.lecture_dct.items()).items())

        self.resetLectures()

        for subject in self.subjects:
            subject.createSiblings()

        # Adds the new lectures to changes, so that algorithms can work with the loaded data
        self.addChanges(self.lectures, withStudents=True)
        self.i += 1

        return self.lectures
