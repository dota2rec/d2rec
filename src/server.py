from flask import Flask, request
from flask_cors import CORS
import json
import random
import sys
import daemon
import os

proj_root = '../'
sys.path.insert(0, proj_root + 'src/data-proc/')
sys.path.insert(0, proj_root + 'src/model/')
sys.path.insert(0, proj_root + 'src/utils/')

from prep import raw_data
from base_model import base_model
from classify_model import classify_model
from tdv_model import tdv_model
from evaluation import eva

DATA_DIR = 'data/'
TEST_DIR = 'test/'

rdata  = raw_data(proj_root)

MODEL_DIR = './model/'
models = {}

active_model_name = ''

def import_model_class_from_file(model_name):
    model_module = __import__(model_name)
    return getattr(model_module, model_name)

for model_filename in os.listdir(MODEL_DIR):
    if model_filename.endswith('_model.py'):
        model_name = model_filename.split('.')[0]
        model_class = import_model_class_from_file(model_name)

        print '---------- Training model: ' + model_name + '----------'
        model = model_class(rdata, (proj_root + DATA_DIR))
        model.train()

        models[model_name] = model

        # set current model as active
        active_model_name = model_name

iid_new2org = { v: k for k, v in rdata.iid_org2new.items() }

dummy_item_ids = [14, 15, 16, 29, 51, 58, 69, 96, 104, 125, 133, 137, 152, 160, 162, 172, 188, 226]

app = Flask(__name__)
CORS(app)

def response_error(error=''):
    return json.dumps({ 'status': 'error', 'error': error })

def response_ok(payload=''):
    return json.dumps({ 'status': 'ok', 'data': payload })

def random_items():
    random.shuffle(dummy_item_ids)
    return dummy_item_ids[0:10]

def get_recommendations(heroes, enemy_heroes):
    results = {}

    team_hids = [h['id'] for h in heroes]
    enemy_hids = [h['id'] for h in enemy_heroes]

    for hero in heroes:
        item_ord_new_id_list = []

        rec_item_ids = models[active_model_name].rec(rdata.hid_org2new[hero['id']], 10, team_hids, enemy_hids).tolist()
        print rec_item_ids

        for item_id in rec_item_ids:
            item_org_id = iid_new2org[item_id]
            item_ord_new_id_list.append({
                'new_id': item_id,
                'id': item_org_id
            })

        results[hero['id']] = item_ord_new_id_list
    return results

@app.route("/api/test", methods=['GET'])
def test():
    return 'appears to be running'

@app.route("/api/get_models", methods=['GET'])
def get_models():
    return response_ok({
        'models': models.keys(),
        'active': active_model_name
    })

@app.route("/api/change_model", methods=['POST'])
def change_model():
    global active_model_name
    request_data = request.get_json()
    model_name = request_data['modelName']
    if model_name in models:
        print '---------- Change model to ' + model_name
        active_model_name = model_name
        return response_ok()
    else:
        return response_error('not a valid model')

@app.route("/api/compute_items", methods=['POST'])
def compute_items():
    print '---------- Predicting items using the model: ' + active_model_name
    request_data = request.get_json()
    if request_data is None:
        return response_error()

    team_recommendations = get_recommendations(request_data['heroes']['team'], request_data['heroes']['enemy'])
    enemy_recommendations = get_recommendations(request_data['heroes']['enemy'], request_data['heroes']['team'])

    return response_ok({
        'team': team_recommendations,
        'enemy': enemy_recommendations
    })

def formatOutput(string_list):
	return "Hellow World"

@app.route("/api/<match_id>", methods=['GET'])
def getResults(match_id):
    evaluator = eva(rdata)
    string_list = evaluator.nec_eva(proj_root+DATA_DIR, models[active_model_name])
    return formatOutput(string_list)

if 'PROD' in os.environ:
    with daemon.DaemonContext():
        app.run(host= '0.0.0.0', threaded=True)
else:
    app.run(threaded=True)
