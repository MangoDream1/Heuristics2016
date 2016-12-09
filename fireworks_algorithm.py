from process_data import *
from iteration_manager import *
from random import randint, choice, random
from operator import itemgetter

import math
import sys

def calculate_sparks_amplitude_direction(firework_score, lowest_score, highest_score, nFireworks)
	
	lSparksAmp = []

	#constants (hier heb ik gewoon wat ingevuld omdat ik geen idee heb wat dit moet zijn nu)
	# m is the total/max number of sparks (heet nu ook maxSparks) (dus nu max 20 sparks, nooit meer), a & b are constant??
	maxSparks = 20
	a = 0.1
	b = 10
	eps = sys.float_info.epsilon

	nSparks = maxSparks * (((lowest_score - firework_score) + eps) / (nFireworks * ((lowest_score - firework_score) + eps)))

	if nSparks < (a * tSparks):
		limitSparks = round(a * maxSparks)
	elif nSparks > (b * m):  #or a < b < 1: (dit ding snap ik ook gewoon niet)
		limitSparks = round(b * maxSparks)
	else:
		limitSparks = round(maxSparks)

	lSparksAmp.add(limitSparks)
	

	# maxAmp is the maximum amplitude aka the maximum amount of changes made to a lecture
	maxAmp = 20

	explosionAmp = maxAmp * (((best_score - firework_score) + eps) / (nFireworks * ((best_score - firework_score) + eps)))

	

	return lSparksAmp

	



def fireworks_algorithm(im, nFireworks):
    print("Starting firebase algorithm...")

	# get nFireworks lectures
	while im.i != nFireworks:
	    changed_lectures = []

	    for lecture in im.lectures:
	        lecture.day = randint(0, 4)
	        lecture.timeslot = randint(0, 3)
	        lecture.classroom = choice(classrooms)

	        changed_lectures.append(lecture)

	    im.addChanges(changed_lectures)

	    # Makes all base since its all random anyways
	    im.createBase()

	    im.i += 1

	# put scores of Fireworks lectures in list??
	scores = sorted([(key, item["score"] / 1440)
	                            for key, item in im.iteration_dct.items()],
	                            key=itemgetter(1))

	# get lowest score
	lowest = key, score in scores[0]
	highest = key, score in scores[nFireworks - 1] # de laatste in de lijst dus
	

	# for every lecture
	for key, score in scores

		#key, score = score??
		
		lSparksAmp = calculate_sparks_amplitude_direction(dimensions, score + 6461, lowest + 6461, highest + 6461, nFireworks)
		
		nSparks = lSparksAmp[0]
		explosionAmp = lSparksAmp[1]

		subjects = len(im)
		dimensions = 0

		for spark in range(0, nSparks):
			dimensions = subjects * (subjects - 1)
			subjects -= 1

		dimensions = (len(im) * len(im - 1))

		# randomly choose z dimensenion of sparks location (directions is z)
		directions = round(dimensions * rand(0, 1))

		#Calculate the displacement: h = Ai · rand(−1, 1);
		displacement = explosionAmp * rand(-1, 1)

		min_dimension = score - 232
		max_dimension = score + 40


		for dimension in dimensions:
			if dimension in directions:
				dimension = dimension + displacement

				if dimension < min_dimension or dimension > max_dimension:
					dimension = (min_dimension + dimension) % (max_dimension - min_dimension)

		


