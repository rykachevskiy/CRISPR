from tqdm import tqdm_notebook
from multiprocessing import Pool
import numpy as np
import regex as re
import crispr_assembler as ca

def extract_read_bc(read, pattern, search_rc=0):
    coords = [x.span() for x in re.finditer(pattern, read)]
    rc = 0
    if len(coords) == 0 and search_rc:
        read = ca.rc(read, r=1)
        coords = [x.span() for x in re.finditer(pattern, read)]
        rc = 1
    if len(coords) != 0:
        bc_start = [x.span() for x in re.finditer(pattern, read)][0][1]
        bc_end = bc_start + 10

        bc = read[bc_start: bc_end]
        read_cut = read[bc_end:]

        return bc, read_cut, read, rc
    else:
        return -1, -1, -1, -1


def process_batch(batch, pattern):
    reads_clusterised = {}
    for r in tqdm_notebook(batch):
        bc, r_cut, r, inv = extract_read_bc(r, pattern, search_rc=1)
        if bc != -1:
            if bc in reads_clusterised:
                reads_clusterised[bc].append(r_cut)
                # print (f'mrgd {bc}')
            else:
                reads_clusterised[bc] = [r_cut]

    return reads_clusterised


def mp_map(func, l, workers=1):
    if workers == 1:
        return list(map(func, l))
    else:
        p = Pool(workers)
        return list(p.map(func, l))


def get_splits(max_idx, n_splits):
    splits = []
    spl = np.linspace(0, max_idx, n_splits + 1, dtype=int)
    for i, j in zip(spl[:-1], spl[1:]):
        splits.append((i, j))

    return splits


def split_read_rc(read, repeat, quality=None):
    if quality is None:
        quality = 'Z' * len(read)

    spacers = ca.split_read(ca.rc(read, r=1), quality, ca.redundant)#.reverse_complementary())
    inv = 0
    if spacers[0] == -1 or spacers[1] == -1:
        spacers = ca.split_read(read, quality, ca.redundant)#.reverse_complementary())
        inv = 1

    if spacers[0] == -1 or spacers[1] == -1:
        return -1,-1,-1
    else:
        
