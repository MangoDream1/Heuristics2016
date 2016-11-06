
# coding: utf-8

# --------------
# Get Data:

import copy
import math

print("Getting data...")

g = lambda x: [y.strip() for y in x]

classRooms = [
    "A1.04 	41",
    "A1.06 	22",
    "A1.08 	20",
    "A1.10 	56",
    "B0.201 	48",
    "C0.110 	117",
    "C1.112 	60",]

classRooms = [g(x.split("\t")) for x in classRooms]

subjects = """Advanced Heuristics 	1 	0 	nvt 	1 	10
Algoritmen en complexiteit 	1 	1 	25 	1 	25
Analysemethoden en -technieken 	1 	0 	nvt 	0 	nvt
Architectuur en computerorganisatie 	2 	0 	nvt 	0 	nvt
Autonomous Agents 2 	2 	1 	10 	1 	10
Bioinformatica 	3 	1 	20 	1 	20
Calculus 2 	1 	1 	40 	0 	nvt
Collectieve Intelligentie 	3 	1 	20 	1 	20
Compilerbouw 	2 	1 	40 	1 	40
Compilerbouw (practicum) 	0 	0 	nvt 	1 	15
Data Mining 	2 	1 	10 	1 	10
Databases 2 	1 	1 	40 	0 	nvt
Heuristieken 1 	1 	1 	25 	0 	nvt
Heuristieken 2 	1 	1 	20 	0 	nvt
Informatie- en organisatieontwerp 	2 	1 	15 	1 	15
Interactie-ontwerp 	2 	0 	nvt 	0 	nvt
Kansrekenen 2 	2 	0 	nvt 	0 	nvt
Lineaire Algebra 	2 	0 	nvt 	0 	nvt
Machine Learning 	2 	0 	nvt 	0 	nvt
Moderne Databases 	1 	1 	20 	1 	20
Netwerken en systeembeveiliging 	0 	0 	nvt 	1 	20
Programmeren in Java 2 	0 	0 	nvt 	1 	20
Project Genetic Algorithms 	0 	0 	nvt 	1 	15
Project Numerical Recipes 	0 	0 	nvt 	1 	15
Reflectie op de digitale cultuur 	2 	1 	20 	0 	nvt
Software engineering 	1 	1 	40 	1 	40
Technology for games 	2 	1 	20 	0 	nvt
Webprogrammeren en databases 	2 	1 	20 	1 	20
Zoeken, sturen en bewegen 	0 	0 	nvt 	1 	15"""

subjects = [g(x.split("\t")) for x in subjects.split("\n")]
students = []

import csv

with open('studenten_roostering.csv', 'r') as csvfile:
    r = csv.reader(csvfile, delimiter=',', quotechar='|')

    # Skip title
    next(r, None)

    for row in r:
        students.append(row)


print("Creating classes...")

# --------------
# Classes:

class ClassRoom:
    def __init__(self, room_number, capacity):
        self.room_number = room_number
        self.capacity = capacity

    def __str__(self):
        return self.room_number

class Subject:
    def __init__(self, name, n_lectures, n_workLectures, w_maxStud,
                 n_practicas, p_maxStud):

        self.name = name

        self.lectures = [Lecture("Lecture", i, "nvt") for i in range(int(n_lectures))]
        self.workLectures = [Lecture("WorkLecture", i, w_maxStud) for i in range(int(n_workLectures))]
        self.practicas = [Lecture("Practica", i, p_maxStud) for i in range(int(n_practicas))]

        self.students = []

    def __str__(self):
        return self.name

    def assignStudentsToLectures(self):
        if len(self.workLectures) and self.workLectures[0].maxStud:
            # Calculate number of groups and the number of students per lecture then round up
            nGroups = math.ceil(len(self.students) / self.workLectures[0].maxStud)
            wLectureSize = math.ceil(len(self.students) / nGroups)

            if nGroups > 1:
                newWorkLectures = []

                # For every work lecture, there are the same groups that need to be filled
                # But these groups also need to be created
                for wLecture in self.workLectures:
                    for groupNumber in range(nGroups):
                        nLecture = copy.copy(wLecture)
                        nLecture.group = groupNumber

                        nLecture.students = self.students[groupNumber*wLectureSize:(groupNumber+1)*wLectureSize]

                        newWorkLectures.append(nLecture)


                self.workLectures = newWorkLectures

            else:
                # Only one group, thus every student in the same group
                for wLecture in self.workLectures:
                    wLecture.students = self.students

        if len(self.practicas) and self.practicas[0].maxStud:
            # Calculate number of groups and the number of students per lecture then round up
            nGroups = math.ceil(len(self.students) / self.practicas[0].maxStud)
            pLectureSize = math.ceil(len(self.students) / nGroups)

            if nGroups > 1:
                newPracticaLectures = []

                # For every work lecture, there are the same groups that need to be filled
                # But these groups also need to be created
                for pLecture in self.practicas:
                    for groupNumber in range(nGroups):
                        nLecture = copy.copy(pLecture)
                        nLecture.group = groupNumber

                        nLecture.students = self.students[groupNumber*pLectureSize:(groupNumber+1)*pLectureSize]

                        newPracticaLectures.append(nLecture)

                    self.practicas = newPracticaLectures

            else:
                # Only one group, thus every student in the same group
                for pLecture in self.practicas:
                    pLecture.students = self.students


class Lecture:
    def __init__(self, name, lecture_number, maxStud):
        self.lecture_number = lecture_number
        self.name = name

        if maxStud == "nvt":
            self.maxStud = 0
        else:
            self.maxStud = int(maxStud)

        self.students = []
        self.group = 0

    def __str__(self):
        return "Name: %s Lecture number: %s Group: %s maxStud: %s" % (self.name, self.lecture_number, self.group, self.maxStud)

class Student:
    def __init__(self, surname, name, studentId, subject1, subject2,
                 subject3, subject4, subject5, subject_dct):

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

        self.__cleanUp()
        self.__fillInSubject(subject_dct)
        self.__addStudentToSubject()

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


print("Transforming data...")

# --------------
# Transform data:

classRooms = [ClassRoom(x[0], x[1]) for x in classRooms]

subjects = [Subject(x[0], x[1], x[2], x[3], x[4], x[5]) for x in subjects]
subject_dct = {x.__str__(): x for x in subjects}

students = [Student(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], subject_dct)
            for x in students]

# Assign students to lectures
for x in subjects:
    x.assignStudentsToLectures()
