#!/bin/bash

module load python3.9-anaconda/2021.11
module load cuda/11.8.0 
module load cudnn/11.8-v8.7.0 

export PATH="/nfs/turbo/umms-maom/mdolo/opt/ColabFold/localcolabfold/colabfold-conda/bin:$PATH"
