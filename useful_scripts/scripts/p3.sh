path="$1"out/


zcat "$path"clostr_spacers.gz  | awk -F "\t" '$4 == "F" && $5 == 1 && $(23) > 0 && $(27) !~ /[\!\"\#\$\%\&\'"'"'\(\)\*\+\,\-\.\/01234]/ && (NF == 28 && $(25) == 1  || NF == 31 && $(28) == 1)'  | gzip - > "$path"clostr_spacers.filtered.gz



zcat "$path"clostr_spacers.filtered.gz | awk -F "\t" '$(23) >= 25 && $(23)<= 60' | gzip - > "$path"clostr_spacers.filtered.25_60.gz

#56789\:\;\<\=\>\?\@ABCDEFGH]
