import copy
import math
import json
import os

NUMBER_OF_SLOTS = 4


print("Creating classes...")

# --------------
# Classes:

class Lecture:
    def __init__(self, name, lecture_number, subject, maxStud):
        self.subject = subject
        self.lecture_number = lecture_number
        self.name = name
        self.group = 0
        self.classRoom = None

        if maxStud == "nvt":
            self.maxStud = 0
        else:
            self.maxStud = int(maxStud)

        self.students = []

        # Default roster settings
        self.day = 0
        self.timeslot = 0

    def __str__(self):
        return "Name: %s | Lecture number: %s | Group: %s | maxStud: %s" % (self.name, self.lecture_number, self.group, self.maxStud)

    def assignLectureToStudents(self):
        print(self.name)

        for student in self.students:
            student.lectures.append(self)

    def toDict(self):
        return {"name": self.name, "subject": self.subject.name,
                "lecture_number": self.lecture_number, "group": self.group,
                "classRoom": self.classRoom}

class Roster:
    def __init__(self):
        # Empty roster with 7 days and the number of slots
        self.roster = {x: {y: [] for y in range(NUMBER_OF_SLOTS)} for x in range(7)}

    def getLectures(self):
        return [x for x in self.lectures if x.name == "Lecture"]

    def getWorkLectures(self):
        return [x for x in self.lectures if x.name == "WorkLecture"]

    def getPractica(self):
        return [x for x in self.lectures if x.name == "Practica"]

    def exportRoster(self):
        self.fillInRoster()

        if not os.path.exists(self.__class__.__name__):
            os.makedirs(self.__class__.__name__)

        with open("%s/%s.json" % (self.__class__.__name__, self.getId()), 'w') as f:
            json.dump(self.roster, f, indent=3)

    def fillInRoster(self):
        for lecture in self.lectures:
            self.roster[lecture.day][lecture.timeslot].append(lecture.toDict())

class ClassRoom(Roster):
    def __init__(self, room_number, capacity):
        super().__init__()

        self.room_number = room_number
        self.capacity = capacity
        self.lectures = []

    def getId(self):
        return self.room_number

    def __str__(self):
        return self.room_number

class Subject(Roster):
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
        if len(self.lectures):
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
                            lecture = copy.copy(lecture)
                            lecture.group = groupNumber

                            lecture.students = self.students[groupNumber*lectureSize:(groupNumber+1)*lectureSize]

                            lecture.assignLectureToStudents()
                            newLectures.append(lecture)

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

            self.lectures = newLectures

class Student(Roster):
    def __init__(self, surname, name, studentId, subject1, subject2,
                 subject3, subject4, subject5, subject_dct):

        super().__init__()

        self.surname = surname
        self.name = name
        self.studentId = studentId

        self.subjectNames = []
        self.__addSubject(subject1)
        self.__addSubject(subject2)
        self.__addSubject(subject3)
        self.__addSubject(subject4)
        self.__addSubject(subject5)

        self.subjects = []
        self.lectures = []

        self.__cleanUp()
        self.__fillInSubject(subject_dct)
        self.__addStudentToSubject()

    def getId(self):
        return self.studentId

    def __str__(self):
        return "%s %s %s" % (self.name, self.surname, self.studentId)

    def __addSubject(self, subject):
        if subject != "":
            self.subjectNames.append(subject)

    def __addStudentToSubject(self):
        for subject in self.subjects:
            subject.students.append(self)

    def __cleanUp(self):
        # Fixes CSV errors

        for i, x in enumerate(self.subjectNames):
            if x == "Zoeken":
                self.subjectNames[i] = "Zoeken, sturen en bewegen"
            if x == " sturen en bewegen":
                del self.subjectNames[i]
            if x == "Compilerbouw practicum":
                self.subjectNames[i] = "Compilerbouw (practicum)"
            if x == "Informatie- en organsatieontwerp":
                self.subjectNames[i] = "Informatie- en organisatieontwerp"

    def __fillInSubject(self, subject_dct):
        for subjectName in self.subjectNames:
            self.subjects.append(subject_dct[subjectName])
