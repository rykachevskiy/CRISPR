#!/bin/bash

default_path="/home/anton/BigMac/skoltech/CRISPR_research/minnn/"
out_path="$default_path/data/out/"


for file in "$out_path"mif/*; do
	rm "$file"
done
for file in "$out_path"fastq/*; do
	rm "$file"
done

# java -jar "$minnn" correct --input "$path"out.mif --output "$path"corrected.mif --groups SB1 # SB2

# java -jar "$minnn" sort --input "$path"corrected.mif --output "$path"sorted.mif --groups SB1 # SB2

# java -jar "$minnn" consensus --input "$path"sorted.mif --output "$path"consensus.mif --max-consensuses-per-cluster 100 --groups SB1 --trim-window-size 5 --reads-trim-window-size 0
#  # SB2




# minnn extract --pattern "^(UMI:N{6})\*" --input data-R1.fastq data-R2.fastq --output extracted.mif
# minnn correct --groups UMI --input extracted.mif --output corrected.mif
# minnn demultiplex --by-sample umi_samples.txt corrected.mif