from data_manager import *
from process_data import *


data_manager.importLectures(input("Timetable name: "))


print(data_manager.score_system.total_score())
data_manager.removeOverlap()
print(data_manager.score_system.total_score())
