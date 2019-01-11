import sys
import os

import regex as re
import pickle
import argparse

import crispr_assembler as ca

sys.path.append("../utils")
from misc import *
#from ..utils.misc import *


DEBUG = 0

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
    parser.add_argument('--b_type', dest='bacteria_type', default='c')

    args = parser.parse_args()
    # args = parser.parse_args(['--fn',
    #                           "/home/anton/BigMac/skoltech/CRISPR_research/data/cdif_11_12_bc/assembled/-merged.assembled_1000.fastq",
    #                           '--workers',
    #                           '6',
    #                           '--save_path',
    #                           '/home/anton/BigMac/skoltech/CRISPR_research/data/cdif_11_12_bc/bc_res'])

    if args.bacteria_type == 'c':
        default_repeat = ca.redundant
    elif args.bacteria_type == 'e':
        default_repeat = ca.ecoli_r2


    reads, quals = ca.read_fastq(args.filename)
    if DEBUG: print(len(reads))

    def process_read(read):
        bc, read_cut, read, inv = extract_read_bc(read, p_cut, search_rc=1)
        if bc != -1:
            spacers, qualities, inv_split = ca.split_read(read_cut, default_repeat)
            if spacers[0] != -1 and spacers[1] != -1 and len(spacers[0]) > 0:
                return bc, spacers, inv, inv_split
        return -1, [-1,-1], -1, -1

    reads_bc = mp_imap(process_read, reads, args.workers)

    if DEBUG: print(len(reads_bc))

    reads_bc = [x for x in reads_bc if x[0] != -1]

    if DEBUG: print(len(reads_bc))
    if DEBUG: print(reads_bc)


    if not os.path.exists(args.save_path):
        os.makedirs(args.save_path)

    pickle.dump(reads_bc, open(args.save_path + "/reads_bc", 'wb'))



