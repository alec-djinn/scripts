#do not run this with qsub
#this script will call NAP that will qsub all the jobs for you

from __future__ import print_function, division
from subprocess import call


NAP_ROOT = '/hpc/cog_bioinf/kloosterman/tools/NAP_v2.1'
ENV    = 'source {}/env/bin/activate'.format(NAP_ROOT)
NAP    = '{}/nap.py'.format(NAP_ROOT)
INPUT  = '/hpc/cog_bioinf/kloosterman/raw_data/NANOPORE/RCA/AlessioRCAx1'
OUTPUT = '/hpc/cog_bioinf/kloosterman/users/amarcozzi/AlessioRCAx1'
MAIL   = 'alessio.marcozzi@gmail.com'

cmd1   = 'python {} create_ini --ini {}/nap_albacore.ini --input {} --output {} --mail {}'.format(NAP, NAP_ROOT, INPUT, OUTPUT, MAIL)
cmd2   = 'python {} run --settings {}/settings.ini'.format(NAP, OUTPUT)

call('{} && {} && {}'.format(ENV, cmd1, cmd2), shell=True)