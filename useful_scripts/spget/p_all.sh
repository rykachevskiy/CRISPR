config_file=$1

echo using config "$config_file" as config

path="$( jq -r '.path' "$config_file" )"
primer="$( jq -r '.primer' "$config_file" )"
spget="$( jq -r '.spget' "$config_file" )"

echo "$path"
 
echo start 1 $path
./p1.sh $path
echo start 2
./p2.sh $path $primer $spget
echo start 3
./p3.sh $path
echo start 4
./p4.sh $path
