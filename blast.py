from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import *

# local databases
db_path = '/Users/amarcozzi/Desktop/BLAST_DB/'
human_genomic = db_path + "human_genomic"
nt = db_path + "nt"
# input
sequence_path = '/Users/amarcozzi/Desktop/Scripts/'
fasta_file = sequence_path + 'sequence.fasta'
out_file = "output.xml"
# blastn
blastn_cline = NcbiblastnCommandline(query=fasta_file, db=human_genomic, evalue=0.001, outfmt=5, out=out_file)
print(blastn_cline)
stdout, stderr = blastn_cline()
#parse output
for blast_record in NCBIXML.parse(open(out_file)):
    for alignment in blast_record.alignments:
        for hsp in alignment.hsps:
            print("*****Alignment****")
            print("sequence:", alignment.title)
            print("length:", alignment.length)
            print("e-value:", hsp.expect)
            print(hsp.query)
            print(hsp.match)
            print(hsp.sbjct)


def blastn(input_fasta_file,db_path='/Users/amarcozzi/Desktop/BLAST_DB/',db_name='human_genomic',out_file='blastn_out.xml'):
	'''Runn blastn on the local machine using a local database.
	Requires NCBI BLAST+ to be installed. http://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download
	Takes a fasta file as input and writes the output in an XML file.'''
	from Bio.Blast.Applications import NcbiblastnCommandline
	db = db_path + db_name
	blastn_cline = NcbiblastnCommandline(query=input_fasta_file, db=db, evalue=0.001, outfmt=5, out=out_file)
	print(blastn_cline)
	stdout, stderr = blastn_cline()


def parse_blastXML(infile):
	'''Parses a blast outfile (XML).'''
	from Bio.Blast import NCBIXML
	for blast_record in NCBIXML.parse(open(infile)):
		for alignment in blast_record.alignments:
			for hsp in alignment.hsps:
				print("*****Alignment****")
				print("sequence:", alignment.title)
				print("length:", alignment.length)
				print("e-value:", hsp.expect)
				print(hsp.query)
				print(hsp.match)
				print(hsp.sbjct)

# print('blasting online...')
# #result_handle = NCBIWWW.qblast("blastn", online_dbs[1][0], fasta_string)
# result_handle = NCBIWWW.qblast("blastn", "human_genomic", fasta_string)
# blast_records = NCBIXML.parse(result_handle)
# blast_record = next(blast_records)

# E_VALUE_THRESH = 0.04


# for alignment in blast_record.alignments:
# 	for hsp in alignment.hsps:
# 		if hsp.expect < E_VALUE_THRESH:
# 			print('****Alignment****')
# 			print('sequence:', alignment.title)
# 			print('length:', alignment.length)
# 			print('e value:', hsp.expect)
# 			print(hsp.query[0:75] + '...')
# 			print(hsp.match[0:75] + '...')
# 			print(hsp.sbjct[0:75] + '...')



# from Bio.Blast.Applications import NcbiblastxCommandline
# print('blasting locally...')
# nr = "/Users/Priya/Documents/Python/ncbi-blast-2.2.26+/bin/nr.pal"
# infile = "/Users/Priya/Documents/Python/Tutorials/opuntia.txt"
# blastx = "/Users/Priya/Documents/Python/ncbi-blast-2.2.26+/bin/blastx"
# outfile = "/Users/Priya/Documents/Python/Tutorials/opuntia_python_local.xml"
# blastx_cline = NcbiblastxCommandline(blastx, query = infile, db = nr, evalue = 0.001, out = outfile)
# stdout, stderr = blastx_cline()


# from Bio import SeqIO
# from Bio.Blast import NCBIWWW

# my_query = SeqIO.read("test.fasta", format="fasta") 
# result_handle = NCBIWWW.qblast("blastn", "nt", my_query.seq)
# blast_result = open("my_blast.xml", "w")
# blast_result.write(result_handle.read())
# blast_result.close()
# result_handle.close()


# from Bio.Blast import NCBIXML

# E_VALUE_THRESH = 1e-20
# for record in NCBIXML.parse(open("my_blast.xml")):
# if record.alignments : #skip queries with no matches
#  print "QUERY: %s" % record.query[:60]
#  for align in record.alignments:
#  for hsp in align.hsps:
#  if hsp.expect < E_VALUE_THRESH:
#  print "MATCH: %s " % align.title[:60]
#  print hsp.expect


# from Bio.Blast.Applications import NcbiblastxCommandline
#  blastx_cline = NcbiblastxCommandline(query="Musa_tx.fasta", db="drospep", \
#  evalue=1e-20, outfmt=5, out="my_blast.xml")
# stdout, stderr = blastx_cline()


# more info here http://booksreadr.org/pdf/blast-with-biopython-232678147.html