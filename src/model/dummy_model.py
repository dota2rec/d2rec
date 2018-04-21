import json
import os
import numpy as np
import sys
from tqdm import tqdm
import pickle

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
class dummy_model(base_model):

	def __init__(self, rdata, datapath):
		self.hid_org2new = rdata.hid_org2new
		self.iname2iid = rdata.item_name2id
		self.datapath = datapath

		hcount = self.hid_org2new.len()
		icount = self.iname2iid.len()
		self.basic_freq = np.zeros((hcount, icount))
		# for winning rate
		self.basic_wr = np.zeros((hcount, icount))
		pass

	# train basic freq model using json match records data in 'datapath'
	def train(self, opt='freq'):
		# [h*i] item occurence total
		hi_total=[]
		#if opt=='wrate':
		hi_total=np.zeros((len(self.hid_org2new), len(self.iname2iid)))

		print self.__class__.__name__ + " train(): "
		for match_file_name in tqdm(os.listdir(self.datapath)):
			match_file = open(self.datapath + match_file_name)
			match_data = json.load(match_file)
			for player in match_data['players']:
				if player['hero_id'] != None and player['purchase'] != None:
					hero_id = self.hid_org2new[player['hero_id']]
				else:
					continue
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

						#if opt=='freq':
						hero_freq = self.basic_freq[hero_id]
						hero_freq[item_id] += base_model.WIN_SCORE if win else base_model.LOSE_SCORE
						#elif opt=='wrate':
						hero_wr = self.basic_wr[hero_id]
						hero_wr[item_id] += 1 if win else 0
						hi_total[hero_id][item_id] += 1
				# use item_vec here for stats purpose per hero in a match
			match_file.close()
		#if opt == 'wrate':
		print self.basic_freq[0]

		print self.basic_wr[0]
		print hi_total[0]
		self.basic_wr = np.divide(self.basic_wr, hi_total, out=np.zeros_like(self.basic_wr), where=hi_total!=0)
		print self.basic_wr[0]
	# @h: the hero id
	# @k: how many items to return
	def rec(self, h, k, allies=None, enemies=None):
		hifreq = self.basic_freq[h]
		tki = topk_index(hifreq, k)
		#print "recommended length: " + str(len(tki))
		return {'basic':tki}