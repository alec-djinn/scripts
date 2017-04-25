from subprocess import call
from glob import glob

path = '/Users/amarcozzi/Desktop/BLAST_DB'
extension = 'tar.gz'
n = 0

for file_ in glob(str(path + '/*.' + extension)):
	call(["tar", "zxvpf", file_])
	n += 1

print(n,'files have been extracted in',path)
