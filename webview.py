from process_data import *
from flask import *
import requests
import json

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/")
def main():
    app.logger.debug('Loading %s' % (url_for('main')))

    _id = request.args.get("id", None)

    _object = findObject(_id)

    return render_template("index.html", object=_object)

@app.route("/json", methods=["GET"])
def json():
    app.logger.debug("You have arrived at " + url_for("json"))
    _id = request.args.get("id", None)

    _object = findObject(_id)

    if _object:
        path = "Timetable/%s/%s.json" % (_object.__class__.__name__, _object.getId())

        with open(path) as f:
            data = f.read()

        return data
    else:
        return jsonify({'result': 'Error'})


def findObject(_id):
    if _id:
        _id = _id.replace('+', ' ')

    print(_id)

    _object = None
    if _id:
        try:
            _object = classroom_dct[_id]
        except:
            pass
        try:
            _object = subject_dct[_id]
        except:
            pass
        try:
            _object = student_dct[_id]
        except:
            pass

    return _object

if __name__ == "__main__":
    app.run()
