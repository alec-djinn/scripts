from pyensembl import *
import operator

genome = EnsemblRelease(75, auto_download=True)
input_file = 'All_breakpoints_HG19_final.txt'
output_file = 'broken_genes.txt'
genes_dict = dict()


with open(input_file, 'r') as f:
	with open(output_file, 'w') as out:

		lines = f.readlines()
		for line in lines:
			coordinates = line.strip().replace(':','-').split('-')
			chromosome = coordinates[0][3:]
			breakpoint = int(coordinates[1])
			#print chromosome, breakpoint

			genes = genome.gene_names_at_locus(contig=chromosome, position=breakpoint)
			if len(genes) > 0:
				for gene in genes:
					print(chromosome,breakpoint,str(gene))
					line_to_write = str(chromosome) + '\t' + str(breakpoint) + '\t' + str(gene) + '\n'
					out.write(line_to_write)
					if str(gene) not in genes_dict:
						genes_dict.update({str(gene):1})
					else:
						genes_dict[str(gene)] += 1

#for key in genes_dict:
#	print key, genes_dict[key]
sorted_ = sorted(genes_dict.items(), key=operator.itemgetter(1), reverse=True)
with open('genes_dict_sorted.txt', 'w') as f:
	for item in sorted_:
		f.write(str(item[0])+'\t'+str(item[1])+'\n')

print('len(genes_dict):',len(genes_dict))