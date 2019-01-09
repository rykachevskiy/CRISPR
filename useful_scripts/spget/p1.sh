path="$1"


mkdir -p "$path"out/

echo "$path"

ls $path

for file in "$path"*fastq.gz; do
    echo "$file"
done
 
for file in "$path"gz/*fastq.gz; do

    #base=`echo "$file"| cut -f 2 -d '/' | perl -pe 's/\.fastq\.gz$//'`

    #echo "$file" | sed -r "s/.+\/(.+)\..+/\1/"

    #echo "$base"
    base=$(basename $file)

    zcat "$file" |  perl -e '
    my $cnt = 0;
    while (my $str = <STDIN>) {
        chomp $str;
        $cnt++;
        my $mod = $cnt % 4;
        if ($mod == 1) { print "'"$base"'\t"};
        if ($mod == 1 || $mod == 2 ) { print "$str\t"};
        if ($mod == 0 ) { print "$str\n"};
    }
'

done | gzip - > "$path"out/raw_data_clostr.gz

