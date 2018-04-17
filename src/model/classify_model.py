import json
import os
import numpy as np
import sys

proj_root = '../../'
sys.path.insert(0, proj_root+'src/utils/')
sys.path.insert(0, proj_root+'src/model/')

from utils import initializer
from utils import topk_index
from base_model import base_model

# base model that only accumulates the frequence of item occuring
# on heroes
# dependency: datapath for training dataset
# hid_org2new, iname2iid mapping set
# output is:
# self.basic_freq = [h*i]
class classify_model(base_model):
	WIN_SCORE = 1.2
	LOSE_SCORE = 0.8

	def __init__(self, hid_org2new, iname2iid, datapath):
		self.hid_org2new = hid_org2new
		self.iname2iid = iname2iid
		self.datapath = datapath

		hcount = self.hid_org2new.len()
		icount = self.iname2iid.len()
		self.basic_freq = np.zeros((hcount, icount))
		pass

	# train basic freq model using json match records data in 'datapath'
	def train(self):
		for match_file_name in os.listdir(self.datapath):
			match_file = open(self.datapath + match_file_name)
			match_data = json.load(match_file)
			for player in match_data['players']:
				hero_id = self.hid_org2new[player['hero_id']]
				purchases = player['purchase']

				win = player['isRadiant'] == player['radiant_win']
				# vectorize frequency
				item_vec = [0]*len(self.iname2iid)
				for item_name in purchases:
					# if we consider this item
					if item_name in self.iname2iid:
						item_count = purchases[item_name]
						item_id = self.iname2iid[item_name]

						if item_count == None:
							item_count = 0
						item_vec[item_id] = int(item_count)

						hero_freq = self.basic_freq[hero_id]
				    	hero_freq[item_id] += base_model.WIN_SCORE if win else base_model.LOSE_SCORE
				# use item_vec here for stats purpose per hero in a match
			match_file.close()
	# @h: the hero id
	# @k: how many items to return
	def rec(self, h, k):
		hifreq = self.basic_freq[h]
		tki = topk_index(hifreq, k)
		print "recommended length: " + str(len(tki))
		return tki

#	def calc_base_freq(hname2hid, iname2iid, consider_func='cost'):
#		#hero_count = 1000
#		#item_count = 1000
#		hero_count = hname2hid.len()
#		item_count = iname2iid.len()
#		self.basic_freq = np.zeros((hero_count, item_count))
#		for match_file_name in os.listdir(self.datapath):
#			match_file = open(self.datapath + match_file_name)
#			match_data = json.load(match_file)
#			for player in match_data['players']:
#				hero_id = player['hero_id']
#				purchases = player['purchase']
#
#				win = player['isRadiant'] == player['radiant_win']
#				for item_name in purchases:
#					if item_name in iname2iid:
#						item_id = iname2iid[item_name]
#				    	#if is_consider(item_name, consider_func) and purchases[item_name] is not None:
#				    	hero_freq = basic_freq[hero_id]
#				    	hero_freq[item_id] += base_model.WIN_SCORE if win else base_model.LOSE_SCORE
#			match_file.close()