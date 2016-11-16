import json
import os

def exportLectures(lecture_dct, file_name):
    nLectures = max([x for x in lecture_dct if type(x) == int])

    export_dct = {x: lecture_dct[x].toLongDict() for x in range(nLectures)}

    if not os.path.exists("Timetable/Lectures"):
        os.makedirs("Timetable/Lectures")

    with open("Timetable/Lectures/%s.json" % file_name, 'w') as f:
        json.dump(export_dct, f, indent=3)

def importLectures(file_name):
    path = "Timetable/Lectures/%s.json" % file_name

    with open(path) as f:
        dct = json.load(f)

    print(dct)
