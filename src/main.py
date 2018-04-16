import sys

proj_root = '/mnt/c/Users/yukun/workspace/d2rec/'
sys.path.insert(0, proj_root + 'src/data-proc/')
sys.path.insert(0, proj_root + 'src/model/')
sys.path.insert(0, proj_root + 'src/utils/')

from prep import raw_data
from base_model import base_model
from evaluation import eva


DATA_DIR = 'data/'
TEST_DIR = 'test/'

rdata = raw_data(proj_root)
bmodel = base_model(rdata.hid_org2new, rdata.item_name2id, (proj_root + DATA_DIR))
bmodel.train()
evaluator = eva(rdata)
evaluator.nec_eva(proj_root+DATA_DIR, bmodel)


#bmodel.calc_base_freq(rdata.hero_name2id, rdata.item_name2id)