# import all the data from process_data
from process_data import *

i=0

print(subjects[i])
print("\n".join([x.__str__() for x in subjects[i].getPractica()]))
print([(x.group, len([y.__str__() for y in x.students]), [y.__str__() for y in x.students]) for x in subjects[i].getPractica()])

# Laat alle werkgroepen zien van vak i

print(subjects[i])
print("\n".join([x.__str__() for x in subjects[i].getWorkLectures()]))
print([(x.group, len([y.__str__() for y in x.students]), [y.__str__() for y in x.students]) for x in subjects[i].getWorkLectures()])


# Laat alle studenten zien van vak i
print(subjects[i])
print([x.__str__() for x in subjects[i].students])


# Laat van de eerste 10 studenten de lecuters zien
print('\n\n'.join(str(y) for y in [(x.__str__(), [t.__str__() for t in x.lectures]) for x in students if subjects[i] in x.subjects][:10]))

for x in students[:20]:
    x.exportTimetable()

for x in classRooms:
    x.exportTimetable()

for x in subjects:
    x.exportTimetable()
