#!/bin/python
#$ -l h_rt=48:00:00,h_vmem=32G
#$ -pe threaded 8
#$ -S /bin/python
#$ -cwd
#$ -M a.marcozzi@umcutrecht.nl
#$ -m beas

from __future__ import print_function, division
from subprocess import call
import glob

def list_of_files(path, extension):
    '''
    Return a list of filepath for each file into path with the target extension.
    '''
    return glob.glob(str(path + '/*.' + extension))

root_folder   = '/hpc/cog_bioinf/kloosterman/users/amarcozzi'
sample_folder = 'FR11122077'#98 #77

paths = list_of_files('{}/{}'.format(root_folder,sample_folder), 'fastq')

reads1 = ''.join(sorted(['{},'.format(f) for f in paths if '_R1_' in f])).replace(' ','')
reads2 = ''.join(sorted(['{},'.format(f) for f in paths if '_R2_' in f])).replace(' ','')

#print(reads1)
#print()
#print(reads2)

bin  = '/hpc/cog_bioinf/kloosterman/tools/bowtie2/'
tool = 'bowtie2'
arg1 = '-p 8' #8 cores, must be the same as -pe option in the header
arg2 = '-x GRCh38_index'
arg3 = '-1{}'.format(reads1)
arg4 = '-2{}'.format(reads2)
arg5 = '-S {}_grch38.sam'.format(sample_folder)


cmd = '{}{}'.format(bin,tool)
#print(cmd)
call([cmd, arg1, arg2, arg3, arg4, arg5])
