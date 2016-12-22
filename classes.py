from copy import copy
import math
import json
import os

print("Creating classes...")

# Global variables

NUMBER_OF_SLOTS = 4
NUMBER_OF_DAYS = 5
TIMESLOTS = {0: "9-11", 1: "11-13", 2: "13-15", 3: "15-17", 4: "17-19"}
DAYS = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
        4: "Friday", 5: "Saturday", 6: "Sunday"}

# --------------
# Classes:

class Lecture:
    ''' A lecture is the object that is put in a slot in a timetable.
        Lectures are the objects that are changed by the algorithms '''

    def __init__(self, name, lecture_number, subject, maxStud):
        self.subject = subject
        self.lecture_number = lecture_number
        self.name = name
        self.group = 0
        self.classroom = None

        self.siblings = [] # siblings are same lectures but different groups

        if maxStud == "nvt":
            self.maxStud = 0
        else:
            self.maxStud = int(maxStud)

        self.students = []

        # Default timetable settings
        self.day = 0
        self.timeslot = 0


    def __str__(self):
        # Concise format for all information.
        # First letter of name to tell the type of lecture,
        # the lecture number to know what lecture this is, the group letter to
        # know what group and finally the amount of students.
        return self.name[0] + str(self.lecture_number) + \
            chr(ord('A') + self.group) + str(len(self.students))


    def assignLecturetoAll(self):
        self.assignLectureToStudents()
        self.assignLecturetoClassroom()
        self.assignLecturetoSubject()


    def assignLectureToStudents(self):
        # Adds self to all lecture students
        for student in self.students:
            if self not in student.lectures:
                student.lectures.append(self)


    def assignLecturetoClassroom(self):
        # Adds self to lecture classroom
        if self not in self.classroom.lectures:
            self.classroom.lectures.append(self)


    def assignLecturetoSubject(self):
        # Adds self to the lecture subject
        if self not in self.subject.lectures:
            self.subject.lectures.append(self)


    def getChangingDataDict(self):
        # This is the data of the lecture object that changes during algorithm iterations
        return {"day": self.day, "timeslot": self.timeslot,
                "classroom": self.classroom.getId()}


    def classroomOverlap(self):
        # Returns true if there is another lecture in the same timeslot
        if len(self.classroom.timetable[self.day][self.timeslot]) > 1:
            return True
        else:
            return False


    def toDict(self):
        # The most condenced form of the data in this object in dict form
        return {"subject": self.subject.name,
                "classroom": self.classroom.__str__(),
                "string": self.__str__()}


    def toLongDict(self):
        # The data in this object in dict form
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
    ''' Timetable class is parent of all classes that have a timetable.
        The creation of a timetable and the assigning of lectures to the
        timetable happens here. '''


    def __init__(self):
        # Empty timetable with number of days and the number of slots
        self.timetable = {x: {y: [] for y in range(NUMBER_OF_SLOTS)}
            for x in range(NUMBER_OF_DAYS)}
        self.jsonDict = {x: {y: [] for y in range(NUMBER_OF_SLOTS)}
            for x in range(NUMBER_OF_DAYS)}

        self.score = 0


    def clearLectures(self):
        self.lectures = []


    def clearTimetable(self):
        self.timetable = {x: {y: [] for y in range(NUMBER_OF_SLOTS)}
            for x in range(NUMBER_OF_DAYS)}


    def getLectures(self):
        return [x for x in self.lectures if x.name == "Lecture"]


    def getWorkLectures(self):
        return [x for x in self.lectures if x.name == "WorkLecture"]


    def getPracticas(self):
        return [x for x in self.lectures if x.name == "Practica"]


    def exportTimetable(self):
        # Export the timetable to json file, so that it can be read by webview

        self.fillInTimetable()

        # Reset jsonDict
        self.jsonDict = {x: {y: [] for y in range(NUMBER_OF_SLOTS)}
            for x in range(NUMBER_OF_DAYS)}

        # Fill the jsonDict with list of dicts on the same location
        # as in timetable. The lecture object is not used since it contains
        # data not needed for visualisation
        for x in self.timetable.keys():
            for y in self.timetable[x].keys():
                lectures = [lecture.toDict() for lecture
                    in self.timetable[x][y]]

                self.jsonDict[x][y] = lectures

        if not os.path.exists("Timetable/%s" % self.__class__.__name__):
            os.makedirs("Timetable/%s" % self.__class__.__name__)

        # Create the json file
        with open("Timetable/%s/%s.json" %
            (self.__class__.__name__, self.getId()), 'w') as f:
            json.dump(self.jsonDict, f, indent=3)


    def fillInTimetable(self):
        self.clearTimetable()

        # For all lectures append to correct location in timetable dict
        for lecture in self.lectures:
            self.timetable[lecture.day][lecture.timeslot].append(lecture)


class Classroom(Timetable):
    ''' Classroom object inherits from Timetable
        containing data specific for classrooms '''

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
    ''' Subject class inherits from Timetable containing data specific for
        subjects. Also creates the lecture objects, creates the different
        groups for the work and pratica lectures and also spreads the students
        over these groups'''

    def __init__(self, name, n_lectures, n_workLectures, w_maxStud,
                 n_practicas, p_maxStud):
        super().__init__()

        self.name = name

        # Create all the lectures of this subject and append to list
        self.lectures = [Lecture("Lecture", i, self, "nvt")
                            for i in range(int(n_lectures))] + \
                        [Lecture("WorkLecture", i, self, w_maxStud)
                            for i in range(int(n_workLectures))] + \
                        [Lecture("Practica", i, self, p_maxStud)
                            for i in range(int(n_practicas))]

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
                    # Calculate number of groups and the number of students
                    # per lecture then round up
                    nGroups = math.ceil(len(self.students) / lecture.maxStud)
                    lectureSize = math.ceil(len(self.students) / nGroups)

                    if nGroups > 1:
                        # For every work lecture, there are the same groups
                        # that need to be filled. But these groups
                        # also need to be created
                        for groupNumber in range(nGroups):
                            nLecture = copy(lecture)
                            nLecture.group = groupNumber

                            nLecture.students = self.students[groupNumber*\
                                lectureSize:(groupNumber+1)*lectureSize]

                            nLecture.assignLectureToStudents()
                            newLectures.append(nLecture)
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
            self.createSiblings()

    def createSiblings(self):
        # Same functionality has to be repeted for practicas and worklectures
        # thus in a seperate function
        def main(lecture_list):
            lectureGroupsDct = {}

            if lecture_list:
                nUniqueLectures = max(x.lecture_number
                    for x in lecture_list) + 1

                if nUniqueLectures:
                    for u in range(nUniqueLectures):
                        lectureGroupsDct[u] = []

                        for l in lecture_list:
                            if l.lecture_number == u:
                                lectureGroupsDct[u].append(l)

                    for l in lecture_list:
                        # Copy needed because every above created sibling lists
                        # use same pointer thus removing from one removed from
                        # all
                        l.siblings = copy(lectureGroupsDct[l.lecture_number])

                    # Remove self from sibling list
                    for l in lecture_list:
                        if l in l.siblings:
                            l.siblings.remove(l)

        # Create siblings for work and practicas.
        # Normal lectures dont have groups thus not needed
        main(self.getWorkLectures())
        main(self.getPracticas())

class Student(Timetable):
    ''' Student class inherits from Timetable containing data specific for
        students. Also assigns the student to all its subjects'''

    def __init__(self, surname, name, studentId, *subjects):

        super().__init__()

        self.surname = surname
        self.name = name
        self.studentId = studentId

        # The names of the subjects of the student
        self.__subjectNames = []

        # Add subject names to __subjectNames
        for s in subjects:
            self.__addSubject(s)

        self.subjects = []
        self.lectures = []


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


    def assignSubjectToStudent(self, subject_dct):
        # Find the subject name in subject_dct and add the subject object to
        # subject list

        for subjectName in self.__subjectNames:
            self.subjects.append(subject_dct[subjectName])

        self.__addStudentToSubject()
