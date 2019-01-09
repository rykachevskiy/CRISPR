#path='/home/anton/BigMac/skoltech/CRISPR_research/data/clostr_11_12/out/'
path='/home/anton/BigMac/skoltech/CRISPR_research/data/cdif_11_12/out/'
#path='/home/anton/BigMac/skoltech/CRISPR_research/data/Run28/out/'
#path='/home/anton/BigMac/skoltech/CRISPR_research/data/ecoli_11_12/out/'
#path='/home/anton/BigMac/skoltech/CRISPR_research/data/student_Dvyg/EC/pairs_spget_20/'

for file in "$path"pairs/*; do 
	#echo  "$(basename $file)"
	filename=$(basename -- "$file")
	filename=`echo "$filename" | cut -d'.' -f1`
	save_path="$path"/restored/"$filename"/

	echo "$save_path"

	python /home/anton/BigMac/skoltech/CRISPR_research/crispr_assembler/src/crispr_assembler/main/run_greedy_pipeline.py --pairs_path "$path"pairs/ --pairs_names "$(basename $file)" --save_path "$save_path" --plot_name "$filename".pdf --error_threshold 6 --assemble_threshold 4
done
