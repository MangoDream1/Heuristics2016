from process_data import *
from flask import *
import requests
import json
from os import listdir

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/")
def main():
    app.logger.debug('Loading %s' % (url_for('main')))

    # Get timetable_id if there is one
    timetable_id = request.args.get("t", None)

    # Import the lecture package and export json files for everything with
    # a timetable so that javascript can read it
    if timetable_id:
        data_manager.importLectures(timetable_id)
        data_manager.exportTimetable()

    # Get id of the timetable that will be read
    _id = request.args.get("id", None)

    # find the correct timetable
    _object = findObject(_id)

    # Create a dict of all information needed for Jinja2 so it can render correct
    # HTML for all the functionalities.
    available_items = {"classrooms": data_manager.classrooms,
                       "students": data_manager.students,
                       "subjects": data_manager.subjects,
                       "lectures": [x.strip(".json")
                        for x in listdir("Timetable/Lectures")]}

    # Render the template
    return render_template("index.html", object=_object,
        available_items=available_items)

@app.route("/json", methods=["GET"])
def json():
    """From this function the javascript will get the json files using GET"""

    app.logger.debug("You have arrived at " + url_for("json"))
    _id = request.args.get("id", None)

    _object = findObject(_id)

    # Return the correct json file of the id
    if _object:
        path = "Timetable/%s/%s.json" % (_object.__class__.__name__, _object.getId())

        with open(path) as f:
            data = f.read()

        return data
    else:
        return jsonify({'result': 'Error'})

def findObject(_id):
    """ Find the object in all the dicts """ 

    if _id:
        _id = _id.replace('+', ' ')

    print(_id)

    _object = None
    if _id:
        try:
            _object = data_manager.classroom_dct[_id]
        except:
            pass
        try:
            _object = data_manager.subject_dct[_id]
        except:
            pass
        try:
            _object = data_manager.student_dct[_id]
        except:
            pass

    return _object

if __name__ == "__main__":
    app.run()
