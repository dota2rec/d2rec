import sys

proj_root = '../'
sys.path.insert(0, proj_root + 'src/data-proc/')
sys.path.insert(0, proj_root + 'src/model/')
sys.path.insert(0, proj_root + 'src/utils/')

from prep import raw_data
from viz import cdf_plot
from base_model import base_model
from classify_model import classify_model
from evaluation import eva


DATA_DIR = 'data/'
TEST_DIR = 'test/'

rdata = raw_data(proj_root)
model = base_model(rdata.hid_org2new, rdata.item_name2id, (proj_root + DATA_DIR))
model.train()

#model = classify_model(rdata.hid_org2new, rdata.item_name2id, (proj_root + DATA_DIR))
#model.train()

evaluator = eva(rdata)
sim_vec = evaluator.nec_eva(proj_root+TEST_DIR, model)
cdf_plot(sim_vec)
suf_res = evaluator.suf_eva(proj_root+TEST_DIR, model)
evaluator.suf_histo(suf_res, bin=20)

#bmodel.calc_base_freq(rdata.hero_name2id, rdata.item_name2id)