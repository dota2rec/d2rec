import json
import re
import sys

proj_root = '../'

sys.path.insert(0, proj_root + 'src/utils/')
sys.path.insert(0, proj_root + 'src/bean/')

from bidict import bdict
from item import item_class as iclass

class raw_data(object):
	"""docstring for raw_data"""
	def __init__(self, proj_root):
		super(raw_data, self).__init__()
		self.hero_name2id, self.hid_org2new, self.item_name2id, self.item_cost,\
		self.iid_org2new = self.prepare_hero_item_info(proj_root)

	# according to the json data reindex continuously
	# @return
	# 1: name2id map
	# 2: orgid2newid map
	def build_hname2hid_map_reindex(self, data):
	    hid_data = bdict()
	    hid_org2new = bdict()
	    ignore = 0
	    for i in range(0, len(data)):
	        # substitute prefix part
	        name = re.sub('(npc_dota_hero_|item_)', '', data[i]['name'])
	        hid = data[i]['id']
	        # not repeated item/hero
	        if name not in hid_data:
	            # 1. remove recipe item
	            # 2. remove consume item
	            # 3. remove upgraded versions of an item
	            newid = i - ignore
	            hid_data[name] = newid
	            hid_org2new[hid] = newid
	        else:
	            print "ignored hero: " + str(name) + "\t" + str(iid)
	            ignore += 1
	    return hid_data, hid_org2new

	def build_iname2iid_map_reindex(self, data):
		name2iid = bdict()
		iid_cost = dict()
		iid_org2new = bdict()
		ignore = 0
		for i in range(0, len(data)):
			# substitute prefix part
			name = re.sub('(npc_dota_hero_|item_)', '', data[i]['name'])
			iid = data[i]['id']
			# not repeated item/hero
			if (name not in name2iid) and (not iclass.is_not_consider(name, iid)):
				# 1. remove recipe item
				# 2. remove consume item
				# 3. remove upgraded versions of an item
				iid_cost[name] = int(data[i]['cost'])
				newid = i - ignore
				name2iid[name] = newid
				iid_org2new[iid] = newid
			else:
				if iid in iclass.consume_iids:
					print "ignored consume item: " + str(name) + "\t" + str(iid)
				ignore += 1
		return name2iid, iid_cost, iid_org2new

	def prepare_hero_item_info(self, proj_root):
		hpath = proj_root + 'heroes.json'
		#print hpath
		ipath = proj_root + 'items.json'
		#print ipath

		hero_list = json.load(open(hpath))['rows']
		item_list = json.load(open(ipath))['rows']

		hero_name2id, hid_org2new = self.build_hname2hid_map_reindex(hero_list)
		item_name2id, item_cost, iid_org2new = self.build_iname2iid_map_reindex(item_list)

		return hero_name2id, hid_org2new, item_name2id, item_cost, iid_org2new

	def get_all_hero_item_info(self):
		return self.hero_name2id, self.hid_org2new, self.item_name2id, self.item_cost, self.iid_org2new

	def print_item_table(self):
		print "name\t org_id\t new_id"
		for name, new_id in self.item_name2id.iteritems():
			print name+"\t"+str(self.iid_org2new.inverse[new_id])+"\t"+str(new_id)

def test():
	alldata = raw_data(proj_root)
	hero_name2id, hid_org2new, item_name2id, item_cost, iid_org2new \
		= alldata.prepare_hero_item_info(proj_root)
	#print "hero bidict:"
	#hero_name2id.__print__()
	#print ""
	#hid_org2new.__print__()

	#print "item bidict:"
	#item_name2id.__print__()
	#print item_cost
	#iid_org2new.__print__()

test()