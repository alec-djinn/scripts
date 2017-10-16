#!/hpc/local/CentOS7/common/lang/python/3.6.1/bin/python3
#$ -l h_rt=48:00:00,h_vmem=8G
#$ -pe threaded 1
#$ -S /hpc/local/CentOS7/common/lang/python/3.6.1/bin/python3
#$ -cwd
#$ -M a.marcozzi@umcutrecht.nl
#$ -m beas
#$ -v PATH

from subprocess import run, check_output

with open('test_env.txt', 'w') as f:
        out = check_output(f'lastal -h', shell=True).decode('UTF-8')
        f.write(out)