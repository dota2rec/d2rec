import sys

proj_root = '/mnt/c/Users/yukun/workspace/d2rec/'
sys.path.insert(0, proj_root + 'src/data-proc/')
sys.path.insert(0, proj_root + 'src/model/')

from prep import raw_data
from base_model import base_model

DATA_DIR = 'data/'
TEST_DIR = 'test/'

rdata = raw_data(proj_root)
bmodel = base_model(proj_root + DATA_DIR)
#bmodel.calc_base_freq(rdata.hero_name2id, rdata.item_name2id)