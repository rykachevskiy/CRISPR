path='/home/anton/BigMac/skoltech/CRISPR_research/data/clostr_11_12/out/pairs/'

for file in "$path"*; do 
	echo  "$(basename $file)"
	python /home/anton/BigMac/skoltech/CRISPR_research/CRISPR_assembler/src/main/run_greedy_pipeline.py --pairs_path "$path" --pairs_names "$(basename $file)" --save_path /home/anton/BigMac/skoltech/CRISPR_research/data/clostr_11_12/out/restored/ --plot_name "$(basename $file)".pdf --error_threshold 6 --assemble_threshold 0
done
