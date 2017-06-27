#!/bin/python
#$ -l h_rt=48:00:00,h_vmem=32G
#$ -pe threaded 8
#$ -S /bin/python
#$ -cwd
#$ -M a.marcozzi@umcutrecht.nl
#$ -m beas


from subprocess import call

cmd  = 'gzip'
arg1 = '-d'
arg2 = '-r'
arg3 = 'FR11122098'
call([cmd, arg1, arg2, arg3])
