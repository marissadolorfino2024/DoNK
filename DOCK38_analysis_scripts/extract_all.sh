#!/bin/sh

# this script runs the extract_all python script from DOCK3.8 on all the dock directories specified 

dock_dir_pattern=$1 ## this should be a string given as the first command line arg when running the script, and should be a pattern matching all the parent directories where you are running each docking run e.g. "dock_2023"
result_dir_pattern=$2 ## this should be a string given as the seccond command line arg when running the script, and should be a pattern matching all the directories within the docking directories when docking actually occurs (where the "dirlist" file is contained) e.g "_ZINC_"

for dir in *${dock_dir_pattern}*/*${result_dir_pattern}*
do
	cd $dir

	python $DOCKBASE/analysis/extract_all_blazing_fast.py ./dirlist extract_all.txt 2000000 # this should be set to a larger value than the number of ligands docked so as to extract all the ligand docking data

	cd ../../
done
