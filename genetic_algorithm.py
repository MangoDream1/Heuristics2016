from process_data import *
from iteration_manager import *
from random import randint, choice, random
from operator import itemgetter

def update_progress(workdone, text='Progress:'):
    print("\r{0} [{1:50s}] {2:.1f}%".format(text, '#' * int(workdone * 50),
    workdone*100), end="", flush=True)

    if workdone == 1:
        print('\n')

def genetic_algorithm(im, nPopulation, nGenerations, mutation_rate):
    print("Starting genetic algorithm...")

    nLectures = len(im.lectures)

    # Start with random timetables
    while im.i != nPopulation:
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
        update_progress(im.i/nPopulation, text="Random timetables:")

    cGeneration = 0

    while nGenerations != cGeneration:
        scores = sorted([(key, item["score"] / 1440)
                            for key, item in im.iteration_dct.items()],
                            key=itemgetter(1))

        # Delete lowest items
        for key, score in scores[:(nPopulation // 5)]:
            del im.iteration_dct[key]

        # Calculate number of parents
        parents = []
        nParents = nPopulation // 5 * 2

        # Save deleted keys for reuse, then delete from scores
        deleted_keys = [x[0] for x in scores[:(nPopulation // 5)]]
        del scores[:(nPopulation // 5)]

        # Parent selection
        while len(parents) != nParents:
            key, score = choice(scores)

            if score > random():
                parents.append(key)

                # Mutate
                if random() > mutation_rate:
                    dct = im.iteration_dct[key]

                    random_lecture = dct[choice(range(nLectures))]

                    # Change classroom, timeslot and day of random lecture
                    random_lecture["day"] = randint(0, 4)
                    random_lecture["timeslot"] = randint(0, 3)
                    random_lecture["classroom"] = choice(im.classrooms).getId()

        # Reproduce
        while parents:
            father = parents.pop()
            mother = parents.pop()

            intersect = int(random() * nLectures)

            father_lectures = [im.iteration_dct[father][x]
                                for x in range(0, intersect)]

            mother_lectures = [im.iteration_dct[mother][x]
                                for x in range(intersect, nLectures)]

            # Has to be numbered dict so that iteration_manager can read it
            child_lectures = {i: x for i, x in
                                enumerate(father_lectures + mother_lectures)}

            im.applyChanges(child_lectures)

            im.i = deleted_keys.pop()
            im.addChanges(im.lectures)

        cGeneration += 1
        update_progress(cGeneration/nGenerations, text="Genetic Algorithm:")

    best_iteration = max([(i, im.iteration_dct[i]["score"])
                            for i in im.iteration_dct.keys()],
                            key=itemgetter(1))

    print("Best iteration: %s, Score: %s" % (best_iteration[0],
                                             best_iteration[1]))

    compiled_changes = im.compileChanges(best_iteration[0])
    im.applyChanges(compiled_changes)

    im.exportLectures("GA%sp%sg%sm%s" % (best_iteration[1], nPopulation,
                                         nGenerations, mutation_rate))

    return im.lecture_dct

genetic_algorithm(iteration_manager, 100, 1000, 0.05)
