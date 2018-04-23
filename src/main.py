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
from classified_emfa_model import classified_emfa_model as cem
#from evaluation_sw import eva_sw as eva
from dummy_model import dummy_model as dummy
from viz import norm_dist_plot

def test():
	rdata = raw_data(proj_root)
	rdata.print_item_table()
	#child = rdata.ihelper.syn_iid_child
	#print len(child)
	#for c in child:
	#	print rdata.item_name2id.inverse[c] + ": " + str([rdata.item_name2id.inverse[i] for i in child[c]])
	#for iid in consume_iids:
	#	print rdata.item_name2id.inverse[iid] + "\t" +str(iid) + "\t" + str(rdata.iid_org2new.inverse[iid])

def construct_env(mname='base'):
	rdata = raw_data(proj_root)
	evaluator = eva(rdata)

	DATA_DIR = "../data/"
	TEST_DIR = "../test/"
	model = None
	if mname=='base':
		model = base_model(rdata, DATA_DIR)
	elif mname=='emfa':
		model = cem(rdata, DATA_DIR)
	elif mname=='dummy':
		model = dummy(rdata, DATA_DIR)
	else:
		print "invalid model!"
		exit()
	model.train()
	sim_vec = evaluator.nec_eva(TEST_DIR, model)
	cdf_plot(sim_vec)
	norm_dist_plot(sim_vec)
	return model

#if len(sys.argv) > 0:
#	rdata = raw_data(proj_root)
#	evaluator = eva(rdata)
#
#	DATA_DIR = sys.argv[2]
#	TEST_DIR = sys.argv[3]
#
#	model = None
#	if sys.argv[1]=='base':
#		model = base_model(rdata, DATA_DIR)
#	elif sys.argv[1]=='emfa':
#		model = cem(rdata, DATA_DIR)
#	elif sys.argv[1]=='dummy':
#		model = dummy(rdata, DATA_DIR)
#	else:
#		print "invalid model!"
#		exit()
#
#	model.train()
#	sim_vec = evaluator.nec_eva(TEST_DIR, model)
#	cdf_plot(sim_vec)
#	norm_dist_plot(sim_vec)
#	suf_res = evaluator.suf_eva(TEST_DIR, model)
#	evaluator.suf_histo(suf_res, bin=20)
#else:
#	test()