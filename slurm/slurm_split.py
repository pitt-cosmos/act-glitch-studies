"""This script splits a task to multiple slurm jobs and submit them"""
from jinja2 import Environment

# Define slurm script
slurm_template='''#!/bin/sh 
#SBATCH -N 1                               # nodes=1 
#SBATCH --ntasks-per-node=1                # ppn=6 
#SBATCH -J {{ name }}                      # job name 
#SBATCH -t 90:00:00                        # 90 hours walltime
#SBATCH --mem=4000MB                       # memory in MB 
#SBATCH --output= {{ logfile }}            # file for STDOUT 
#SBATCH --mail-user= {{ email }}           # Mail id of the user 
#SBATCH --mail-type=end                    # Slurm will send at the completion of your job 

python {{ program }} {{ opts }}
'''
compiled = Environment().from_string(slurm_template).render(
    name = "complie_glitch",
    logfile = "../logs/1.log",
    email = "yig20@pitt.edu",
    program = "find_cuts",
    opts = "0 100"
)
print compiled
