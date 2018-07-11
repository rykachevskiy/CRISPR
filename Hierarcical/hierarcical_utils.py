
# coding: utf-8

import editdistance as ed
import numpy as np
from tqdm import tqdm_notebook
from collections import Counter, OrderedDict



def find_closest(d, init_item):
    '''finds closest in dictionary d to init item'''
    min_ed = 999
    answ_item = [-1, -1]
    for comp_item in d.keys():
        dist = ed.eval(init_item, comp_item)
        if dist < min_ed:
            min_ed = dist
            answ_item = (min_ed, comp_item)

    return answ_item


def squash(od, t, verbose = False):
    answ = OrderedDict()
    sp_to_n = {}
    index = 0
    
    for init_item in tqdm_notebook(od.items()):
        #ord_dict.pop(init_item[0])

        if len(answ) == 0 :
            if verbose: print("new spacer:", init_item[0], init_item[1])
            answ[init_item[0]] = init_item[1]
            sp_to_n[init_item[0]] = index
            index += 1
        else:
            min_ed, answ_item = find_closest(answ, init_item[0])
            if min_ed < t:
                if verbose: print("add:", init_item[0], "to", answ_item, )
                answ[answ_item] += init_item[1]
                sp_to_n[init_item[0]] = sp_to_n[answ_item]
                
            else:
                if verbose: print("new spacer:", init_item[0], init_item[1])
                sp_to_n[init_item[0]] = index
                index += 1
                answ[init_item[0]] = init_item[1]
                
        cl_to_n = {}
		n_to_cl = {}
		for i, it in enumerate(answ.items()):
		    cl_to_n[it[0]] = i
		    n_to_cl[i] = it[0]

    return answ, sp_to_n, cl_to_n, n_to_cl


def counter_to_ordered_dict(counter):
    ord_dict = OrderedDict()

    u_lines = []
    counts = []
    for item in counter.items():
        u_lines.append(item[0])
        counts.append(item[1])

    u_lines = np.array(u_lines)
    counts = np.array(counts)

    args_s = np.argsort(counts)[::-1]

    for l, c in zip(u_lines[args_s], counts[args_s]):
        ord_dict[l] = c
    
    return ord_dict


def process_pair(pair, cl_to_num, t = 6):
    try:
        return [cl_to_n[find_closest(cl_to_num, pair[0])[1]], cl_to_n[find_closest(cl_to_num, pair[1])[1]]]
    except:
        return [-1, -1]

