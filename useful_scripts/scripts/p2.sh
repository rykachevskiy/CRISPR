#for i in 0 1 2 3; do
path="$1"out/
primers="$2"
spget="$3"

zcat "$path"raw_data_clostr.gz | awk -F "\t" '{OFS="\t"; $2=$2"_"NR; print}'| python "$spget" --primers "$primers" --each 1000 --dump-linked-ids | gzip - > "$path"clostr_spacers.gz
#done
