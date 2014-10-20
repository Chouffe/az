import flask
import settings

print "Test"

app = flask.Flask(__name__)


@app.route('/api/<string:uuid>', methods=['GET'])
def next_point(uuid):
    return "NEXT POINT TO TRY"


@app.route('/api/<string:uuid>', methods=['POST'])
def save_point(uuid):
    data = flask.request.json
    if not data:
        flask.abort(400)  # bad request
    return "Saving point..."

if __name__ == '__main__':
    app.run(port=settings.server_port)
