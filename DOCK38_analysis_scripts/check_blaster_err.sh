#!/bin/bash

# this script just checks and prints out the directories (proteins) for which the blastermaster step in the DOCK38 pipeline failed
for dir in *dock*/*prepared_struct/dockfiles
do
	cd $dir
	if [ -f "INDOCK" ];
	then
		echo "successful"
		cd ../../../
	else 
		echo "$dir unsuccessful"
		cd ../../../
	fi
done

