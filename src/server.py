from flask import Flask, request
from flask_cors import CORS
import json
import random
import sys

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

@app.route("/api/compute_items", methods=['POST'])
def compute_items():
    request_data = request.get_json()
    if request_data is None:
        return response_error()

    iid_new2org = { v: k for k, v in rdata.iid_org2new.items() }
    print iid_new2org

    team_recommendations = {
        hero['id']: [iid_new2org[iid] for iid in bmodel.rec(rdata.hid_org2new[hero['id']], 10).tolist()]
        for hero in request_data['heroes']['team']
    }

    enemy_recommendations = {
        hero['id']: [iid_new2org[iid] for iid in bmodel.rec(rdata.hid_org2new[hero['id']], 10).tolist()]
        for hero in request_data['heroes']['enemy']
    }

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

if __name__ == "__main__":
	app.run(threaded=True)