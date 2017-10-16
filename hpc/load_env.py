# run this before "qsub -v your_script.py" to setup the environment

from subprocess import run

run('export PATH=/hpc/cog_bioinf/kloosterman/tools/last-869/src:$PATH', shell=True)
run('export PATH=/hpc/cog_bioinf/kloosterman/tools/bowtie2:$PATH', shell=True)
run('export PATH=/hpc/local/CentOS7/cog/bin/poretools:$PATH', shell=True)