#!/bin/usr/python

import pymol.cmd as cmd
import sys
import glob

des = sys.argv[1]

# script to align designed receptors to the corresponding scaffold protein (to place a ligand in the designed pocket for docking)

# function get the name of the ligand from the reference pdb file
def get_lig(file):
    with open(file, 'r') as pdbf:
        lines = pdbf.readlines()

    ligs = set()
    for line in lines:
        if line[0:6] == 'HETATM':
            lig = line[17:20]
            if lig in ['SEP', 'TPO', 'SCS', 'CAS']:
                continue
            else:
                ligs.add(lig)


    lig = list(ligs)[0]
    if lig[0] == ' ':
        lig = lig[1:]
    elif lig[2] == ' ':
        lig = lig[:2]
    else:
        lig = lig

    return str(lig)

# for each designed pdb file in the directory, align the designed receptor with the reference, then delete reference protein (but keep ligand))
try:
    ref_name = des.split('prepped_formatted')[0] + 'prepped_formatted.pdb'
    ref = '/nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1/scaffolds/prepped_formatted_scaffolds/'+ref_name

    lign = get_lig(ref)
    
    cmd.load(des, object='des_ob')
    cmd.load(ref, object='ref_ob')

    # print(cmd.get_object_list(selection='(all)')) # print the currently loaded objects
    
    cmd.align('des_ob', 'ref_ob')

    selection_string = f'ref_ob and (not resn {lign})'
    cmd.select('to_remove', selection_string) 
    cmd.remove('to_remove')
    
    aligned_design = des[:-4]+'_aligned.pdb'
    cmd.save(aligned_design)
except:
    print(f'failed for receptor: {des}')
