from classes import *

class ScoreSystem:
	def __init__(self, iteration_manager):
		self.im = iteration_manager

		self.score = self.total_score()

	def __str__(self):
		return "Score: %s" % self.score

	def total_score(self):
		# Fill in the timetables, so that the score can be calculated
		for x in self.im.students + self.im.subjects + self.im.classrooms:
			x.fillInTimetable()

		# Map creates iterable, thats why list is used sinds it loops over the iter thus using the function
		list(map(self.student_score, self.im.students))
		list(map(self.subject_score, self.im.subjects))
		list(map(self.classroom_score, self.im.classrooms))

		total_student_score = sum([student.score for student in self.im.students])
		total_subject_score = sum([subject.score for subject in self.im.subjects])
		total_classroom_score = sum([classroom.score for classroom in self.im.classrooms])

		return total_subject_score + total_student_score + total_classroom_score + self.total_valid_score()

	def total_valid_score(self):
		valid = True

		for subject in self.im.subjects:
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

		for day, timeslot in classroom_object.timetable.items():
			for key, lectures in timeslot.items():
				# Count all the students in the room minus the capacity
				nTooManyStudents = sum([len(lecture.students)
					for lecture in lectures]) - classroom_object.capacity

				# If over capacity then subtract the points
				if nTooManyStudents > 0:
					classroom_score -= nTooManyStudents

				# Remove 100 points for every lecture if there are to many
				if len(lectures) > 1:
					classroom_score -= 100 * len(lectures)

				# For every lecture after 17 hours minus points
				if key >= 4 and len(lectures) > 0:
					classroom_score -= 50

		classroom_object.score = classroom_score

	def student_score(self, student_object):
		student_score = 0

		for day, timeslot in student_object.timetable.items():
			for key, lectures in timeslot.items():

				if len(lectures) > 1:
					student_score -= (len(lectures) - 1)

		student_object.score = student_score

	def subject_score(self, subject_object):
		malus = 0
		bonus = 0

		if len(subject_object.getLectures()) > 0:
			nLectures = max([lecture.group for lecture in
				subject_object.getLectures()])
		else:
			nLectures = 0

		if len(subject_object.getWorkLectures()) > 0:
			nWorkLectureGroups = max([lecture.group for lecture in
				subject_object.getWorkLectures()])
		else:
			nWorkLectureGroups = 0

		if len(subject_object.getPracticas()) > 0:
			nPraticaGroups = max([lecture.group for lecture in
				subject_object.getPracticas()])
		else:
			nPraticaGroups = 0


		nUniqueLectures = len(subject_object.lectures) - nWorkLectureGroups - \
							nPraticaGroups

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

		lecture_lst = []

		for student in subject_object.students:
			nFullDays = 0

			lecture_lst.append([l for l in student.lectures
								if l.subject == subject_object])

		for student_lst in lecture_lst:
			days_dct = {x: False for x in range(5)}

			for lecture in student_lst:
				days_dct[lecture.day] = True


				for index, option in enumerate(options):
					if lecture.day in option:
						nSpreadTimetables[index] += 1

			nFullDays = sum(days_dct.values())

			if nUniqueLectures - 1 == nFullDays:
				malus += 10 / nStudents
			elif nUniqueLectures - 2 == nFullDays:
				malus += 20 / nStudents
			elif nUniqueLectures - 3 == nFullDays:
				malus += 30 / nStudents

		if options[0]:
			bonus = 20 / nStudents * max(nSpreadTimetables) / len(options[0])

		subject_object.score = bonus - malus
