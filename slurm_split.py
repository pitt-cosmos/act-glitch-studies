"""This script splits a task to multiple slurm jobs and submit them"""
from jinja2 import Environment
import os
import math

# Define slurm script
slurm_template='''#!/bin/sh 
#SBATCH -N 1                               # nodes=1 
#SBATCH --ntasks-per-node=1                # ppn=6 
#SBATCH -J {{ name }}                      # job name 
#SBATCH -t 90:00:00                        # 90 hours walltime
#SBATCH --mem=8000MB                       # memory in MB 
#SBATCH --output={{ logfile }}            # file for STDOUT 
#SBATCH --mail-user={{ email }}           # mail id of the user


python {{ script }} {{ opts }}
'''

def generate_bash(name, script, options, enum=0):
    """Generate bash based on the template"""
    compiled = Environment().from_string(slurm_template).render(
        name = name,
        logfile = "logs/%s_%d.log" % (name, enum),
        script = script,
        email = "yig20@pitt.edu",
        opts = options
    )
    print '[INFO] Compiling with options:', options
    filename = generate_file(compiled, name, enum)
    return filename

def generate_file(bash, name, enum):
    """Generate bash file based on string"""
    filename = "%s_%d.sh" % (name, enum)
    print '[INFO] Writing %s' % filename
    with open(filename, "w") as f:
        f.write(bash)
    return filename

def delete_files(list_of_files):
    """Delete files based on a list of filenames in current folder"""
    for f in list_of_files:
        print "[INFO] Running: rm %s" % f
        os.system("rm %s" % f)        

def generate_parameters_2d(start, end, n):
    """Generate list of parameters based on start, end, and number"""
    step = int(math.ceil((end-start)*1.0/n))
    print '[INFO] Choosing a step of %d' % step
    parameters = []
    for i in range(n):
        _start = start + i*step
        _end = min(_start + step, end)
        entry = "%d %d" % (_start, _end)
        parameters.append(entry)
    return parameters

def run_bash(list_of_filenames):
    for f in list_of_filenames:
        print '[INFO] Running qsub %s' % f
        os.system("qsub %s" % f)

if __name__ == "__main__":
    #parameters = generate_parameters_2d(0, 16167, 80)
    parameters = generate_parameters_2d(0, 14782, 80)
    #parameters = generate_parameters_2d(0, 8175, 50)
    #name = "cs_finder"
    #script = "compile_glitch_cuts_all.py"
    #script = "coincident_signals_clean.py"
    #name = "get_tracks"
    #script = "get_tracks.py"
    #name = "get_cut"
    #script = "coincident_signals_subset.py"
    name = "get_tracks"
    script = "get_tracks_db.py"
    filenames = []
    for i, p in enumerate(parameters):
        filenames.append(generate_bash(name, script, p, i))
    
    # run bash
    run_bash(filenames)

    # clean bash
    delete_files(filenames)
