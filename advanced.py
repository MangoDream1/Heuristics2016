from process_data import *

# Advanced assignment calculations:

def classroom_occupation(classroom):
    # Get the filled and empty slots of the timetable
    filled = 0
    empty = 0

    for day, timeslot in classroom.timetable.items():
        for cell in timeslot.values():
            if cell:
                filled += 1
            else:
                empty += 1

    return filled, empty

def classroom_capacity(classroom):
    # Get average empty seats of a classroom
    total = 0

    for day, timeslot in classroom.timetable.items():
        for cell in timeslot.values():
            total += sum([classroom.capacity - len(l.students) for l in cell])

    return round(total / len(classroom.lectures))

if __name__ == "__main__":
    data_manager.importLectures(input("Enter a timetable: "))

    print("Name \t occupation \t average excess capacity")

    for c in data_manager.classrooms:
        print(c.__str__(), "\t", classroom_capacity(c),
            "\t\t", classroom_occupation(c))
