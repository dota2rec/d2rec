import sys

proj_root = '../'
sys.path.insert(0, proj_root + 'src/data-proc/')
sys.path.insert(0, proj_root + 'src/model/')
sys.path.insert(0, proj_root + 'src/utils/')

from prep import raw_data
from viz import cdf_plot
from base_model import base_model
from dummy_model import dummy_model
#from evaluation import eva
from classified_emfa_model import classified_emfa_model as cem
from evaluation_sw import eva_sw as eva
from wei_model import wei_model

# production test
#DATA_DIR = 'data/'
#TEST_DIR = 'test/'

# mini test
DATA_DIR = 'data_small/'
TEST_DIR = 'test_small/'

def evaluation():
	rdata = raw_data(proj_root)
	# base model prediction
	#bmodel = base_model(rdata, (proj_root + DATA_DIR))
	#bmodel.train()
	evaluator = eva(rdata)
	#sim_vec = evaluator.nec_eva(proj_root+TEST_DIR, bmodel)
	
	# dummy model recommendation
	#model = dummy_model(rdata, (proj_root + DATA_DIR))
	#model.train(opt='wrate')
	model = wei_model(rdata, (proj_root + DATA_DIR))
	model.train()
	# emfa model
	#model = cem(rdata, (proj_root + DATA_DIR))
	#model.train()
	# evaluation package
	sim_vec = evaluator.nec_eva(proj_root+TEST_DIR, model)
	#cdf_plot(sim_vec)
	#suf_res = evaluator.suf_eva(proj_root+TEST_DIR, model)
	#evaluator.suf_histo(suf_res, bin=10)

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