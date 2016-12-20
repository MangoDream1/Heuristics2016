from process_data import *


data_manager.importLectures("STUDENT_OPTIMIZED1331nPl100000")


print(data_manager.iteration_dct[0]["score"])
print()

x = data_manager.subject_dct["Databases 2"]
y = data_manager.score_system

y.subject_score(x)

print(x.score)
