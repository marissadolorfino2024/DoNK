#!/bin/usr/python

import sys
import glob
import os

# script to get the contigs for diffusion on scaffold backbones
# writes a seq_contig.txt file and a tasks.txt file for use in partialdiffusion script

# path to directory that contains fasta files for the scaffold proteins
fasta_dir = sys.argv[1]

pwd = os.getcwd()

lengths_file = pwd + '/seq_contigs.txt'
tasks_file = pwd + '/tasks.txt'

os.chdir(fasta_dir)
fasta_dir = os.getcwd()

for fasta_file in glob.glob("*.fasta"):
    pdbfile = fasta_file[:-6]
    with open(fasta_file, 'r') as fasta:
        lines = fasta.readlines()

    seq_len = 0
    for i in range(len(lines)):
        if i % 2 == 0:
            chain_id = str(lines[i].split()[0])
            chain_id = list(chain_id)[-1]
            chain_res = str(lines[i+1].split()[0])
            chain_len = len(chain_res)
            seq_len += chain_len

    with open(tasks_file, 'a+') as tasks:
        tasks.write(str(fasta_dir + '/' + pdbfile))
        tasks.write("\n")
    
    with open(lengths_file, 'a+') as lengths:
        lengths.write(str(seq_len))
        lengths.write("\n")

os.chdir(pwd)
