import sys
import os
import json
import numpy as np
import os
from tqdm import tqdm

proj_root = '../../'
sys.path.insert(0, proj_root+'src/utils/')
sys.path.insert(0, proj_root + 'src/bean/')

from utils import team_purchase_sim_calc

if 'PROD' not in os.environ:
	from viz import cdf_plot
	from viz import bar_plot

def get_two_teams(data):
	# assumes: the first 5 is radiant hero
	# get the winner players
	if(data['radiant_win']):
		wplayers=data['players'][0:5]
		lplayers=data['players'][5:10]
	else:
		wplayers=data['players'][5:10]
		lplayers=data['players'][0:5]
	return wplayers, lplayers

class eva:
	def __init__(self, rdata):
		self.iname2iid = rdata.item_name2id
		self.hname2hid = rdata.hero_name2id
		self.hid_org2new = rdata.hid_org2new
	# assumes: we have tot_count[h] that stores the avg total "vital" item purchased by hero h
	# assumes: dummy_is_vital(iid)
	# necissity evaluation
	# calculating probability
	# returns: a vector that records the similarity in items of winning team of each match
	def nec_eva(self, fpath, model):
		print "necissity evaluation: "
		mcount=0
		sim_sum=0
		sim_vec = []
		for fname in tqdm(os.listdir(fpath)):
			data=json.load(open(fpath+fname))
			wplayers, lplayers = get_two_teams(data)

			hero_vitem, rec_vitem = self.get_team_actual_rec_item(wplayers, model, enemies=lplayers)

			if len(hero_vitem) > 0:
				sim=team_purchase_sim_calc(self.iname2iid, hero_vitem, rec_vitem, sim_func='exist_in_rec')
				#print "rec-actual item purchase similarity of match " + str(fname) + ": " + str(sim)

				sim_vec.append(sim)
				if not np.isnan(sim):
					sim_sum=(sim_sum*mcount+sim)/(mcount+1)
					mcount+=1
		print "all winners similarity avg: " + str(sim_sum)
		return sim_vec

	# same prerequisites as nec_eva()
	# + bin: how many bucket we want to put all similarities in
	# returns
	def suf_eva(self, fpath, model):
		print "sufficiency evaluation:"
		result = []

		for fname in tqdm(os.listdir(fpath)):
			data=json.load(open(fpath+fname))
			wplayers, lplayers = get_two_teams(data)

			# similarity of the winning team
			hero_vitem, rec_vitem = self.get_team_actual_rec_item(wplayers, model, enemies=lplayers)
			if len(hero_vitem) > 0:
				sim=team_purchase_sim_calc(self.iname2iid, hero_vitem, rec_vitem, sim_func='exist_in_rec')
			result.append([sim, 1])
			# similarity of the losing team
			hero_vitem, rec_vitem = self.get_team_actual_rec_item(lplayers, model, enemies=wplayers)
			if len(hero_vitem) > 0:
				sim=team_purchase_sim_calc(self.iname2iid, hero_vitem, rec_vitem, sim_func='exist_in_rec')
			result.append([sim, 0])
		return result

	def suf_histo(self, suf_res, bin=10):
		unit = 1.0/bin
		bin = bin+1
		x = [((i*unit)+(unit/2)) for i in range(0, bin)]
		y = [0]*bin
		y_tot = [0]*bin
		for res in suf_res:
			sim = res[0]
			win = res[1]
			index = int(sim/unit)
			new_tot = y_tot[index]+1
			y[index] = (y[index]*y_tot[index]+win)/(float(new_tot))
			y_tot[index] = new_tot
		print "percentage: "
		print y
		print "sample count: "
		print y_tot
		print "bins: "
		print x

		if 'PROD' not in os.environ:
			bar_plot(x, y)

	# returns:
	# 1. hero_vitem: actual [hero*{item:count}]
	# 2. rec_vitem: recommended [item]
	def get_team_actual_rec_item(self, players, model, enemies=None):
		hero_vitem=[]
		rec_vitem=[]

		plist=[]
		for p in players:
			if p['hero_id'] != None:
					hid=self.hid_org2new[p['hero_id']]
					plist.append(hid)
			else:
				continue
		elist=[]
		for p in enemies:
			if p['hero_id'] != None:
					hid=self.hid_org2new[p['hero_id']]
					elist.append(hid)
			else:
				continue

		for p in players:
			# vital items that we consider
			vitem=dict()
			purchase=p['purchase']
			if p['hero_id'] != None:
					hid=self.hid_org2new[p['hero_id']]
			else:
				continue
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
			#print self.hname2hid.inverse[hid]
			#print "actual purchase: "
			#print vitem
			#print "hero item avg count: " + str(hero_item_count[hid])
			# rec with new interface


			rec=model.rec(hid, len(vitem), plist, elist)['basic']
			rec_vitem.append(rec)
			# print recommended items
			#print "recommended: "
			#rec_name=[self.iname2iid.inverse[iid] for iid in rec]
			#print rec_name
			#print ""
		return hero_vitem, rec_vitem
	# two evaluation plots:
	# 1. similarity distribution in all winning teams
	# 2. winning rate distribution in all similarity conditions

	# TODOs
	# 3. how much similarity can we say that the hero followed the recommended item
	# 4. inherent similarity: how much similarity in item purchase does a hero has
	# in all conditions?


	# weighting
