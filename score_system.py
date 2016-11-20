from classes import *

class ScoreSystem:
	def __init__(self, subject_lst, student_lst, classroom_lst):
		self.subject_lst = subject_lst
		self.student_lst = student_lst
		self.classroom_lst = classroom_lst

		self.score = self.total_score()

	def __str__(self):
		return "Score: %s" % self.score

	def total_score(self):

		# Map creates iterable, thats why list is used sinds it loops over the iter thus using the function
		list(map(self.subject_score, self.subject_lst))
		list(map(self.student_score, self.student_lst))
		list(map(self.classroom_score, self.classroom_lst))

		total_subject_score = sum([subject.score for subject in self.subject_lst])
		total_student_score = sum([student.score for student in self.student_lst])
		total_classroom_score = sum([classroom.score for classroom in self.classroom_lst])

		return total_subject_score + total_student_score + total_classroom_score + self.total_valid_score()

	def total_valid_score(self):
		valid = True

		for subject in self.subject_lst:

			for lecture in subject.lectures:
				if lecture.classroom == None or lecture.day == None or lecture.timeslot == None:
					valid = False
					break

			if not valid:
				break

		if valid:
			return 1000
		else:
			return 0

	def classroom_score(self, classroom_object):
		classroom_score = 0

		classroom_object.fillInTimetable()

		for day, timeslot in classroom_object.timetable.items():
			for key, lectures in timeslot.items():

				if len(lectures) > 1:

					nToManyStudents = sum([len(lecture.students) for lecture in lectures]) - classroom_object.capacity

					if nToManyStudents > 0:
						classroom_score -= nToManyStudents

				# For every lecture after 17 hours minus points
				if key >= 4 and len(lecture) > 0:
					classroom_score -= 50

		classroom_object.score = classroom_score

	def student_score(self, student_object):
		student_score = 0

		student_object.fillInTimetable()

		for day, timeslot in student_object.timetable.items():
			for key, lectures in timeslot.items():

				if len(lectures) > 1:
					student_score -= (len(lectures) - 1)

		student_object.score = student_score

	def subject_score(self, subject_object):
		subject_score = 0

		subject_object.fillInTimetable()

		if len(subject_object.getWorkLectures()) > 0:
			nWorkLectureGroups = max([lecture.group for lecture in subject_object.getWorkLectures()])
		else:
			nWorkLectureGroups = 0

		if len(subject_object.getPracticas()) > 0:
			nPraticaGroups = max([lecture.group for lecture in subject_object.getPracticas()])
		else:
			nPraticaGroups = 0

		nUniqueLectures = len(subject_object.lectures) - nWorkLectureGroups - nPraticaGroups

		empty_day = {y: [] for y in range(NUMBER_OF_SLOTS)}

		if nUniqueLectures == 2:
			if subject_object.timetable[0] != empty_day and subject_object.timetable[3] != empty_day:
				subject_score += 20
			elif subject_object.timetable[1] != empty_day and subject_object.timetable[4] != empty_day:
				subject_score += 20

		elif nUniqueLectures == 3:
			if subject_object.timetable[0] != empty_day and subject_object.timetable[2] != empty_day and \
			   subject_object.timetable[4] != empty_day:
				subject_score += 20

		elif nUniqueLectures == 4:
			if subject_object.timetable[0] != empty_day and subject_object.timetable[1] != empty_day and \
			   subject_object.timetable[3] != empty_day and subject_object.timetable[4] != empty_day:
				subject_score += 20

		nFullDays = 0

		for day, timeslot in subject_object.timetable.items():
			if timeslot != empty_day:
				nFullDays += 1

		# Voor ieder vak van x activiteiten geldt dat ze 10 maluspunten opleveren
		# als ze op x-1 dagen geroosterd zijn, 20 voor x-2 en 30 voor x-3.

		if nUniqueLectures - 1 == nFullDays:
			subject_score -= 10
		elif nUniqueLectures - 2 == nFullDays:
			subject_score -= 20
		elif nUniqueLectures - 3 == nFullDays:
			subject_score -= 30

		subject_object.score = subject_score
