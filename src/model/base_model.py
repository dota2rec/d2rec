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
class base_model:
	WIN_SCORE = 1.0
	LOSE_SCORE = 0.1

	def __init__(self, rdata, datapath):
		self.hid_org2new = rdata.hid_org2new
		self.iname2iid = rdata.item_name2id
		self.datapath = datapath

		hcount = self.hid_org2new.len()
		icount = self.iname2iid.len()
		self.basic_freq = np.zeros((hcount, icount))
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
				hero_id = player['hero_id']
				# validate current player
				if hero_id != None and player['purchase'] != None and hero_id in self.hid_org2new:
					hero_id = self.hid_org2new[hero_id]
				else:
					continue
				purchases = player['purchase']

				win = player['isRadiant'] == player['radiant_win']
				for item_name in purchases:
					if item_name in self.iname2iid:
						item_id = self.iname2iid[item_name]
						#if is_consider(item_name, consider_func) and purchases[item_name] is not None:
						hero_freq = self.basic_freq[hero_id]
						hero_freq[item_id] += base_model.WIN_SCORE if win else base_model.LOSE_SCORE
			match_file.close()
	# @h: the hero id
	# @k: how many items to return
	def rec(self, h, k, allies=None, enemies=None):
		hifreq = self.basic_freq[h]
		tki = topk_index(hifreq, k)
		#print "recommended length: " + str(len(tki))
		return {'basic':tki.tolist()}
