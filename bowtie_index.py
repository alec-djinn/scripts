#!/bin/python
#$ -S /bin/python
#$ -cwd
#$ -M a.marcozzi@umcutrecht.nl
#$ -m beas


from subprocess import call

bin = '/hpc/cog_bioinf/kloosterman/tools/bowtie2/'
tool = 'bowtie2-build'
arg1 = '/hpc/cog_bioinf/kloosterman/users/amarcozzi/GRCh38/Homo_sapiens_assembly38.fasta'
arg2 = '/hpc/cog_bioinf/kloosterman/users/amarcozzi/GRCh38/GRCh38_index'

cmd = '{}{}'.format(bin,tool)

call([cmd, arg1, arg2])

