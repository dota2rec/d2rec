import sys
import re

sys.path.insert(0, '../utils/')

from utils import initializer
from utils import lst_id_org2new
from utils import dict_id_org2new

class item_class:

	# transformed consume iids
	consume_iids = [4, 5, 6, 7, 8, 9, 10, 87, 145, 151, 173, 174]

	@initializer
	def __init__(self, iname2iid, iid2name):
		print "item_class initializer: "
		self.syn_iids = [121,123,98,250,252,263,104,141,145,147,110,249,154,158,164,235,185,229,196,242,190,231,206,208,210,212,79,81,90]
		self.syn_iids = lst_id_org2new(syn_iids)

		self.syn_iid_child = {121:[129],123:[69],98:[67,67],250:[98,149],252:[67],263:[102,236,75],104:[77],141:[149],145:[69],147:[170],110:[69,69],249:[152],154:[162,170],158:[166],164:[94],235:[129],185:[73],229:[187],196:[92],242:[86,125],190:[77,77],231:[79,180],206:[73,73],208:[125,143],210:[162],212:[75,88],79:[86,94],81:[88,94],90:[131,94]}
		self.syn_iid_child = dict_id_org2new(syn_iid_child)

		# new consume_iids after continuous assignment
		self.consume_iids = [216,40,42,43,218,44,241,257,265,237,38,39]
		print "original consume_iids: "
		print consume_iids

		self.consume_iids = lst_id_org2new(consume_iids)
		print "transformed consume_iids"
		print consume_iids

		self.basic_iids = [21, 31, 37, 45, 55, 57, 59, 61, 56, 58, 60, 13, 15, 17, 19, 23, 25, 27, 29, 215, 12, 240, 52, 51, 53, 54, 3, 5, 7, 9, 11, 2, 4, 6, 8, 10, 244, 182, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 41, 84, 181]
		self.basic_iids = lst_id_org2new(basic_iids)

		self.inter_iids = [48, 92,98, 102, 143, 149, 236, 152, 162, 166, 170, 187, 129,131, 73,75,77, 79,86, 88, 125,67, 69, 94, 180]
		self.inter_iids = lst_id_org2new(inter_iids)

		self.final_iids = [160, 196, 48, 50, 106, 119, 121, 123, 96, 250, 252, 100, 232, 263, 104, 108, 141, 145, 147, 223, 225, 256, 259, 110, 112, 114, 116, 139, 151, 249, 154, 156, 158, 164, 172, 174, 176, 178, 235, 185, 229, 196, 242, 127, 133, 135, 137, 168, 190, 231, 206, 239, 208, 210, 212, 214, 63, 81, 90, 1, 247, 65, 36, 254, 71]
		self.final_iids = lst_id_org2new(final_iids)
		pass

	@staticmethod
	def is_recipe(iname):
	    return re.match('recipe_', iname)!=None

	@staticmethod
	def is_upgrade(iname):
	    return re.match('^[A-Za-z0-9_-]*_[0-9]$', iname)!=None
	
	@staticmethod
	def is_consume(iid):
	    return (iid in item_class.consume_iids)
	    #return (iname2iid[iname] in consume_iids)
	
	@staticmethod
	def is_not_consider(iname, iid):
	    return (item_class.is_recipe(iname) or item_class.is_upgrade(iname) or item_class.is_consume(iid))

	def item_name2id(iname):
		return iname2iid[iname]

	def item_id2name(iid):
		return iid2name[iid]

