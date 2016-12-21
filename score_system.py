from classes import *

class ScoreSystem:
	def __init__(self, data_manager):
		self.dm = data_manager

		self.score = None

	def __str__(self):
		return "Score: %s" % self.score

	def total_score(self):
		# Fill in the timetables, so that the score can be calculated
		for x in self.dm.students + self.dm.subjects + self.dm.classrooms:
			x.fillInTimetable()

		# Map creates iterable, thats why list is used sinds it
		# loops over the iter thus using the function
		list(map(self.student_score, self.dm.students))
		list(map(self.subject_score, self.dm.subjects))
		list(map(self.classroom_score, self.dm.classrooms))

		# Sum score
		total_student_score = sum([student.score for student in self.dm.students])
		total_subject_score = sum([subject.score for subject in self.dm.subjects])
		total_classroom_score = sum([classroom.score for classroom in self.dm.classrooms])

		# sum all scores
		self.score = total_subject_score + total_student_score + \
			   		 total_classroom_score + self.total_valid_score()

		return self.score

	def total_valid_score(self):
		# Checks if all lectures have a day, timeslot and classroom
		# if true 1000 points else 0

		valid = True

		for subject in self.dm.subjects:
			for lecture in subject.lectures:
				if lecture.classroom == None or \
				   lecture.day == None or \
				   lecture.timeslot == None:

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
				if lectures:
					classroom_score -= 100 * (len(lectures) - 1)

				# For every lecture after 17 hours minus points
				if key >= 4 and len(lectures) > 0:
					classroom_score -= 50

		classroom_object.score = classroom_score

	def student_score(self, student_object):
		student_score = 0

		# If a student has more than one lecture in the same timeslot subtract
		# one point per excess lecture
		for day, timeslot in student_object.timetable.items():
			for key, lectures in timeslot.items():

				if lectures:
					student_score -= (len(lectures) - 1)

		student_object.score = student_score

	def subject_score(self, subject_object):
		malus = 0
		bonus = 0

		workLectures = subject_object.getWorkLectures()

		# Find the number of workgroups
		if workLectures:
			nWorkLectureGroups = max([lecture.group for lecture in workLectures])
		else:
			nWorkLectureGroups = 0

		practicas = subject_object.getPracticas()

		# Find the number of practica groups
		if practicas:
			nPraticaGroups = max([lecture.group for lecture in practicas])
		else:
			nPraticaGroups = 0

		# The number of unique lectures are the amount of lectures minus
		# the groups
		nUniqueLectures = len(subject_object.lectures) - nWorkLectureGroups - \
							nPraticaGroups

		# The spread options differ for the nUniqueLectures
		if nUniqueLectures == 2:
			options = [[0, 3], [1, 4]]
		elif nUniqueLectures == 3:
			options = [[0, 2, 4]]
		elif nUniqueLectures == 4:
			options = [[0, 1, 3, 4]]
		else:
			options = [[]]

		nSpreadTimetables = [0 for x in range(len(options))]
		nStudents = len(subject_object.students)

		# For every student append the list of lectures
		# that have matching subject
		lecture_lst = []
		for student in subject_object.students:
			lecture_lst.append([l for l in student.lectures
								if l.subject == subject_object])

		for student_lst in lecture_lst:
			# If the lectures of the student match the options than add a point
			for option in options:
				if sorted([x.day for x in student_lst]) == option:
					nSpreadTimetables[0] += 1

			nFullDays = len(set([x.day for x in student_lst]))

			# Set malus to the correct number of points depending on nFullDays,
			# per student
			if nUniqueLectures - 1 == nFullDays:
				malus += 10 / nStudents
			elif nUniqueLectures - 2 == nFullDays:
				malus += 20 / nStudents
			elif nUniqueLectures - 3 == nFullDays:
				malus += 30 / nStudents

		# If there is an options set bonus to the highest counter (best spread)
		# And divide by the length
		if options[0]:
			#bonus = 20 / nStudents * max(nSpreadTimetables) / len(options[0])
			bonus = 20 / nStudents * max(nSpreadTimetables)

		# Subtract malus from bonus to get the subject score
		subject_object.score = bonus - malus
