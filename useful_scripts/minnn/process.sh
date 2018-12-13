#!/bin/bash

minnn="/home/anton/BigMac/skoltech/CRISPR_research/minnn/minnn-1.0.0/minnn.jar"
path="../data/"

java -jar "$minnn" extract --input "$path"test2_R1.fastq "$path"test2_R1.fastq --pattern "^(SB1:AANNNN)\*" --output "$path"out.mif

java -jar "$minnn" correct --input "$path"out.mif --output "$path"corrected.mif --groups SB1 # SB2

java -jar "$minnn" sort --input "$path"corrected.mif --output "$path"sorted.mif --groups SB1 # SB2

java -jar "$minnn" consensus --input "$path"sorted.mif --output "$path"consensus.mif --max-consensuses-per-cluster 100 --groups SB1 --trim-window-size 5 --reads-trim-window-size 0
 # SB2


for file in "$path"*.mif; do
	java -jar "$minnn" mif2fastq --input "$file" --group-R1 "$path""$(basename $file)".fastq #--group-R2 "$path"out2.fastq
done