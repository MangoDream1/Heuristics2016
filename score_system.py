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

		#print(total_subject_score, total_student_score, total_classroom_score, self.total_valid_score())

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
		subject_object.fillInTimetable()

		def pointsCalculator(nUniqueLectures):
			malus = 0

			if nUniqueLectures == 2:
				options = [[0, 3], [1, 4]]
			elif nUniqueLectures == 3:
				options = [[0, 2, 4]]
			elif nUniqueLectures == 4:
				options = [[0, 1, 3, 4]]
			elif nUniqueLectures == 5:
				options = [[0, 1, 2, 3, 4]]
			else:
				options = [[]]

			nSpreadTimetables = [0 for x in range(len(options))]
			nStudents = len(subject_object.students)

			for student in subject_object.students:
				nFullDays = 0

				for day, timeslot in student.timetable.items():
					isFullDay = False

					for lectures in timeslot.values():
						for lecture in lectures:
							if lecture.subject == subject_object:
								isFullDay = True

								for index, option in enumerate(options):
									if day in option:
										nSpreadTimetables[index] += 1

				if isFullDay:
					nFullDays += 1

				if nUniqueLectures - 1 == nFullDays:
					malus += 10 / nStudents
				elif nUniqueLectures - 2 == nFullDays:
					malus += 20 / nStudents
				elif nUniqueLectures - 3 == nFullDays:
					malus += 30 / nStudents

			bonus = 0

			if options[0]:
				bonus = 20 / nStudents * max(nSpreadTimetables) / len(options[0])

			return {"bonus": bonus, "malus": malus}


		if len(subject_object.getLectures()) > 0:
			nLectures = max([lecture.group for lecture in subject_object.getLectures()])
		else:
			nLectures = 0

		if len(subject_object.getWorkLectures()) > 0:
			nWorkLectureGroups = max([lecture.group for lecture in subject_object.getWorkLectures()])
		else:
			nWorkLectureGroups = 0

		if len(subject_object.getPracticas()) > 0:
			nPraticaGroups = max([lecture.group for lecture in subject_object.getPracticas()])
		else:
			nPraticaGroups = 0

		nUniqueLectures = len(subject_object.lectures) - nWorkLectureGroups - nPraticaGroups

		points = pointsCalculator(nUniqueLectures)

		subject_object.score = round(points["bonus"] - points["malus"])
