from pyensembl import EnsemblRelease

genome = EnsemblRelease(75)
genes_dict = dict()
intervals_dict = {'6' :[13200000, 28870000, 29930000, 102850000, 155350000],
				  '11':[93170000],
				  'Y' :[],
				  '10':[90960000],
				  '19':[],
				  '9' :[21830000, 21970000, 21980000, 22360000, 22810000],
				  '2' :[43450000, 49870000, 116380000, 130830000],
				  '3' :[123600000, 149890000, 165240000, 186380000],
				  '5' :[1050000],
				  '13':[],
				  '1' :[23410000, 180640000],
				  '14':[59230000],
				  '18':[28340000],
				  'X' :[11740000],
				  '20':[],
				  '16':[],
				  '17':[],
				  '7' :[47870000, 54800000, 55230000, 55240000, 55250000],
				  '22':[29070000],
				  '4' :[60000, 191040000],
				  '21':[],
				  '12':[9730000, 22320000, 28560000],
				  '15':[35410000, 41860000],
				  '8' :[3620000, 18770000, 70690000, 128750000, 132260000, 135090000]
				  }


for chromosome in intervals_dict:
	genes_dict.update({chromosome:[]})
	for interval in intervals_dict[chromosome]:
		genes = genome.gene_names_at_locus(contig=chromosome, position=interval-10000, end=interval)
		if len(genes) > 0:
			for gene in genes:
				if str(gene) not in genes_dict[chromosome]:
					genes_dict[chromosome].append(str(gene))

for key in genes_dict:
	if len(genes_dict[key]):
		print('---------------------------')
		print('Genes in chromosome',key)
		for item in genes_dict[key]:
			print(item)
