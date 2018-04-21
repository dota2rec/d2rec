# improvements:
# 1. classify into: early(<1000), mid term(<3000), final(>=3000), assistance(dust, ward)
# 2. determine a threshold, items with freq above which should be recommended
# 2. determine a number for each hero for each category and recommend such many items for each category
# 3. 
# 4. add the td based deviation
import json
import os
import numpy as np
import sys
from tqdm import tqdm

proj_root = '../../'
sys.path.insert(0, proj_root+'src/utils/')

from utils import initializer
from utils import topk_index

# base model that only accumulates the frequence of item occuring
# on heroes
# dependency: datapath for training dataset
# hid_org2new, iname2iid mapping set
# output is:
# self.basic_freq = [h*i]
class classified_emfa_model:
	WIN_SCORE = 1.0
	LOSE_SCORE = 0.1

	def __init__(self, rdata, datapath):
		# data and var from init
		self.hid_org2new = rdata.hid_org2new
		self.iname2iid = rdata.item_name2id
		self.ihelper = rdata.ihelper
		self.datapath = datapath
		# how many heros and items we have to consider
		hcount = self.hid_org2new.len()
		icount = self.iname2iid.len()
		# init the basic win/lose weighted frequency
		self.basic_freq = np.zeros((hcount, icount))
		# init early-mid stage avg total item count per hero
		self.avg_etot = []*hcount
		self.avg_mtot = []*hcount
		# confident final (X% confidence in terms of match time coverage)
		# 1. total item count for a match per hero
		self.conf_tot_icount = []*hcount
		# 2. total assistance item count for a match per hero
		self.conf_acount = []*hcount
		pass

	# train basic freq model using json match records data in 'datapath'
	# opt:
	# 1. freq: raw frequency with win/lose weight
	# 2. wrate: winning rate of the item
	#	2.1. TODO: how about rare cases where only several matches item i is choose 
	#		 therefore a high/low winning rate        
	def train(self, opt='freq'):
		print self.__class__.__name__ + " train(): "
		for match_file_name in tqdm(os.listdir(self.datapath)):
			match_file = open(self.datapath + match_file_name)
			match_data = json.load(match_file)
			for player in match_data['players']:
				# validate current player
				if player['hero_id'] != None and player['purchase'] != None:
					hero_id = self.hid_org2new[player['hero_id']]
				else:
					continue
				# get hid and purchases of the hero
				hero_id = self.hid_org2new[player['hero_id']]
				purchases = player['purchase']
				win = player['isRadiant'] == player['radiant_win']
				# iterate through all purchased item
				for item_name in purchases:
					# if this is an item we consider
					if item_name in self.iname2iid:
						item_id = self.iname2iid[item_name]
						hero_freq = self.basic_freq[hero_id]
						hero_freq[item_id] += classified_emfa_model.WIN_SCORE if win else classified_emfa_model.LOSE_SCORE
			match_file.close()

	# @h: the hero id
	# @k: how many items to return
	def rec(self, h, k=0, allies=None, enemies=None):
		a_num = self.conf_acount[h]
		e_num = self.avg_etot[h]
		m_num = self.avg_mtot[h]
		f_num = self.conf_tot_icount[h] - e_num - m_num - a_num
		class2count = {"Assist":a_num, "Early":e_num, "Mid":m_num, "Final":f_num}
		# get the sorted item id list
		hifreq = self.basic_freq[h]
		tki = topk_index(hifreq, len(hifreq))
		# classified top k item recommendation dict
		classified_tki = {"Assist":[], "Early":[], "Mid":[], "Final":[]}

		for iid in range(0, len(tki)):
			# classify into four classes
			c = self.ihelper.emfa_freq_classify(iid)
			# if the current class is not full, add the item for recommendation
			if len(classified_tki[c]) < class2count[c]:
				classified_tki[c].append(iid)
		return classified_tki
