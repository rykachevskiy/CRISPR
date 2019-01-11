import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys
from importlib import reload
import regex as re
import pickle
import argparse

import crispr_assembler as ca

sys.path.append("../utils")
from misc import *
#from ..utils.misc import *


DEBUG = 1

m1s = 'AAGCAGTGGTATCAACGCAGAGT'
p = re.compile('(?:' + m1s + '){e<=2}')
p_cut = re.compile('(?:' + m1s[-11:] + '){e<=2}')
p_rc = re.compile('(?:' + ca.rc(m1s, r=1) + '){e<=2}')
p_rc_cut = re.compile('(?:' + ca.rc(m1s[-11:], r=1) + '){e<=2}')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run error correction on pairs')

    parser.add_argument('--fn', dest='filename', required=True)
    parser.add_argument('--reads_bc_path', dest='reads_bc_path', default=None)
    parser.add_argument('--workers', dest='workers', type=int, default=6)
    parser.add_argument('--save_path', dest='save_path')

    args = parser.parse_args()

    # filename = "/home/anton/BigMac/skoltech/CRISPR_research/data/cdif_11_12_bc/assembled/-merged.assembled.fastq"
    # reads_bc_path = None
    # tag = 'cdif'
    # workers = 6

    if args.reads_bc_path is None:
        reads, quals = ca.read_fastq(args.filename)
        if DEBUG: print(len(reads))

        def process_batch_mp(batch):
            return process_batch(batch, p_cut)

        reads_batches = [reads[idxs[0]: idxs[1]] for idxs in get_splits(len(reads), args.workers)]

        if DEBUG: print([len(x) for x in reads_batches])

        reads_bc_list = mp_map(process_batch_mp, reads_batches, args.workers)

        reads_bc = {}
        for reads_bc_batch in reads_bc_list:
            for k,v in reads_bc_batch.items():
                if k in reads_bc:
                    reads_bc[k] += v
                else:
                    reads_bc[k] = v

    else:
        reads_bc = pickle.load(open(args.filename, 'rb'))

    # pickle.dump(reads_bc, open(args.save_path + "/reads_bc", 'wb'))
    #
    #
    # reads_bc_list = []
    # for k,v in reads_bc.items():
    #     reads_bc_list.append((k, v))
    #
    #
    # reads_splited = []
    # for k, v in tqdm(reads_bc_list):
    #     reads_splited.append((k, ca.split_read(v[0], ca.redundant)[0]))


    # reads_splited = {}
    # for k, v in tqdm(reads_bc.items()):
    #     reads_splited[k] = ca.split_read(v[0], ca.redundant)[0]
    #
    # pickle.dump(reads_splited, open(args.save_path + "/reads_splited", 'wb'))
    #
    # reads_splited_list = []
    # for k,v in reads_splited.items():
    #


