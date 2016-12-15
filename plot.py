import matplotlib.pyplot as plt
from datetime import datetime
import os

class Plot:
    def __init__(self):
        self.score_lst = []
        self.time_lst = []

        if not os.path.exists("Timetable/Plots/"):
            os.makedirs("Timetable/Plots/")


    def addScore(self, score):
        self.score_lst.append(score)
        self.time_lst.append(datetime.now())

    def plotTime(self, name):

        self.convert_time()

        plt.plot(self.time_lst, self.score_lst)
        plt.ylabel("score")
        plt.xlabel("time")

        plt.savefig("Timetable/Plots/" + name + ".png")

    def plotHistogram(self, name):
        plt.hist(self.score_lst)
        plt.xlabel("score")

        plt.savefig("Timetable/Plots/" + name + ".png")

    def convert_time(self):
        self.score_lst = [mktime(datetime.strptime(i, "%Y-%m-%d %H:%M:%S.%f").timetuple()) for i in self.score_lst]
