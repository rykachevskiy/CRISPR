#!/bin/bash

default_path="/home/anton/BigMac/skoltech/CRISPR_research/minnn/"
minnn="/home/anton/BigMac/skoltech/CRISPR_research/minnn/minnn-1.0.0/minnn.jar"

inp_path="$default_path/data/inp/"
out_path="$default_path/data/out/"


echo "$inp_path"

java -jar "$minnn" extract --input "$inp_path"test2_R1.fastq "$inp_path"test2_R1.fastq --pattern "^at(BC1:NNNN)\*" --output "$out_path"mif/extracted.mif --oriented

java -jar "$minnn" correct --groups BC1 --input "$out_path"mif/extracted.mif --output "$out_path"mif/corrected.mif

java -jar "$minnn" demultiplex --by-barcode  BC1 "$out_path"mif/corrected.mif

for file in "$out_path"mif/*.mif; do
	java -jar "$minnn" mif2fastq --input "$file" --group-R1 "$out_path"fastq/"$(basename $file)".fastq
	gzip  "$out_path"fastq/"$(basename $file)".fastq #--group-R2 "$path"out2.fastq
done

# java -jar "$minnn" correct --input "$path"out.mif --output "$path"corrected.mif --groups SB1 # SB2

# java -jar "$minnn" sort --input "$path"corrected.mif --output "$path"sorted.mif --groups SB1 # SB2

# java -jar "$minnn" consensus --input "$path"sorted.mif --output "$path"consensus.mif --max-consensuses-per-cluster 100 --groups SB1 --trim-window-size 5 --reads-trim-window-size 0
#  # SB2




# minnn extract --pattern "^(UMI:N{6})\*" --input data-R1.fastq data-R2.fastq --output extracted.mif
# minnn correct --groups UMI --input extracted.mif --output corrected.mif
# minnn demultiplex --by-sample umi_samples.txt corrected.mif