import json
import os
import numpy as np

class base_model:
	WIN_SCORE = 1.2
	LOSE_SCORE = 0.8

	def __init__(self, datapath):
		self.datapath = datapath

	def calc_base_freq(hname2hid, iname2iid, consider_func='cost'):
		hero_count = 1000
		item_count = 1000
		#hero_count = len(hname2hid)
		#item_count = len(iname2iid)
		self.basic_freq = np.zeros((hero_count, item_count))
		for match_file_name in os.listdir(self.datapath):
			match_file = open(self.datapath + match_file_name)
			match_data = json.load(match_file)
			for player in match_data['players']:
				hero_id = player['hero_id']
				purchases = player['purchase']

				win = player['isRadiant'] == player['radiant_win']
				for item_name in purchases:
					if item_name in iname2iid:
						item_id = iname2iid[item_name]
				    	#if is_consider(item_name, consider_func) and purchases[item_name] is not None:
				    	hero_freq = basic_freq[hero_id]
				    	hero_freq[item_id] += base_model.WIN_SCORE if win else base_model.LOSE_SCORE
			match_file.close()
