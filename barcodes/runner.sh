#!/bin/bash

reads_path='/home/anton/BigMac/skoltech/CRISPR_research/data/cdif_11_12_bc/assembled/-merged.assembled_1000.fastq'
save_path='/home/anton/BigMac/skoltech/CRISPR_research/data/cdif_11_12_bc/bc_res'

python barcodes.py --fn "$reads_path" --workers 6 --save_path "$save_path"
