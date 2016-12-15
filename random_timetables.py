from process_data import *

from random import randint, choice

def update_progress(workdone, text='Progress:'):
    print("\r{0} [{1:50s}] {2:.1f}%".format(text, '#' * int(workdone * 50),
    workdone*100), end="", flush=True)

    if workdone == 1:
        print('\n')

def random_timetables(im):
    while True:
        user_input = input("Please enter your desired amount of random lectures: ")
        nPlannedIterations = int(user_input)
        if nPlannedIterations <= 0:
            print("Pick a positive number for the amount of lectures...")
            continue
        else:
        	break

    while True:
        overlap_input = input("Can subjects be placed in the same timeslot? y/n: ")
        
        if overlap_input != "y" and overlap_input != "n":
        	print("Invalid input")
        	continue
        elif overlap_input == "y":
        	no_overlap = False
        	print("Overlap allowed.")
        	break
        elif overlap_input == "n":
   	    	no_overlap = True
   	    	print("No overlap allowed.")
   	    	break

    print("Starting random timetables with %s iterations..."
            % nPlannedIterations)

    while im.i != nPlannedIterations:
        changed_lectures = []

        for lecture in im.lectures:
            changed_lectures.append(
                im.randomLocation(lecture, no_overlap=no_overlap))

        im.addChanges(changed_lectures)

        # Makes all base since its all random anyways
        im.createBase()

        im.plot.addScore(im.iteration_dct[im.i]["score"])

        im.i += 1
        update_progress(im.i/nPlannedIterations)

        im.resetTimetables()

    best_iteration, score = im.compileBest()

    average = sum([im.iteration_dct[i]["score"]
                    for i in im.iteration_dct.keys()]) / nPlannedIterations

    print("Best iteration: %s, Best score: %s, Average Score: %s" %
                (best_iteration, round(score), round(average)))

    im.exportLectures("RT%si%sa%s" % (round(score),
        nPlannedIterations, round(average)))

    return im.lecture_dct

random_timetables(iteration_manager)
