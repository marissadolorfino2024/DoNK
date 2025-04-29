#!/bin/python

import os
import sys
import tempfile
import torch
import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim
import torch.multiprocessing as mp

from torch.nn.parallel import DistributedDataParallel as DDP

# set up for distributed data parallel training
def setup(rank, world_size):
    os.environ['MASTER_ADDR'] = os.getenv('SLURM_NODELIST').split()[0] # set the rank will act as the master processor (GPU?)
    os.environ['MASTER_PORT'] = '12355' # open port (must check with 'netstat -tuln | grep 12355' first. if no results, port is available)

    # initialize the process group
    dist.init_process_group("gloo", rank=rank, world_size=world_size) # gloo is an alternative framework to MPI but behaves similarly 

# cleanup for distributed data parallel training
def cleanup():
    dist.destroy_process_group() # free processors
    
