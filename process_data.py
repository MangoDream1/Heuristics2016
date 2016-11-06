
# coding: utf-8

# --------------
# Get Data:

from classes import *

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


print("Transforming data...")

# --------------
# Transform data:

classRooms = [ClassRoom(x[0], x[1]) for x in classRooms]
classRoom_dct = {x.room_number: x for x in classRooms}

subjects = [Subject(x[0], x[1], x[2], x[3], x[4], x[5]) for x in subjects]
subject_dct = {x.__str__(): x for x in subjects}

students = [Student(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], subject_dct)
            for x in students]
student_dct = {x.studentId: x for x in students}

# Assign students to lectures
for x in subjects:
    x.assignStudentsToLectures()
