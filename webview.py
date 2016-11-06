from process_data import *

i=1

print(subjects[i])
print("\n".join([x.__str__() for x in subjects[i].practicas]))
print([(x.group, len([y.__str__() for y in x.students]), [y.__str__() for y in x.students]) for x in subjects[i].practicas])


# In[103]:

# Laat alle werkgroepen zien van vak i

print(subjects[i])
print("\n".join([x.__str__() for x in subjects[i].workLectures]))
print([(x.group, len([y.__str__() for y in x.students]), [y.__str__() for y in x.students]) for x in subjects[i].workLectures])


# In[104]:

# Laat alle studenten zien van vak i
print(subjects[i])
print([x.__str__() for x in subjects[i].students])
