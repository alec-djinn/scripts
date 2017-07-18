#!/bin/python
#$ -l h_rt=48:00:00,h_vmem=32G
#$ -pe threaded 8
#$ -S /bin/python
#$ -cwd
#$ -M a.marcozzi@umcutrecht.nl
#$ -m beas

from __future__ import print_function, division
import subprocessl

bin  = '/hpc/cog_bioinf/kloosterman/tools/'
tool = 'muscle3.8.31_i86linux64'
infile  = ''
outfile = ''
cmd = 'muscle -in {} -out {}'.format(infile, outfile)
subprocess.check_call(cmd.split())

