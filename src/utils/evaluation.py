import sys
import os
import json
import numpy as np

proj_root = '../../'
sys.path.insert(0, proj_root+'src/utils/')
sys.path.insert(0, proj_root + 'src/bean/')

from utils import team_purchase_sim_calc
from item import item_class as iclass

class eva:
	def __init__(self, rdata):
		self.iname2iid = rdata.item_name2id
		self.hname2hid = rdata.hero_name2id
		self.hid_org2new = rdata.hid_org2new
	# assumes: we have tot_count[h] that stores the avg total "vital" item purchased by hero h
	# assumes: dummy_is_vital(iid)
	# necissity evaluation
	# calculating probability 
	def nec_eva(self, fpath, model):
		mcount=0
		sim_sum=0
		for fname in os.listdir(fpath):
			data=json.load(open(fpath+fname))
			wplayers=[]
			# assumes: the first 5 is radiant hero
			# get the winner players
			if(data['radiant_win']):
				wplayers=data['players'][0:5]
			else:
				wplayers=data['players'][5:10]
			hero_vitem=[]
			rec_vitem=[]
			for p in wplayers:
				# vital items that we consider
				vitem=dict()
				purchase=p['purchase']
				hid=self.hid_org2new[p['hero_id']]
				#print "purchase length of hero " + str(hid) + ": " + str(len(purchase))
				for k in purchase:
					if k not in self.iname2iid:
						pass
					#iid = self.iname2iid[k]
					#if iclass.is_not_consider(k, iid):
					#	pass
					else:
						vitem[k]=purchase[k]
				hero_vitem.append(vitem)
				print self.hname2hid.inverse[hid]
				print "actual purchase: "
				print vitem
				#print "hero item avg count: " + str(hero_item_count[hid])
				# rec with new interface
				rec=model.rec(hid, len(vitem))
				#rec=base_rec_h(hid, model, len(vitem))
				rec_vitem.append(rec)
				# print recommended items
				print "recommended: "
				rec_name=[self.iname2iid.inverse[iid] for iid in rec]
				print rec_name
				print ""
			#print hero_vitem
			#print rec_vitem
			sim=team_purchase_sim_calc(self.iname2iid.inverse, hero_vitem, rec_vitem, sim_func='exist_in_rec')
			print "rec-actual item purchase similarity of match " + str(fname) + ": " + str(sim)
			if not np.isnan(sim):
				sim_sum=(sim_sum*mcount+sim)/(mcount+1)
				mcount+=1
		print "all winners similarity avg: " + str(sim_sum)