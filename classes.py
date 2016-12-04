from copy import copy
import math
import json
import os

# Global variables

NUMBER_OF_SLOTS = 4
TIMESLOTS = {0: "9-11", 1: "11-13", 2: "13-15", 3: "15-17", 4: "17-19"}
DAYS = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
        4: "Friday", 5: "Saturday", 6: "Sunday"}


print("Creating classes...")

# --------------
# Classes:

class Lecture:
    def __init__(self, name, lecture_number, subject, maxStud):
        self.subject = subject
        self.lecture_number = lecture_number
        self.name = name
        self.group = 0
        self.classroom = None

        self.siblings = []

        if maxStud == "nvt":
            self.maxStud = 0
        else:
            self.maxStud = int(maxStud)

        self.students = []

        # Default timetable settings
        self.day = 0
        self.timeslot = 0

    def long_str(self):
        return "Name: %s | Lecture number: %s | Group: %s | maxStud: %s" % (self.name, self.lecture_number, self.group, self.maxStud)

    def __str__(self):
        return self.name[0] + str(self.lecture_number) + chr(ord('A') + self.group) + str(len(self.students))

    def assignLecturetoAll(self):
        self.assignLectureToStudents()
        self.assignLecturetoClassroom()
        self.assignLecturetoSubject()

    def assignLectureToStudents(self):
        for student in self.students:
            student.lectures.append(self)

    def assignLecturetoClassroom(self):
        self.classroom.lectures.append(self)

    def assignLecturetoSubject(self):
        self.subject.lectures.append(self)

    def getChangingDataDict(self):
        # This is the data of the lecture object that changes during algorithm iterations
        return {"day": self.day, "timeslot": self.timeslot, "classroom": self.classroom.getId()}

    def toDict(self):
        return {"subject": self.subject.name, "classroom": self.classroom.__str__(),
                "string": self.__str__()}

    def toLongDict(self):
        return {
            "subject": self.subject.getId(),
            "lecture_number": self.lecture_number,
            "name": self.name,
            "group": self.group,
            "classroom": self.classroom.getId(),
            "maxStud": self.maxStud,
            "students": [x.getId() for x in self.students],
            "day": self.day,
            "timeslot": self.timeslot
        }

class Timetable:
    def __init__(self):
        # Empty timetable with 5 days and the number of slots
        self.timetable = {x: {y: [] for y in range(NUMBER_OF_SLOTS)} for x in range(5)}
        self.jsonDict = {x: {y: [] for y in range(NUMBER_OF_SLOTS)} for x in range(5)}

        self.score = 0

    def clearLectures(self):
        self.lectures = []

    def getLectures(self):
        return [x for x in self.lectures if x.name == "Lecture"]

    def getWorkLectures(self):
        return [x for x in self.lectures if x.name == "WorkLecture"]

    def getPracticas(self):
        return [x for x in self.lectures if x.name == "Practica"]

    def exportTimetable(self):
        self.fillInTimetable()

        self.jsonDict = {x: {y: [] for y in range(NUMBER_OF_SLOTS)} for x in range(5)}

        for x in self.timetable.keys():
            for y in self.timetable[x].keys():
                self.jsonDict[x][y] = self.timetable[x][y]

        for day, timeslot in self.jsonDict.items():
            for key, lectures in timeslot.items():
                nLectures = [lecture.toDict() for lecture in lectures]

                self.jsonDict[day][key] = nLectures

        if not os.path.exists("Timetable/%s" % self.__class__.__name__):
            os.makedirs("Timetable/%s" % self.__class__.__name__)

        with open("Timetable/%s/%s.json" % (self.__class__.__name__, self.getId()), 'w') as f:
            json.dump(self.jsonDict, f, indent=3)

    def fillInTimetable(self):
        self.timetable = {x: {y: [] for y in range(NUMBER_OF_SLOTS)} for x in range(5)}

        for lecture in self.lectures:
            self.timetable[lecture.day][lecture.timeslot].append(lecture)

class Classroom(Timetable):
    def __init__(self, room_number, capacity):
        super().__init__()

        self.room_number = room_number
        self.capacity = int(capacity)
        self.lectures = []

    def getId(self):
        return self.room_number

    def __str__(self):
        return self.room_number

class Subject(Timetable):
    def __init__(self, name, n_lectures, n_workLectures, w_maxStud,
                 n_practicas, p_maxStud):

        super().__init__()
        self.name = name

        self.lectures = [Lecture("Lecture", i, self, "nvt") for i in range(int(n_lectures))] + \
                        [Lecture("WorkLecture", i, self, w_maxStud) for i in range(int(n_workLectures))] + \
                        [Lecture("Practica", i, self, p_maxStud) for i in range(int(n_practicas))]

        self.students = []

    def getId(self):
        return self.name

    def __str__(self):
        return self.name

    def assignStudentsToLectures(self):
        if self.lectures:
            newLectures = []

            for lecture in self.lectures:
                if lecture.maxStud:
                    # Calculate number of groups and the number of students per lecture then round up
                    nGroups = math.ceil(len(self.students) / lecture.maxStud)
                    lectureSize = math.ceil(len(self.students) / nGroups)

                    if nGroups > 1:
                        # For every work lecture, there are the same groups that need to be filled
                        # But these groups also need to be created
                        for groupNumber in range(nGroups):
                            nLecture = copy(lecture)
                            nLecture.group = groupNumber

                            nLecture.students = self.students[groupNumber*\
                                lectureSize:(groupNumber+1)*lectureSize]

                            nLecture.assignLectureToStudents()
                            newLectures.append(nLecture)

                            lecture.siblings.append(nLecture)
                    else:
                        # Only one group, thus every student in the same group
                        lecture.students = self.students
                        lecture.assignLectureToStudents()
                        newLectures.append(lecture)
                else:
                    # Has no maxStud thus no groups needed
                    lecture.students = self.students
                    lecture.assignLectureToStudents()
                    newLectures.append(lecture)

            # Add connected lectures to sibling list
            for lecture in newLectures:
                for sibling in lecture.siblings:
                    if lecture not in sibling.siblings:
                        sibling.siblings.append(lecture)

            # Remove self from sibling list
            for lecture in newLectures:
                # Copy needed because every above created sibling lists
                # use same pointer thus removing from one removed from all
                lecture.siblings = copy(lecture.siblings)

                if lecture in lecture.siblings:
                    lecture.siblings.remove(lecture)

            self.lectures = newLectures

class Student(Timetable):
    def __init__(self, surname, name, studentId, subject1, subject2,
                 subject3, subject4, subject5):

        super().__init__()

        self.surname = surname
        self.name = name
        self.studentId = studentId

        self.__subjectNames = []
        self.__addSubject(subject1)
        self.__addSubject(subject2)
        self.__addSubject(subject3)
        self.__addSubject(subject4)
        self.__addSubject(subject5)

        self.subjects = []
        self.lectures = []

        self.__cleanUp()

    def getId(self):
        return self.studentId

    def __str__(self):
        return "%s %s %s" % (self.name, self.surname, self.studentId)

    def __addSubject(self, subject):
        if subject != "":
            self.__subjectNames.append(subject)

    def __addStudentToSubject(self):
        for subject in self.subjects:
            subject.students.append(self)

    def __cleanUp(self):
        # Fixes CSV errors

        for i, x in enumerate(self.__subjectNames):
            if x == "Zoeken":
                self.__subjectNames[i] = "Zoeken, sturen en bewegen"
            if x == " sturen en bewegen":
                del self.__subjectNames[i]
            if x == "Compilerbouw practicum":
                self.__subjectNames[i] = "Compilerbouw (practicum)"
            if x == "Informatie- en organsatieontwerp":
                self.__subjectNames[i] = "Informatie- en organisatieontwerp"

    def assignSubjectToStudent(self, subject_dct):
        for subjectName in self.__subjectNames:
            self.subjects.append(subject_dct[subjectName])

        self.__addStudentToSubject()
