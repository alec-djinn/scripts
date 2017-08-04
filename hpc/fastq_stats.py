#!/bin/python
#$ -l h_rt=48:00:00,h_vmem=32G
#$ -pe threaded 8
#$ -S /bin/python
#$ -cwd
#$ -M a.marcozzi@umcutrecht.nl
#$ -m beas

#Compute some basic stats on fastq files made by NAP

from __future__ import print_function, division
from subprocess import call
from os import walk
from glob import iglob
from collections import Counter
import matplotlib

matplotlib.use('Agg') #no display on HPC
import matplotlib.pyplot as plt


path  = '/hpc/cog_bioinf/kloosterman/users/amarcozzi/AlessioRCAx1'

read_length = Counter()
for root, dirs, files in walk(path + '/fastq'):
    for file_path in iglob(root + '/*.fastq'):
        with open(file_path, 'r') as f:
                for line in f:
                        if line[0] not in '+@"\n':
                                read_length.update({len(line)})

call('cd {} && mkdir stats'.format(path), shell=True)

#Plot
#plt.style.use('ggplot')
plt.figure(dpi=100)
for k,v in read_length.iteritems():
         plt.bar(k,v, color='green')
plt.title('Read length distribution')
plt.savefig('{}/stats/read_len_dis.png'.format(path))