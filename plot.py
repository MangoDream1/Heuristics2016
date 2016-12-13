import matplotlib.pyplot as plt
from datetime import datetime

class Plot:
    def __init__(self):
        self.score_lst = []
        self.time_lst = []

    def addScore(self, score):
        self.score_lst.append(score)
        self.time_lst.append(datetime.now())

    def plotTime(self):
        plt.plot(self.time_lst, self.score_lst)
        plt.ylabel("score")
        plt.xlabel("time")
        plt.show()

    def plotHistogram(self):
        plt.hist(self.score_lst)
        plt.xlabel("score")
        plt.show()
