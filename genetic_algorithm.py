from process_data import *
from random import randint, choice, random

from optparse import OptionParser
import re


def update_progress(workdone, text='Progress:'):
    """ Print the progress bar """

    print("\r{0} [{1:50s}] {2:.1f}%".format(text, '#' * int(workdone * 50),
        workdone*100), end="", flush=True)

    if workdone == 1:
        print('\n')


def genetic_algorithm(dm, nPopulation, nGenerations, mutation_rate,
        load_best=False, remove_overlap=True):
    """ Create nPopulation random timetables or that many of the best lecuture
        packages. Then delete the lowest 20% and select 40% number of parents.
        Selection is based on the fitness (score in comparison with max score).
        Let these parents procreate with a mutation_rate that changes a lecture
        in the parents. Then continue this process until the nGenerations is
        reached
    """

    print("Starting genetic algorithm...")

    nLectures = len(dm.lectures)

    if load_best:
        # Dict with file name as key and ints as value
        ints = {x: list(map(int, re.findall(r"\d+", x)))
                    for x in os.listdir("Timetable/Lectures")}

        # Tuple (score, timetable file name) if not same noProgressLimit
        # to prevent same timetables from being improved
        timetables = [(ints[x][0], x)
            for x in os.listdir("Timetable/Lectures")]

        best_scores = sorted(timetables,
            key=itemgetter(0), reverse=True)[:nPopulation]

        best_timetables = list(map(lambda x: x[1], best_scores))

        if len(best_timetables) < nPopulation:
            print("Not enough timetables in folder thus cannot continue")
            return False

    # Create as many timetables until population is filled (count starts at 0)
    while dm.i != (nPopulation - 1):
        if not load_best:
            # Start with random timetables without overlap
            changed_lectures = []

            for lecture in dm.lectures:
                changed_lectures.append(
                    dm.randomLocation(lecture, no_overlap=True))

            dm.addChanges(changed_lectures)

            # Makes all base since its all random
            dm.createBase()

            dm.resetTimetables()

            dm.i += 1
            update_progress(dm.i/(nPopulation-1), text="Random timetables:")

        else:
            # Import best lecture
            dm.importLectures(best_timetables.pop())
            update_progress(dm.i/nPopulation, text="Loading best:")

    cGeneration = 0

    best_score = max(item["score"] for item in dm.iteration_dct.values())

    # Export current best score, will be overwritten by better ones
    dm.exportLectures("GA%sp%sg%sm%sb%s" % (round(best_score), nPopulation,
        nGenerations, mutation_rate, load_best))

    while nGenerations != cGeneration:
        scores = sorted([(key, item["score"] / 1400)
                            for key, item in dm.iteration_dct.items()],
                            key=itemgetter(1))

        # Delete lowest items
        for key, score in scores[:(nPopulation // 5)]:
            del dm.iteration_dct[key]

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
                    dct = dm.iteration_dct[key]

                    random_lecture = dct[choice(range(nLectures))]

                    # Change classroom, timeslot and day of random lecture
                    random_lecture["day"] = randint(0, 4)
                    random_lecture["timeslot"] = randint(0, 3)
                    random_lecture["classroom"] = choice(dm.classrooms).getId()

        # Reproduce
        while parents:
            father = parents.pop()
            mother = parents.pop()

            # The dividing point until where fathers DNA will be used,
            # from there its all mama
            divide = int(random() * nLectures)

            father_lectures = [dm.iteration_dct[father][x]
                                for x in range(0, divide)]

            mother_lectures = [dm.iteration_dct[mother][x]
                                for x in range(divide, nLectures)]

            # Has to be numbered dict so that data_manager can read it
            child_lectures = {i: x for i, x in
                                enumerate(father_lectures + mother_lectures)}

            # Apply the changes
            dm.applyChanges(child_lectures)

            # Set i to an previous used spot to overwrite
            dm.i = deleted_keys.pop()

            # Remove overlap in child if used
            if remove_overlap:
                dm.removeOverlap()

            # Add the changes
            dm.addChanges(dm.lectures)

            score = dm.iteration_dct[dm.i]["score"]

            # If score is better then old delete old files and write new
            # ones
            if score > best_score:
                old_name = "GA%sp%sg%sm%sb%s" % (round(best_score),
                    nPopulation, nGenerations, mutation_rate, load_best)

                os.remove("Timetable/Lectures/" + old_name + ".json")
                os.remove("Timetable/Scores/" + old_name + ".json")
                os.remove("Timetable/Plots/" + old_name + ".png")

                best_score = score
                dm.exportLectures("GA%sp%sg%sm%sb%s" % (round(best_score),
                    nPopulation, nGenerations, mutation_rate, load_best))


        average_score = sum(value["score"]
            for value in dm.iteration_dct.values()) / len(dm.iteration_dct)

        # Plot average score since best might stay the same for long
        dm.plot.addScore(average_score)

        cGeneration += 1
        update_progress(cGeneration/nGenerations, text="Genetic Algorithm:")

    dm.plot.plotTime("GA%sp%sg%sm%sb%s" % (round(best_score),
        nPopulation, nGenerations, mutation_rate, load_best))

    print("Score: %s" % (round(best_score)))

    return dm.lecture_dct

if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-p", "--nPopulation", dest="nPopulation",
    default=100, help="The total population, default is 100")

    parser.add_option("-g", "--nGenerations", dest="nGenerations",
        default=100, help="The number of generations, default is 100")

    parser.add_option("-m", "--mutation_rate", dest="mutation_rate",
        default=0.05,
        help="The mutation rate, between 0 and 1 default is 0.05")

    parser.add_option("-b", "--load_best", dest="load_best",
        default=False, action="store_true",
        help="Load in the best timetables instead of starting random")

    parser.add_option("-o", "--keep_overlap", dest="overlap",
        default=True, action="store_false",
        help="Keep overlap in the created children, default is False")

    (options, args) = parser.parse_args()

    genetic_algorithm(data_manager, int(options.nPopulation),
        int(options.nGenerations), float(options.mutation_rate),
        load_best=options.load_best, remove_overlap=options.overlap)
