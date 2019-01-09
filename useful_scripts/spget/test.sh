config_file=$1

echo "$1"

username="$( jq -r '.username' "$config_file" )"

echo "$username"
