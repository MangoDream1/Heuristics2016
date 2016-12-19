import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import os
import matplotlib

import time

class Plot:
    ''' Plot class handles all the plotting of the different algorithms '''

    def __init__(self):
        self.score_lst = []
        self.time_lst = []
        self.start = time.time()

        if not os.path.exists("Timetable/Plots/"):
            os.makedirs("Timetable/Plots/")


    def addScore(self, score):
        # Add score and the timestamp since start
        self.score_lst.append(score)
        self.time_lst.append(time.time() - self.start)

    def plotTime(self, name):
        plt.plot(self.time_lst, self.score_lst)

        plt.title(name)
        plt.ylabel("score")
        plt.xlabel("time (seconds)")

        plt.savefig("Timetable/Plots/" + name + ".png")

    def plotHistogram(self, name):
        plt.hist(self.score_lst)

        plt.title(name)
        plt.xlabel("score")

        plt.savefig("Timetable/Plots/" + name + ".png")
