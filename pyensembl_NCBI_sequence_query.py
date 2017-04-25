from pyensembl import EnsemblRelease
from Bio import Entrez, SeqIO # obtain DNA sequence from NCBI


#Last available version
NCBI_IDS = {'1':"NC_000001", '2':"NC_000002",'3':"NC_000003",'4':"NC_000004",
           '5':"NC_000005",'6':"NC_000006",'7':"NC_000007", '8':"NC_000008",
           '9':"NC_000009", '10':"NC_000010", '11':"NC_000011", '12':"NC_000012",
           '13':"NC_000013",'14':"NC_000014", '15':"NC_000015", '16':"NC_000016", 
           '17':"NC_000017", '18':"NC_000018", '19':"NC_000019", '20':"NC_000020",
           '21':"NC_000021", '22':"NC_000022", 'X':"NC_000023", 'Y':"NC_000024"}


#GRCh37 from http://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.25/#/def_asm_Primary_Assembly
NCBI_IDS_GRCh37 = { 'NC_000001.10','NC_000002.11','NC_000003.11','NC_000004.11',
					'NC_000005.9','NC_000006.11','NC_000007.13','NC_000008.10',
					'NC_000009.11','NC_000010.10','NC_000011.9','NC_000012.11',
					'NC_000013.10','NC_000014.8','NC_000015.9','NC_000016.9',
					'NC_000017.10','NC_000018.9','NC_000019.9','NC_000020.10',
					'NC_000021.8','NC_000022.10','NC_000023.10','NC_000024.9'}
					

data = EnsemblRelease(75, auto_download=True)

_genes = data.genes(contig=1, strand=None)

list_of_genes = _genes[:10]

for item in list_of_genes:
	#Gene(id=ENSG00000196188, name=CTSE, biotype=protein_coding, location=1:206317459-206332104)
	
	_data     = str(item).replace(')','').split(',')
	_id       = _data[0].split('=')[-1]
	_name     = _data[1].split('=')[-1]
	_biotype  = _data[2].split('=')[-1]
	_location = _data[3].split('=')[-1]

	_chr, _ss = _location.split(':')
	_start, _stop = _ss.split('-')

	print(_name,_chr,_start,_stop)

	try:
		Entrez.email = "A.E.vanvlimmeren@students.uu.nl"     # Always tell NCBI who you are
		handle = Entrez.efetch(	db="nucleotide", 
								id=NCBI_IDS[_chr], 
								rettype="fasta", 
								strand=1, 
								seq_start=int(_start), #this is to obtain actual start coordinates from the index
								seq_stop=int(_stop)
							  ) # this is the end of the chromosome
		record = SeqIO.read(handle, "fasta")
		handle.close()
		sequence = record.seq

		print(_name)
		print(sequence)
	except ValueError:
		print('ValueError: no sequence found in NCBI')
