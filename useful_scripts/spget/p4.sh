path="$1"out/

mkdir -p "$path"pairs
mkdir -p "$path"spacers

zcat "$path"clostr_spacers.filtered.25_60.gz | awk '{ FS = "\t" } {print $24 >> $1"_spacers.txt"}'
zcat "$path"clostr_spacers.filtered.25_60.gz | awk -F "\t" 'a[$2]++&&($31 == old[$1]+1){print sp[$1], $24 >> $1"_pairs.txt" }{old[$1]=$31; sp[$1]=$24}'

mv *pairs* "$path"pairs/
mv *spacers* "$path"spacers/
