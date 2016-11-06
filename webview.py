# import all the data from process_data
from process_data import *

i=1

print(subjects[i])
print("\n".join([x.__str__() for x in subjects[i].getPractica()]))
print([(x.group, len([y.__str__() for y in x.students]), [y.__str__() for y in x.students]) for x in subjects[i].getPractica()])


# In[103]:

# Laat alle werkgroepen zien van vak i

print(subjects[i])
print("\n".join([x.__str__() for x in subjects[i].getWorkLectures()]))
print([(x.group, len([y.__str__() for y in x.students]), [y.__str__() for y in x.students]) for x in subjects[i].getWorkLectures()])


# In[104]:

# Laat alle studenten zien van vak i
print(subjects[i])
print([x.__str__() for x in subjects[i].students])


# Laat van de eerste 10 studenten de lecuters zien
print('\n\n'.join(str(y) for y in [(x.__str__(), [t.__str__() for t in x.lectures]) for x in students[:10]]))

for x in students[:10]:
    x.exportRoster()

for x in classRooms:
    x.exportRoster()
