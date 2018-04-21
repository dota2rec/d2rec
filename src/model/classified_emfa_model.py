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
sys.path.insert(0, proj_root+'src/bean/')

from utils import initializer
from utils import topk_index
from item import iclass

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
		self.tot_by_class = {iclass.EARLY:([[] for i in range(0, hcount)]), \
			iclass.MID:([[] for i in range(0, hcount)])}
		# confident final (X% confidence in terms of match time coverage)
		# 1. total item count for a match per hero
		self.conf_all_icount = []*hcount
		self.all_icount = [[] for i in range(0, hcount)]
		# 2. total assistance item count for a match per hero
		self.conf_acount = []*hcount
		self.tot_acount = [[] for i in range(0, hcount)]
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
				# how many final item present at this match for this hero
				fcount = 0
				# how many item in total
				count = 0
				acount = 0
				# init a temp stats dict for item count in diff class
				tmp_tot = {}
				for key in tot_by_class:
					tmp_tot[key] = 0
				# iterate through all purchased item
				for item_name in purchases:
					# if this is an item we consider
					if item_name in self.iname2iid:
						# calc the total relevant item purchased in this game
						if purchases[item_name] != None:
							count += purchases[item_name]

						item_id = self.iname2iid[item_name]
						# calc the basic weighted frequency matrix
						hero_freq = self.basic_freq[hero_id]
						hero_freq[item_id] += classified_emfa_model.WIN_SCORE if win else classified_emfa_model.LOSE_SCORE
						# get the class of the item
						item_class = self.ihelper.emfa_freq_classify(item_id)
						# if this is a class we have interests in
						if item_class in tot_by_class:
							tmp_tot[item_class] += 1
						elif item_class == iclass.FINAL:
							fcount += 1
						elif item_class == iclass.ASSIST:
							acount += 1
				if fcount > 0:
					# append the current match 
					for key in tmp_tot:
						tot_by_class[key][hero_id].append(tmp_tot[key])
				self.all_icount[hero_id].append(count)
				self.tot_acount[hero_id].append(acount)
				# TODO
				# calc the avg purchase amount of em items
				# calc the total icount and acount that is larger than item count in 90% games
				# is_assistance() in item.py
			match_file.close()

	# @h: the hero id
	# @k: how many items to return
	def rec(self, h, k=0, allies=None, enemies=None):
		a_num = self.conf_acount[h]
		e_num = self.avg_etot[h]
		m_num = self.avg_mtot[h]
		f_num = self.conf_all_icount[h] - e_num - m_num - a_num
		class2count = {iclass.ASSIST:a_num, iclass.EARLY:e_num, iclass.MID:m_num, iclass.FINAL:f_num}
		# get the sorted item id list
		hifreq = self.basic_freq[h]
		tki = topk_index(hifreq, len(hifreq))
		# classified top k item recommendation dict
		classified_tki = {iclass.ASSIST:[], iclass.EARLY:[], iclass.MID:[], iclass.FINAL:[]}

		for iid in range(0, len(tki)):
			# classify into four classes
			c = self.ihelper.emfa_freq_classify(iid)
			# if the current class is not full, add the item for recommendation
			if len(classified_tki[c]) < class2count[c]:
				classified_tki[c].append(iid)
		return classified_tki
