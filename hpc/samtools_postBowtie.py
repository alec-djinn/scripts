#!/hpc/local/CentOS7/common/lang/python/3.6.1/bin/python
#$ -l h_rt=48:00:00,h_vmem=16G
#$ -S /hpc/local/CentOS7/common/lang/python/3.6.1/bin/python
#$ -cwd
#$ -M a.marcozzi@umcutrecht.nl
#$ -m beas


from subprocess import run


#Use samtools view to convert the SAM file into a BAM file. BAM is the binary format corresponding to the SAM text format. Run:
#samtools view -bS eg2.sam > eg2.bam

bin = '/hpc/local/CentOS7/cog/software/samtools-1.3/'
tool = 'samtools'
_in  = '/hpc/cog_bioinf/kloosterman/users/amarcozzi/FR11122098/FR11122098_grch38.sam'
_out = _in.replace('.sam','.bam')

cmd = '{}{} view -bS {} -o {}'.format(bin,tool,_in,_out)

run(cmd, shell=True)


#Use samtools sort to convert the BAM file to a sorted BAM file.
#samtools sort eg2.bam -o eg2.sorted.bam
_in2  = _out
_out2 = _in2.replace('.bam','.sorted.bam')

cmd2 = '{}{} sort {} -o {}'.format(bin,tool,_in2,_out2)
run(cmd2, shell=True)
