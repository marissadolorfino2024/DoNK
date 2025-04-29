#!/bin/bash

# spacing is sometimes weird with PDB files when the coordinate is negative
# this script iterates through all of the PDB files in a directory and fixes this problem by adding an initial space
# this script should be run if the pdb produces errors during protein design or protein preparation within DOCK (blaster master step)

for pdb in *.pdb;
do
	sed -i 's/-/ -/g' $pdb # it could also be the case that the fix might be: sed -i 's/ -/-/g'... it is pretty case dependent and I haven't found a good way to check yet
done
