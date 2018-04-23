from functools import wraps
import inspect
import numpy as np

from scipy import spatial as sp

def initializer(func):
	"""
	Automatically assigns the parameters.

	>>> class process:
	...     @initializer
	...     def __init__(self, cmd, reachable=False, user='root'):
	...         pass
	>>> p = process('halt', True)
	>>> p.cmd, p.reachable, p.user
	('halt', True, 'root')
	"""
	names, varargs, keywords, defaults = inspect.getargspec(func)

	@wraps(func)
	def wrapper(self, *args, **kargs):
		for name, arg in list(zip(names[1:], args)) + list(kargs.items()):
			setattr(self, name, arg)

		for name, default in zip(reversed(names), reversed(defaults)):
			if not hasattr(self, name):
				setattr(self, name, default)

		func(self, *args, **kargs)

	return wrapper

def topk_index(arr, k):
	arr = np.array(arr)
	return arr.argsort()[-k:][::-1]

# sufficiency evaluation
# def suf_eva():
# utils
# transform two dict to feature vector
# dic1: <iname, 1/0>
# arr2: list of iname recommended
def feature_vec(iid2name, dic1, arr2):
	kvec = []
	vec1 = []
	for k, v in dic1.iteritems():
		kvec.append(k)
		# changed from counter to 1
		vec1.append(1)
	vec2 = [0]*len(kvec)
	for iid in arr2:
		name = iid2name[iid]
		if name in kvec:
			index = kvec.index(name)
			vec2[index] = 1
		else:
			kvec.append(name)
			vec1.append(0)
			vec2.append(1)
	return vec1, vec2

# sim: similarity between item purchases
# ideal evaluation: P(Exactly same purchase log) 
# assume the input team has hero for at least one player
# @hp: actual hero-purchase counter dict array
# @hp_rec: recommended hero-purchase counter dict array
# @opt: aggregation function, average and etc
# TODO: for diff heroes, we may have different weight when calc total similarity
def team_purchase_sim_calc(iname2iid, hp, hp_rec, norm=False, sim_func='cosine'):
	#print "len(hero purchase): " + str(len(hp))
	sim_vec=[]
	tot_sim=0
	
	if sim_func == 'cosine':
		for (h, hpr) in zip(hp, hp_rec):
			#print h
			#print hpr
			# item purchase counter to feature vector
			h, hpr=feature_vec(iid2name, h, hpr)
			# do normalization if needed
			if norm:
				norm1=np.linalg.norm(hp)
				norm2=np.linalg.norm(hpr)
				h=h/norm1
				hpr=hpr/norm2
			# calc cosine similarity
			sim=1-sp.distance.cosine(h, hpr)
			# append crrent hero item similarity
			sim_vec.append(sim)
	elif sim_func == 'exist_in_rec':
		for (h, hpr) in zip(hp, hp_rec):
			if len(h)!=0:
				#print hpr
				# item purchase counter to feature vector
				success = 0
				for actual_name in h:
					if iname2iid[actual_name] in hpr:
						success += 1
				sim_vec.append((float(success)/len(h)))
	else:
		raise Exception("No similarity function " + sim_func + " is defined!")
	return sim_vec

def aggr_similarity(sim_vec, aggr_opt='avg'):
	#print "per hero similarity vector:"
	#print sim_vec
	if aggr_opt=='avg':
		tot_sim=sum(sim_vec)/len(sim_vec)
	else:
		print "no aggr function " + sim_func + " is pre defined!"
		tot_sim=-1
	return tot_sim