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

				for lecture in timeslot:
					if lecture.subject == subject_object:
						isFullDay = True

						for index, option in enumerate(options):
							if day in option:
								nSpreadTimetables[index] += 1

				if isFullDay:
					nFullDays += 1

			if nUniqueLectures - 1 == max(nFullDays):
				malus -= 10 / nStudents
			elif nUniqueLectures - 2 == max(nFullDays):
				malus -= 20 / nStudents
			elif nUniqueLectures - 3 == max(nFullDays):
				malus -= 30 / nStudents

		return {"bonus": 20 / nStudents * max(nSpreadTimetables), "malus": malus}


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

	subject_object.score = points["bonus"] - points["malus"]