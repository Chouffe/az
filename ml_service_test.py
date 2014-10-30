import json
import settings
import requests
import db
import generator
import ml_service

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
base_url = "http://localhost:%s/service/predict/" % settings.ml_service_port

uuid = "srv"
schema = db.get_schema(uuid)
features = schema['features']

gen = generator.RandomGenerator(features)
points_to_try = gen.get(n=2)

print points_to_try


r = requests.post(base_url + uuid,
                  data=json.dumps({'points':
                                   points_to_try
                                   # [
                                   #     {
                                   #         'a1': .1,
                                   #         'a2': .1,
                                   #         'a3': .1
                                   #     },
                                   #     {
                                   #         'a1': .5,
                                   #         'a2': .25,
                                   #         'a3': .1
                                   #     }
                                   # ]
                                   }),
                  headers=headers)

print r
results =  r.json()
print results

# model = ml_service.get_model(uuid)
# print model
