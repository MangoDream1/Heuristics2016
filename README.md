# Heuristics2016: Lectures & Lesroosters

The algorithms will try to find the best possible timetable for the given data.
The following algorithms are included: *random_timetables, hill_climber,
swap_hill_climber, simulated_annealing* and *genetic_algorithm*. An optimization
algorithm has also been written called *student_optimization*.

A script has been written called ```run4.py``` that uses multiprocessing to run multiple swap_hill_climber or student_optimization instances. This is a major speedup since Python normally only uses 1 processor core. How to operate it can also be found in the Documentation below. The script ```timing.py``` is also loaded into every algorithm and will measure the time spend on the algorithm.

The score system score the timetable. The score system is build on the specifications
of the brief (http://heuristieken.nl/wiki/index.php?title=Lectures_%26_Lesroosters)
The maximum score is 1400 and our best algorithm has reached **MAXSCORE HIER**
and is **BESTE ALGORITHME HIER**.


Every algorithm will create a Lecture json, a Score json and a plot. The lecture
json contains all the data of the timetable and is a lecture package, the score
json contains the scores for every object in the timetable and the plot show the progression of the score versus the time (except for random timetables then a histogram is shown). These files can be found in the timetable folder under Lectures, Scores and Plots.

To view the created lecture package run ```python3 webview.py``` and navigate to
http://127.0.0.1:5000/. The python module Flask is needed for this. In the
webview select the lecture package you want to view from the first drop down menu
and then use the other drop downs to see the timetables of classrooms, subjects
or students. A screenshot of the webview is attached at the bottom of this
README with explanation. When selecting a lecture package a json file is created for every timetable (classes, students and subjects) that can be found under the Timetable folder. These jsons are read by the webviews javascript.



The name of these files will be explained in the Documentation below. If the
same score is reached by the same algorithm then behind the name is added
n{number}; number being the number of results with the same score.

---

#### Documentation:

###### Random timetables:

```python3 random_timetables.py```

```
Options:
  -h, --help            show this help message and exit
  -i NPLANNEDITERATIONS, --iterations=NPLANNEDITERATIONS
                           The number of timetables created
  -o NO_OVERLAP, --no_overlap=NO_OVERLAP
                           Removal of overlap for every random timetable.
```

For example: ```python3 random_timetables.py -i 10000 -o```: 10000 random
timetables where overlap will not be removed

Random timetables are named as follows:
**RT{score}i{nPlannedIterations}a{average score}**

---

###### Hill climber:

```python3 hill_climber.py```

```
Options:
  -h, --help            show this help message and exit
  -n NOPROGRESSLIMIT, --noProgressLimit=NOPROGRESSLIMIT
                        The number of times the algorithm is allowed not to progress
  -l, --loadFromOld     start from old timetable
  -c CLASSROOMWEIGTH, --classroomWeigth=CLASSROOMWEIGTH
                        The weight that is given to classrooms in random
                        changes
  -t TIMESLOTWEIGTH, --timeslotWeigth=TIMESLOTWEIGTH
                        The weight that is given to timeslots in random
                        changes
  -d DAYWEIGTH, --dayWeigth=DAYWEIGTH
                        The weight that is given to days in random changes
```

For example: ```python3 hill_climber.py -r -l -c 2 - t 0 -d 10```: hill climber
which will start from user input old lecture package and has weight 2 for classrooms,
0 for timeslots and 10 for days

Hill climber are named as follows:
**HC{score}nPl{no progress limit}c{weight classroom}t{weight timeslot}d{weight day}**

---

###### Swap Hill climber:

```python3 swap_hill_climber.py```

```
Options:
  -h, --help            show this help message and exit
  -l, --loadFromOld     start from old timetable
  -n NOPROGRESSLIMIT, --noProgressLimit=NOPROGRESSLIMIT
                        The number of times the algorithm is allowed not to progress
```

For example: ```python3 swap_hill_climber.py -n 10```: swap_hill_climber that
stops when it has not progressed 10 times

Swap hill climber are named as follows:
**SHC{score}nPl{no progress limit}**

---

###### Simulated annealing:

```python3 simulated_annealing.py```

```
Options:
-h, --help            show this help message and exit
-l, --loadFromOld     start from old timetable
-t TEMP, --startTemp=TEMP
                      define the default temp
```

For example: ```python3 simulated_annealing.py -t 10000```: simulated_annealing
with start temp of 10000

Simulated Annealing is named as follows:
**SSA{score}Tmax{Max temp}**

---

###### Genetic Algorithm:

```python3 genetic_algorithm.py```

```
Options:
  -h, --help            show this help message and exit
  -p NPOPULATION, --nPopulation=NPOPULATION
                        The total population, default is 100
  -g NGENERATIONS, --nGenerations=NGENERATIONS
                        The number of generations, default is 100
  -m MUTATION_RATE, --mutation_rate=MUTATION_RATE
                        The mutation rate, between 0 and 1 default is 0.05
  -b, --load_best       Load in the best timetables instead of starting random
  -o, --remove_overlap  Remove overlap in the created children, default is
                        True
```

For example: ```python3 genetic_algorithm.py -b```: genetic_algorithm with
the best 100 from the Timetable/Lectures folder for 100 generations

Genetic Algorithm is named as follows:
**GA{score}p{population}g{generations}m{mutation rate}b{loaded from best True or False}**

---

###### Student Optimization:

```python3 student_optimization.py```

```
Options:
  -h, --help            show this help message and exit
  -n NOPROGRESSLIMIT, --noProgressLimit=NOPROGRESSLIMIT
                        The number of times the algorithm is allowed not to
                        progress
```

For example: ```python3 student_optimization.py -n 10000```: student_optimization
that will keep going until it does not progress for 10000 iterations

---

##### Run4 (4 processor cores are needed for this)

```python3 run4.py```

```
Options:
  -h, --help            show this help message and exit
  -i NITERATIONS, --nIterations=NITERATIONS
                        The number of timetables that need to be created or
                        improved
  -n NOPROGRESSLIMIT, --noProgressLimit=NOPROGRESSLIMIT
                        The number of times the algorithm is allowed not to
                        progress
  -p, --improve         Improves timetables instead of creating new ones
  -s, --student_optimization
                        Use student_optimization if improve is also used
                        instead of swap_hill_climber

```
For example: ```python3 run4.py -p -s -i 10000 -n 1000```: will improve 10000 previously created lecture packages using student_optimization with an no progress limit of 1000  

Run4 does not use a special name but the name for swap_hill_climber if swap_hill_climber is used otherwise will use student_optimization name


---


Webview screenshot:

In this screenshot the timetable of classroom A1.04 is pictured. Beneath the timetable all the information of the classroom is pictured. Inside each cell in the timetable there is a lecture. Shown is the name of the subject, the classroom and the lecture string. The first letter in the lecture string represents the type of lecture (Lecture, WorkLecture or Practica). The following number represents the what lecture it is, for example a subject can have 2 work lectures then the first would have a 0 here and the second a 1. The next letter is the group and the last numbers represent the amount of students in this lecture.

Not shown here when there is overlap, meaning multiple lectures in the same slot, then the slot would be red with a big number representing the amount of lectures in the slot. Also below in the information these lectures would be colored red.

![](https://raw.githubusercontent.com/MangoDream1/Heuristics2016/master/screenshots/webview_example.png "screenshot webview")
