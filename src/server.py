from flask import Flask, request
from flask_cors import CORS
import json
import random
import sys
import daemon

proj_root = '../'
sys.path.insert(0, proj_root + 'src/data-proc/')
sys.path.insert(0, proj_root + 'src/model/')
sys.path.insert(0, proj_root + 'src/utils/')

from prep import raw_data
from base_model import base_model
from evaluation import eva

DATA_DIR = 'data/'
TEST_DIR = 'test/'

rdata  = raw_data(proj_root)
bmodel = base_model(rdata.hid_org2new, rdata.item_name2id, (proj_root + DATA_DIR))
bmodel.train()

iid_new2org = { v: k for k, v in rdata.iid_org2new.items() }

dummy_item_ids = [14, 15, 16, 29, 51, 58, 69, 96, 104, 125, 133, 137, 152, 160, 162, 172, 188, 226]

app = Flask(__name__)
CORS(app)

def response_error():
    return json.dumps({ 'status': 'error' })

def response_ok(payload):
    return json.dumps({ 'status': 'ok', 'data': payload })

def random_items():
    random.shuffle(dummy_item_ids)
    return dummy_item_ids[0:10]

def get_recommendations(heroes):
    results = {}

    for hero in heroes:
        item_ord_new_id_list = []

        rec_item_ids = bmodel.rec(rdata.hid_org2new[hero['id']], 10).tolist()
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

@app.route("/api/compute_items", methods=['POST'])
def compute_items():
    request_data = request.get_json()
    if request_data is None:
        return response_error()

    team_recommendations = get_recommendations(request_data['heroes']['team'])
    enemy_recommendations = get_recommendations(request_data['heroes']['enemy'])

    print team_recommendations

    # team_recommendations = {
    #     hero['id']: [iid_new2org[iid] for iid in bmodel.rec(rdata.hid_org2new[hero['id']], 10).tolist()]
    #     for hero in request_data['heroes']['team']
    # }

    # enemy_recommendations = {
    #     hero['id']: [iid_new2org[iid] for iid in bmodel.rec(rdata.hid_org2new[hero['id']], 10).tolist()]
    #     for hero in request_data['heroes']['enemy']
    # }

    return response_ok({
        'team': team_recommendations,
        'enemy': enemy_recommendations
    })

def formatOutput(string_list):

	return "Hellow World"

@app.route("/api/<match_id>", methods=['GET'])
def getResults(match_id):
    evaluator = eva(rdata)
    string_list = evaluator.nec_eva(proj_root+DATA_DIR, bmodel)
    return formatOutput(string_list)

with daemon.DaemonContext():
	app.run(host= '0.0.0.0', threaded=True)