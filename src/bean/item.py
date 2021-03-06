import sys
import re
from enum import Enum

sys.path.insert(0, '../utils/')

from utils import initializer

class iclass(Enum):
	EARLY = "Early"
	MID = "Mid"
	FINAL = "Final"
	ASSIST = "Assistance"


class item:
	# transformed consume iids
	#consume_iids = [4, 5, 6, 7, 8, 9, 10, 87, 145, 151, 173, 174]
	consume_iids = [216,44,241,257,265,237,38,39,46]
	consume_iids_more = [216,40, 42, 43, 218,44,241,257,16,265,237,38,39,46,17,25,27,2]
	# enchanted mango(4)


	def __init__(self, iname2iid, iid_org2new, icost, opt='less_consume'):
		self.iid_org2new = iid_org2new
		#print "item initializer: "
		self.syn_iids = [121,123,98,250,252,263,104,141,145,147,110,249,154,158,164,235,185,229,196,242,190,231,206,208,210,212,79,81,90]
		self.syn_iids = self.lst_id_org2new(self.syn_iids)
		
		# removed from list
		# 26:216, 92:265
		self.syn_iid_child = {92:[265,20,12],102:[56],143:[17],149:[2,3],236:[18,18],152:[5],162:[17],166:[25],170:[18],187:[4,28],129:[59,61],131:[56,27],73:[20,13],75:[20,14],77:[20,15],86:[4,16],88:[28,12],125:[156,61],67:[10,28,19],98:[67,67],69:[56,57],94:[16,27],79:[94,86],180:[59],160:[24,60],48:[],196:[61,244],50:[2,2],104:[23],106:[17,28,28],119:[58],121:[69],123:[69],226:[69,59],96:[57,24],250:[149],252:[67],100:[244,57],232:[57,59],263:[236,75],108:[21,22,23],141:[52],145:[52],147:[24],223:[21,23,27,28],225:[6],256:[59,61],259:[19],110:[69],112:[4,55],114:[61,61],116:[8],139:[10,32],151:[2,13],249:[24],154:[162],172:[10],156:[26,5],158:[55],164:[56,25],174:[22,19],176:[52],178:[13,27],235:[58],185:[28,244],229:[32],196:[61,244],242:[86],127:[3,19],133:[52],135:[7,7],137:[],168:[8,240],190:[6,77],231:[],206:[73,73],239:[12,11],208:[125],210:[32],212:[88,88],214:[27,244],81:[26,94,88],63:[17,25],90:[94],247:[55],65:[],36:[34,216,16,16],254:[31],71:[182,14,14]}
		self.syn_iid_child = self.dict_id_org2new(self.syn_iid_child)

		# new consume_iids after continuous assignment
		self.consume_iids_new_more = self.lst_id_org2new(item.consume_iids_more)
		self.consume_iids_new = self.lst_id_org2new(item.consume_iids)

		# wei's list
		#self.basic_iids = [21, 31, 37, 55, 57, 59, 61, 56, 58, 60, 13, 15, 17, 19, 23, 25, 27, 29, 215, 12, 240, 52, 51, 53, 54, 3, 5, 7, 9, 11, 2, 4, 6, 8, 10, 244, 182, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 41, 181]
		#self.basic_iids = self.lst_id_org2new(self.basic_iids)
		#self.inter_iids = [48, 92,98, 102, 143, 149, 236, 152, 162, 166, 170, 187, 129,131, 73,75,77, 79,86, 88, 125,67, 69, 94, 180]
		#self.inter_iids = self.lst_id_org2new(self.inter_iids)
		#self.final_iids = [160, 196, 48, 50, 106, 119, 121, 123, 96, 250, 252, 100, 232, 263, 104, 108, 141, 145, 147, 223, 225, 256, 259, 110, 112, 114, 116, 139, 151, 249, 154, 156, 158, 164, 172, 174, 176, 178, 235, 185, 229, 196, 242, 127, 133, 135, 137, 168, 190, 231, 206, 239, 208, 210, 212, 214, 63, 81, 90, 1, 247, 65, 36, 254, 71]
		#self.final_iids = self.lst_id_org2new(self.final_iids)

		self.icost = icost
		# dust:40, ward_observer:42, ward_sentry:43
		# ward_dispenser:218, courier:45, flying_courier:84
		self.assist_iids = [40, 42, 43, 218, 45, 84, 188]
		self.assist_iids = self.lst_id_org2new(self.assist_iids)
		#print self.assist_iids

		self.iname2iid = iname2iid
		pass

	@staticmethod
	def is_recipe(iname):
		return re.match('recipe_', iname)!=None

	@staticmethod
	def is_upgrade(iname):
	    return re.match('^[A-Za-z0-9_-]*_[0-9]$', iname)!=None
	
	@staticmethod
	def is_consume(iid):
	    return (iid in item.consume_iids)
	    #return (iname2iid[iname] in consume_iids)
	@staticmethod
	def is_consume_more(iid):
	    return (iid in item.consume_iids_more)
	
	def is_consume_new(self, iname):
		return (self.iname2iid[iname] in self.consume_iids_new)

	def is_consume_new(self, iname):
		return (self.iname2iid[iname] in self.consume_iids_new_more)

	@staticmethod
	def is_not_consider(iname, iid):
	    return (item.is_recipe(iname) or item.is_upgrade(iname) or item.is_consume(iid))

	@staticmethod
	def is_not_consider_more(iname, iid):
	    return (item.is_recipe(iname) or item.is_upgrade(iname) or item.is_consume_more(iid))

	def is_not_consider_new(iname, new_iid):
		return (self.is_recipe(iname) or self.is_upgrade(iname) or self.is_consume_new(iname))

	def is_not_consider_new_more(iname, new_iid):
		return (self.is_recipe(iname) or self.is_upgrade(iname) or self.is_consume_new_more(iname))
		
	def item_name2id(iname):
		return self.iname2iid[iname]

	def item_id2name(iid):
		return self.iname2iid.inverse[iid]

	def lst_id_org2new(self, id_lst):
		new_id_lst = []
		for i in id_lst:
			if i in self.iid_org2new:
				new_id_lst.append(self.iid_org2new[i])
		return new_id_lst

	def dict_id_org2new(self, id_dict):
		new_dict = {}
		for k, v in id_dict.iteritems():
			new_child=[]
			for i in v:
				if i in self.iid_org2new:
					new_child.append(self.iid_org2new[i])
			new_dict[self.iid_org2new[k]] = new_child
		return new_dict

	def emfa_freq_classify(self, iid, opt='cost'):
		if iid in self.assist_iids:
			return iclass.ASSIST

		cost = self.icost[self.iname2iid.inverse[iid]]
		if cost > 3500:
			return iclass.FINAL
		elif cost > 1000:
			return iclass.MID
		else:
			return iclass.EARLY
