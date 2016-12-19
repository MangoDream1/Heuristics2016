from score_system import *
from plot import *

from random import randint, choice
from operator import itemgetter

class DataManager:
    ''' The DataManager class contains all the data needed for the algorithms.
        Also contains several helpfull functions that are used by the
        algorithms'''

    def __init__(self, classrooms, subjects, students):
        # Saves changes of all previous iterations. Doesnt save whole timetables
        # only the changed lectures
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

        # Two way dictionary for finding lectures and the lecture index
        self.lectures = [lecture for subject in subjects for lecture in subject.lectures]
        self.lecture_dct = {index: lecture for index, lecture in enumerate(self.lectures)}
        self.lecture_dct = dict(self.lecture_dct.items() | dict(reversed(item) for item in self.lecture_dct.items()).items())

        # The current iteration
        self.i = 0

        # New instance of plot and score system
        self.score_system = ScoreSystem(self)
        self.plot = Plot()


    def resetLectures(self):
        # Clear all lectures from subjects, students and classrooms
        for x in self.subjects + self.students + self.classrooms:
            x.clearLectures()

        # Append all lectures to correct subject, students and classroom
        for x in self.lectures:
            x.assignLecturetoAll()


    def resetTimetables(self):
        # Clear timetable for all
        for x in self.subjects + self.students + self.classrooms:
            x.clearTimetable()


    def addChanges(self, changed_lectures, withStudents=False):
        #Add dictionary of lectures index as key and changingDataDict as value
        self.iteration_dct[self.i] = {self.lecture_dct[l]:l.getChangingDataDict()
                                        for l in changed_lectures}

        # if withStudents also add students to changes
        if withStudents:
            for l in changed_lectures:
                dct = self.iteration_dct[self.i][self.lecture_dct[l]]
                dct["students"] = [s.getId() for s in l.students]

        # Base default false
        self.iteration_dct[self.i]["base"] = False

        # Reset lectures then calculate score and add to dict
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

        # From base add all changes until i
        # This is the compiled result
        compiled_result = {}
        for x in range(base, i+1):
            for key, data in self.iteration_dct[x].items():
                compiled_result[key] = data

        return compiled_result


    def createBase(self):
        # Create a base by compiling all to this point
        self.iteration_dct[self.i] = self.compileChanges(self.i)
        self.iteration_dct[self.i]["base"] = True


    def applyChanges(self, compiled_changes):
        # Change the values of the current lecture object so that it matches
        # the compiled changes
        for index, data in compiled_changes.items():
            if index not in ["base", "score"]:
                lecture = self.lecture_dct[index]

                lecture.day = data["day"]
                lecture.timeslot = data["timeslot"]
                lecture.classroom = self.classroom_dct[data["classroom"]]

                try:
                    lecture.students = [self.student_dct[s]
                        for s in data["students"]]
                except KeyError:
                    pass

        self.resetLectures()

        return self.lecture_dct


    def randomLocation(self, lecture, no_overlap=False):
        # Find a random location for a lecture. If no_overlap is True
        # keep looking until a space has been found where no other lectures
        # are.

        overlap = True
        while overlap:
            lecture.day = randint(0, 4)
            lecture.timeslot = randint(0, 3)
            lecture.classroom = choice(self.classrooms)

            if no_overlap:
                slot = lecture.classroom.timetable\
                    [lecture.day][lecture.timeslot]

                # If slot is empty then lecture can be placed here
                if not slot:
                    slot.append(lecture)
                    overlap=False
            else:
                overlap=False

        return lecture


    def removeOverlap(self):
        # Go through the timetables to find overlap and remove it randomly

        for x in self.classrooms:
            x.fillInTimetable()

        overlap_lectures = [l for l in self.lectures if l.classroomOverlap()]

        for l in overlap_lectures:
            l.classroom.lectures.remove(l)
            l.classroom.timetable[l.day][l.timeslot] = []

        for l in overlap_lectures:
            self.randomLocation(l, no_overlap=True)

        self.resetLectures()

        for x in self.classrooms + self.students + self.subjects:
            x.fillInTimetable()


    def compileBest(self):
        # Find the best score in iteration_dct and compile it

        best_iteration, score = max([(i, self.iteration_dct[i]["score"])
                                for i in self.iteration_dct.keys()],
                                key=itemgetter(1))

        compiled_changes = self.compileChanges(best_iteration)
        self.applyChanges(compiled_changes)

        return best_iteration, score


    def exportLectures(self, file_name, plot=True):
        # Export the current timetable to file_name. Exports timetable, score
        # distribution and a plot if plot=True

        export_dct = [x.toLongDict() for x in self.lectures]

        if not os.path.exists("Timetable/Lectures"):
            os.makedirs("Timetable/Lectures")

        # Prevent same scores from being overwritten by sticking a number on
        # the end if the same score has already been calculated by the same
        # algorithm
        if os.path.exists("Timetable/Lectures/%s.json" % file_name):
            number = len([f for f in os.listdir("Timetable/Lectures")
                            if file_name in f])

            file_name = file_name + "n" + str(number)

        with open("Timetable/Lectures/%s.json" % file_name, 'w') as f:
            json.dump(export_dct, f, indent=3)

        # Recalculate score
        self.score_system.total_score()

        # The score dct that is going to be saved
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

        # Export plot
        if plot:
            self.plot.plotTime(file_name)


    def exportTimetable(self):
        # Export all the objects with timetables so it can be read by webview
        for x in self.subjects + self.students + self.classrooms:
            x.exportTimetable()


    def importLectures(self, file_name):
        # Import lecture file and apply contents

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
