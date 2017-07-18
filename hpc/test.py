#!/bin/python
#$ -S /bin/python
#$ -cwd
#$ -M a.marcozzi@umcutrecht.nl
#$ -m beas

import sys
import time

with open('test_output.txt', 'w') as f:
	f.write(sys.version)
	f.write('\n{}'.format(time.time()))


