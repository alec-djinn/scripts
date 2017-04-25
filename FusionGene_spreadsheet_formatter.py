

col_names = ['ID1', 'ID2', 'ID3', 'C1', 'START_C1', 'END_C1', 'C2', 'START_C2', 'END_C2', 'CNV_TYPE', 'ORIENTATION', 'ORIGIN', 'RECURRENCY']

infile_1 = '/home/amarcozz/Documents/Projects/Fusion Genes/datasets/nonrecdn_hg19_123sv.txt'
outfile_1 = '/home/amarcozz/Documents/Projects/Fusion Genes/datasets/dataset_1.txt'

infile_2 = '/home/amarcozz/Documents/Projects/Fusion Genes/datasets/1KG_123SVformat.txt'
outfile_2 = '/home/amarcozz/Documents/Projects/Fusion Genes/datasets/dataset_2.txt'

infile_3 = '/home/amarcozz/Documents/Projects/Fusion Genes/datasets/ISCA_UCSC_cleaned.txt'
outfile_3 = '/home/amarcozz/Documents/Projects/Fusion Genes/datasets/dataset_3.txt'

infile_4 = '/home/amarcozz/Documents/Projects/Fusion Genes/datasets/DevBreakpoints.txt'
outfile_4 = '/home/amarcozz/Documents/Projects/Fusion Genes/datasets/dataset_4.txt'

def find(string, char):
	'''Looks for a character in a sctring and retrurns its indes.'''
	return [index for index, letter in enumerate(string) if letter == char]

def format_file_1(infile, outfile): #### Works only for the specificated file
	with open(infile) as inf:
		lines = inf.readlines()
	
	with open(outfile, 'w') as outf:
		first_line = ""
		for item in col_names:			
			first_line += item + "\t"
		print first_line
		outf.write(first_line + '\n')
	
		# splits the content of a line into items in a list
		# uses /t as separator
		for line in lines:
			tab_indexes = find(line, '\t')
			data_list = []
			n = 0
			for index in tab_indexes:
				data_list.append(line[n:index])
				n = index + 1
			# add the last line
			data_list.append(line[n:].rstrip('\r\n'))	
			print data_list
			# reorder the data
			reordered_list = []
			reordered_list.append(data_list[0][:-3]) 	# ID1
			reordered_list.append('None') 				# ID2
			reordered_list.append('None')			 	# ID3
			reordered_list.append(data_list[1]) 		# C1
			reordered_list.append(data_list[2]) 		# START_C1
			reordered_list.append(data_list[3]) 		# END_C1
			reordered_list.append(data_list[4]) 		# C2
			reordered_list.append(data_list[5]) 		# START_C2
			reordered_list.append(data_list[6]) 		# END_C2
			if data_list[0][-3:] == 'del':				# CNV_TYPE
				reordered_list.append('DELETION') 		
			elif data_list[0][-3:] == 'dup':
				reordered_list.append('DUPLICATION')
			else:
				reordered_list.append('ERROR')
			reordered_list.append(data_list[7]) 		# ORIENTATION
			reordered_list.append('None') 				# ORIGIN
			reordered_list.append('DE NOVO') 			# RECURRENCY # as the input file specifies

			out_line = ""
			for item in reordered_list:			
				out_line += item + "\t"
			print out_line
			outf.write(out_line + '\n')
#format_file_1(infile_1, outfile_1)

def format_file_2(infile, outfile): #### Works only for the specificated file
	with open(infile) as inf:
		lines = inf.readlines()
	
	with open(outfile, 'w') as outf:
		first_line = ""
		for item in col_names:			
			first_line += item + "\t"
		print first_line
		outf.write(first_line + '\n')
	
		# splits the content of a line into items in a list
		# uses /t as separator
		for line in lines:
			tab_indexes = find(line, '\t')
			data_list = []
			n = 0
			for index in tab_indexes:
				data_list.append(line[n:index])
				n = index + 1
			# add the last line
			data_list.append(line[n:].rstrip('\r\n'))	
			print data_list
			# reorder the data
			reordered_list = []
			reordered_list.append('None')			 	# ID1
			reordered_list.append('None') 				# ID2
			reordered_list.append('None')			 	# ID3
			reordered_list.append(data_list[0]) 		# C1
			reordered_list.append(data_list[1]) 		# START_C1
			reordered_list.append(data_list[2]) 		# END_C1
			reordered_list.append(data_list[3]) 		# C2
			reordered_list.append(data_list[4]) 		# START_C2
			reordered_list.append(data_list[5]) 		# END_C2
			reordered_list.append(data_list[7].upper()) # CNV_TYPE		
			reordered_list.append(data_list[6]) 		# ORIENTATION
			reordered_list.append('None') 				# ORIGIN
			reordered_list.append('None') 				# RECURRENCY

			out_line = ""
			for item in reordered_list:			
				out_line += item + "\t"
			print out_line
			outf.write(out_line + '\n')
#format_file_2(infile_2, outfile_2)

def format_file_3(infile, outfile): #### Works only for the specificated file
	with open(infile) as inf:
		lines = inf.readlines()
	
	with open(outfile, 'w') as outf:
		first_line = ""
		for item in col_names:			
			first_line += item + "\t"
		print first_line
		outf.write(first_line + '\n')
	
		# splits the content of a line into items in a list
		# uses /t as separator
		for line in lines[1:]: # skip first line since it contains a header
			tab_indexes = find(line, '\t')
			data_list = []
			n = 0
			for index in tab_indexes:
				data_list.append(line[n:index])
				n = index + 1
			# add the last line
			data_list.append(line[n:].rstrip('\r\n'))	
			print data_list
			# reorder the data
			reordered_list = []
			reordered_list.append(data_list[0])			# ID1
			reordered_list.append(data_list[2])			# ID2
			if 'ISCA' in data_list[10]:
				reordered_list.append(data_list[10].rstrip('2CUnknown').rstrip('%'))			 	# ID3
			else:
				reordered_list.append('None')
			reordered_list.append(data_list[1][3:]) 	# C1 - same as C2, it's a single chromosome event
			reordered_list.append(data_list[4][4:]) 	# START_C1
			reordered_list.append(data_list[4][4:]) 	# END_C1
			reordered_list.append(data_list[1][3:]) 	# C2 - same as C1, it's a single chromosome event
			reordered_list.append(data_list[5][:-4]) 	# START_C2
			reordered_list.append(data_list[5][:-4]) 	# END_C2
			if '1' in data_list[7]:
				reordered_list.append('DELETION') 		# 'CNV_TYPE'
				reordered_list.append('TH') 			# ORIENTATION
			elif '3' in data_list[7]:
				reordered_list.append('DUPLICATION')
				reordered_list.append('HT') 			# ORIENTATION
			else:
				reordered_list.append(data_list[7])
				reordered_list.append('None')	
			
			
			reordered_list.append('None') 				# ORIGIN
			reordered_list.append('None') 				# RECURRENCY

			out_line = ""
			for item in reordered_list:			
				out_line += item + "\t"
			print out_line
			outf.write(out_line + '\n')
#format_file_3(infile_3, outfile_3)

def format_file_4(infile, outfile): #### Works only for the specificated file
	with open(infile) as inf:
		lines = inf.readlines()
	
	with open(outfile, 'w') as outf:
		first_line = ""
		for item in col_names:			
			first_line += item + "\t"
		print first_line
		outf.write(first_line + '\n')
	
		# splits the content of a line into items in a list
		# uses /t as separator
		for line in lines[1:]: # skip first line since it contains a header
			tab_indexes = find(line, '\t')
			data_list = []
			n = 0
			for index in tab_indexes:
				data_list.append(line[n:index])
				n = index + 1
			# add the last line
			data_list.append(line[n:].rstrip('\r\n'))	
			print data_list
			# reorder the data
			reordered_list = []
			reordered_list.append('Breackpoint ' + data_list[0]) 	# ID1
			reordered_list.append('Patient ' + data_list[1])		# ID2
			reordered_list.append('None')			 	# ID3
			reordered_list.append(data_list[4]) 		# C1
			reordered_list.append(data_list[5]) 		# START_C1
			reordered_list.append(data_list[6]) 		# END_C1
			reordered_list.append(data_list[7]) 		# C2
			reordered_list.append(data_list[8]) 		# START_C2
			reordered_list.append(data_list[9]) 		# END_C2
			reordered_list.append(data_list[15].upper())	# CNV_TYPE
			reordered_list.append(data_list[10]) 		# ORIENTATION

			reordered_list.append('None')			 	# ORIGIN

			if data_list[14] == 'denovo':				# RECURRENCY
				reordered_list.append('DE NOVO')
			else:
				reordered_list.append(data_list[14].upper())		

			out_line = ""
			for item in reordered_list:			
				out_line += item + "\t"
			print out_line
			outf.write(out_line + '\n')
#format_file_4(infile_4, outfile_4)