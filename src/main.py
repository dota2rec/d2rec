import sys

proj_root = '../'
sys.path.insert(0, proj_root + 'src/data-proc/')
sys.path.insert(0, proj_root + 'src/model/')
sys.path.insert(0, proj_root + 'src/utils/')

from prep import raw_data
from viz import cdf_plot
from base_model import base_model
from dummy_model import dummy_model
from evaluation import eva
from wei_model import wei_model

# production test
#DATA_DIR = 'data/'
#TEST_DIR = 'test/'

# mini test
DATA_DIR = 'mini/'
TEST_DIR = 'mini/'

def evaluation():
	rdata = raw_data(proj_root)
	# base model prediction
	#model = base_model(rdata.hid_org2new, rdata.item_name2id, (proj_root + DATA_DIR))
	#model.train()
	# classify model prediction
	#model = classify_model(rdata.hid_org2new, rdata.item_name2id, (proj_root + DATA_DIR))
	#model.train()
	
	# dummy model recommendation
	model = dummy_model(rdata, (proj_root + DATA_DIR))
	model.train(opt='wrate')

	# wei model recommendation
	#model = wei_model(rdata, (proj_root + DATA_DIR))
	#model.train()

	evaluator = eva(rdata)
	sim_vec = evaluator.nec_eva(proj_root+TEST_DIR, model)
	cdf_plot(sim_vec)
	suf_res = evaluator.suf_eva(proj_root+TEST_DIR, model)
	evaluator.suf_histo(suf_res, bin=10)

	#bmodel.calc_base_freq(rdata.hero_name2id, rdata.item_name2id)

def test():
	rdata = raw_data(proj_root)
	rdata.print_item_table()
	#child = rdata.ihelper.syn_iid_child
	#print len(child)
	#for c in child:
	#	print rdata.item_name2id.inverse[c] + ": " + str([rdata.item_name2id.inverse[i] for i in child[c]])
	#for iid in consume_iids:
	#	print rdata.item_name2id.inverse[iid] + "\t" +str(iid) + "\t" + str(rdata.iid_org2new.inverse[iid])

evaluation()
#test()