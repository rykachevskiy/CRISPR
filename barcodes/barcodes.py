import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm

import sys
from importlib import reload
import regex as re

import crispr_assembler as ca

import pickle

sys.path.append("../utils")
from misc import *
from ..utils.misc import *


DEBUG = 1

m1s = 'AAGCAGTGGTATCAACGCAGAGT'
p = re.compile('(?:' + m1s + '){e<=2}')
p_cut = re.compile('(?:' + m1s[-11:] + '){e<=2}')
p_rc = re.compile('(?:' + ca.rc(m1s, r=1) + '){e<=2}')
p_rc_cut = re.compile('(?:' + ca.rc(m1s[-11:], r=1) + '){e<=2}')



if __name__ == '__main__':
    filename = "/home/anton/BigMac/skoltech/CRISPR_research/data/cdif_11_12_bc/assembled/-merged.assembled_1000.fastq"
    reads_bc_path = None
    tag = 'cdif'
    workers = 6

    if reads_bc_path is None:
        reads, quals = ca.read_fastq(filename)
        if DEBUG: print(len(reads))

        def process_batch_mp(batch):
            return process_batch(batch, p_cut)

        reads_batches = [reads[idxs[0]: idxs[1]] for idxs in get_splits(len(reads), workers)]

        if DEBUG: print([len(x) for x in reads_batches])

        reads_bc_list = mp_map(process_batch_mp, reads_batches, workers)

        reads_bc = {}
        for reads_bc_batch in reads_bc_list:
            for k,v in reads_bc_batch.items():
                if k in reads_bc:
                    reads_bc[k] += v
                else:
                    reads_bc[k] = v

    else:
        reads_bc = pickle.load(open(filename, 'rb'))

    pickle.dump(reads_bc, open("./reads_bc_" + tag))


    def split_read_rc(read, patter):
        spacers = ca.split_read(ca.rc(read, r=1), 'Z' * len(read), ca.redundant)#.reverse_complementary())
        inv = 0
        if spacers[0] == -1 or spacers[1] == -1:
            spacers = ca.split_read(v[0], 'Z' * len(v), ca.redundant.reverse_complementary())



    reads_splited = {}
    for k, v in tqdm(reads_bc.items()):
        reads_splited[k] = ca.split_read(v[0], 'Z' * len(v), ca.redundant.reverse_complementary())
