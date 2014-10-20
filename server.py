import flask
import settings
import json
import db
import data_handling

app = flask.Flask(__name__)


@app.route('/api/<string:uuid>', methods=['GET'])
def next_point(uuid):
    return "NEXT POINT TO TRY"


@app.route('/api/<string:uuid>', methods=['POST'])
def save_point(uuid):
    """Saves the datapoint sent
    It returns success or an error message"""
    data = flask.request.json
    if not data:
        flask.abort(400)  # bad request
    # TODO: add data validation
    result, features = data_handling.api_preprocess_datapoint(data)
    try:
        db.write_datapoint(uuid, features, result)
        return json.dumps({'error': None})
    except Error:
        return json.dumps({'error': 'An error occured'})


if __name__ == '__main__':
    app.run(port=settings.server_port)
