import flask

import experiments
import settings
import json
import db
import ml
import utils
import data_handling

service = flask.Flask(__name__)

@service.route('/service/demo/<string:uuid>', methods=['POST'])
def run_demo(uuid):
    experiments.run_demo(uuid)
    return json.dumps({'results': 'running'})

if __name__ == '__main__':
    service.run(port=settings.demo_service_port)

