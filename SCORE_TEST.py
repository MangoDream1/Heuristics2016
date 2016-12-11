from iteration_manager import *
from process_data import *


iteration_manager.importLectures(input("Timetable name: "))


print(iteration_manager.score_system.total_score())
iteration_manager.exportLectures("TEST1")
iteration_manager.removeOverlap()
print(iteration_manager.score_system.total_score())
