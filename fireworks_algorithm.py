from process_data import *
from iteration_manager import *
from random import randint, choice, random
from operator import itemgetter

import math
import sys

def calculate_sparks_amplitude_direction(firework_score, lowest_score, 
	highest_score, nFireworks, scores)
	
	# maxSparks is the total/max number of sparks
	max_sparks = 20

	# maxAmp is the maximum amplitude aka the maximum amount of changes made to a lecture
	max_aplitude = 20

	# Constants
	a = 0.1
	b = 10
	eps = sys.float_info.epsilon

	amplitude = max_aplitude * (firework_score - lowest_score + eps) \
		  			/ sum(score - lowest_score + eps for score in scores) 

	nSparks = max_sparks * (highest_score - firework_score + eps) \
				/ sum(highest_score - firework_score + eps for score in scores)


	if nSparks < (a * max_sparks):
		limitSparks = round(a * max_sparks)
	elif nSparks > (b * max_sparks):  #or a < b < 1: (dit ding snap ik ook gewoon niet)
		limitSparks = round(b * max_sparks)
	else:
		limitSparks = round(nSparks)
	

	return limitSparks, amplitude


def fireworks_algorithm(im, nFireworks):
    print("Starting firebase algorithm...")


    dimensenion = len(im.lectures) * (len(im.lectures) - 1)

	# get nFireworks lectures
	while im.i != nFireworks:
	    changed_lectures = []

	    for lecture in im.lectures:
            changed_lectures.append(
                im.randomLocation(lecture, no_overlap=no_overlap))

	        changed_lectures.append(lecture)

	    im.addChanges(changed_lectures)

	    # Makes all base since its all random anyways
	    im.createBase()

	    im.i += 1

	# put scores of Fireworks lectures in list??
	scores = sorted([(key, item["score"] / 1400)
					    for key, item in im.iteration_dct.items()],
					    key=itemgetter(1))


	# get lowest score
	lowest = scores[0][1]
	highest = scores[-1][1] # de laatste in de lijst dus
	

	if round(random()):
		pass

	directions = round(random() * dimensions)


	# for every lecture
	for key, score in scores:
		






		lSparksAmp = calculate_sparks_amplitude_direction(dimensions, score + 6461, lowest + 6461, highest + 6461, nFireworks)
		
		nSparks = lSparksAmp[0]
		explosionAmp = lSparksAmp[1]

		subjects = len(im)
		dimensions = 0

		for spark in range(0, nSparks):
			dimensions = subjects * (subjects - 1)
			subjects -= 1

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

		


