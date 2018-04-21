# -*- coding: utf-8 -*-
import json
import os
import numpy as np
import sys
from tqdm import tqdm

proj_root = '../../'
sys.path.insert(0, proj_root+'src/utils/')
sys.path.insert(0, proj_root+'src/model/')

from utils import initializer
from utils import topk_index
from base_model import base_model
from item import item_class 

# base model that only accumulates the frequence of item occuring
# on heroes
# dependency: datapath for training dataset
# hid_org2new, iname2iid mapping set
# output is:
# self.basic_freq = [h*i]
class classify_model_sw(base_model):
    WIN_SCORE = 1.5
    LOSE_SCORE = 0.4
    SUPPORT_WIN_SCORE = 2.0
    SUPPORT_LOSE_SCORE = 0.8
        
    def __init__(self, hid_org2new, iname2iid,item_cost,syn_iid_child, datapath):
        self.hid_org2new = hid_org2new
        self.iname2iid = iname2iid
        self.item_cost = item_cost
        self.datapath = datapath
        self.syn_iid_child = syn_iid_child
                
        hcount = self.hid_org2new.len()
        icount = self.iname2iid.len()
        self.basic_freq = np.zeros((hcount, icount))
        #count what item your ally purchase
        self.support_from_ally_freq = np.zeros((hcount,hcount,icount))
        #count what item your enemy purchase
        self.support_from_ememy_freq = np.zeros((hcount,hcount,icount))
        pass
    
        # train basic freq model using json match records data in 'datapath'
    def train(self):
        print self.__class__.__name__ + " train(): "
        for match_file_name in tqdm(os.listdir(self.datapath)):
            match_file = open(self.datapath + match_file_name)
            match_data = json.load(match_file)
            ######################################
            #get hero_id list of two teams
            list_radiant = []
            list_dire = []
            for player in match_data['players']:
                if player['hero_id'] != None and player['purchase'] != None:
                    id = self.hid_org2new[player['hero_id']]
                    if player['isRadiant']:
                        list_radiant.append(id)
                    else:
                        list_dire.append(id)
                    
            if len(list_radiant)!= 5 or len(list_dire)!=5:
                continue
            #######################################
            for player in match_data['players']:
                if player['hero_id'] != None and player['purchase'] != None:
                    hero_id = self.hid_org2new[player['hero_id']]
                else:
                    continue
                purchases = player['purchase']
                                
                win = player['isRadiant'] == player['radiant_win']
                # vectorize frequency
#                item_vec = [0]*len(self.iname2iid)
                item_vec = np.zeros(len(self.iname2iid))
                for item_name in purchases:
                    # if we consider this item
                    if item_name in self.iname2iid:
                        item_count = purchases[item_name]
                        item_id = self.iname2iid[item_name]
                                                
                        if item_count == None:
                            item_count = 0
                        item_vec[item_id] = item_vec[item_id] + 1
                        
                        if item_id in self.syn_iid_child.keys():
                            for it in self.syn_iid_child[item_id]:
                                if item_vec[it] >0:
                                    item_vec[it] = item_vec[it] -1
                                    
                                
               
                
                hero_freq = self.basic_freq[hero_id]
                if win:
                    hero_freq += item_vec * classify_model_sw.WIN_SCORE
                else:
                    hero_freq += item_vec * classify_model_sw.LOSE_SCORE

                    
                ####### Here I directly use vec_item and if it's not the vector of item frequence for this player,plesse modify it
                vector = item_vec.copy()
                if hero_id in list_radiant:
                    for id in list_radiant:
                        if id != hero_id:
                            if win:
                                self.support_from_ally_freq[id][hero_id] += vector * classify_model_sw.SUPPORT_WIN_SCORE
                            else:
                                self.support_from_ally_freq[id][hero_id] += vector * classify_model_sw.SUPPORT_LOSE_SCORE
                    for id in list_dire:
                        if win:
                            self.support_from_ememy_freq[id][hero_id] += vector * classify_model_sw.SUPPORT_LOSE_SCORE
                        else:
                            self.support_from_ememy_freq[id][hero_id] += vector * classify_model_sw.SUPPORT_WIN_SCORE
                else:
                    for id in list_dire:
                        if id != hero_id:
                            if win:
                                self.support_from_ally_freq[id][hero_id] += vector * classify_model_sw.SUPPORT_WIN_SCORE
                            else:
                                self.support_from_ally_freq[id][hero_id] += vector * classify_model_sw.SUPPORT_LOSE_SCORE
                    for id in list_radiant:
                        if win:
                            self.support_from_ememy_freq[id][hero_id] += vector * classify_model_sw.SUPPORT_LOSE_SCORE
                        else:
                            self.support_from_ememy_freq[id][hero_id] += vector * classify_model_sw.SUPPORT_WIN_SCORE

                ##############################
                
                
                # use item_vec here for stats purpose per hero in a match
            match_file.close()

    def get_item_id2cost(self):
        item_id2cost = {}
        for item in self.item_name2id.keys():
            item_id2cost[self.item_name2id[item]] = self.item_cost[item]                       
        return item_id2cost

    
# @h: the hero id
# @k: how many items to return
    def rec(self, h, k,ally_list,enemy_list):
        hifreq = self.basic_freq[h].copy()
        
        for hero in ally_list:
            hid = self.hid_org2new[hero['hero_id']]
            if hid != h:
                hifreq += self.support_from_ally_freq[hid][h]
        for hero in enemy_list:
            hid = self.hid_org2new[hero['hero_id']]
            hifreq += self.support_from_ememy_freq[hid][h]
        

        item_id2cost = {}
        #print self.iname2iid
        #print self.item_cost
        for item in self.iname2iid.keys():
            item_id2cost[self.iname2iid[item]] = self.item_cost[item]
        #print item_id2cost
        print h           
        
        tki = topk_index(hifreq, int(3.0*k))
 
        
        count_1000 = 0
        count_1000_2800 = 0
        count_2800 = 0
        list_1000 = []
        list_1000_2800 =[]
        list_2800 = []
        for index in tki:
            if item_id2cost[index] < 1000 and item_id2cost[index] > 60  and item_id2cost[index]and count_1000 < 7:
                list_1000.append(index)
                count_1000 +=1
            if item_id2cost[index] >= 1000 and item_id2cost[index] < 2800 and count_1000_2800 < 5:
                list_1000_2800.append(index)
                count_1000_2800 +=1
            if item_id2cost[index] >= 2800 and count_2800 < 9:
                list_2800.append(index)
                count_2800 += 1
        rec_list = list_1000 + list_1000_2800 + list_2800
        rec_array = np.asarray(rec_list)
        #print h
        print list_1000,list_1000_2800 ,list_2800
        
    
        return rec_array

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
