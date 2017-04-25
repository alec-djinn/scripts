
infile = '/home/amarcozz/Documents/Projects/Fusion Genes/datasets/ISCA_UCSC_missing.txt'
outfile = '/home/amarcozz/Documents/Projects/Fusion Genes/datasets/dataset_4b.txt'

def find(string, char):
	'''Looks for a character in a sctring and retrurns its indes.'''
	return [index for index, letter in enumerate(string) if letter == char]

def format_Tags_Vals(infile, outfile):
	with open(infile) as inf:
		lines = inf.readlines()

	with open(outfile, 'w') as outf:
			
		startline = 1840
		list_of_dict = []

		for line in lines:
			tab_index = find(line, '\t')
			tags_string = line[:tab_index[0]].rstrip(',').rstrip('\n')
			data_string = line[tab_index[0]+1:].rstrip(',').rstrip('\n')

			# divides each strings in list of strings. The comma is the separator.
			tags_indexes = find(tags_string, ",")
			data_indexes = find(data_string, ",")
			print tags_indexes
			print data_indexes
			tags_list = []
			data_list = []
			
			n = 0
			for index in tags_indexes:
				tags_list.append(tags_string[n:index])
				n = index + 1
			tags_list.append(tags_string[n:])	
			print tags_list

			n = 0
			for index in data_indexes:
				data_list.append(data_string[n:index].replace('%2C','').replace('.',''))
				n = index + 1
			data_list.append(data_string[n:])	
			print data_list

			# creates a dictionary for aech line with Tag:Value pairs
			vars()['dict'+ str(startline)] = {}
			for n in range(len(tags_list)):
				vars()['dict'+ str(startline)].update({tags_list[n]:data_list[n]})

			# organizes the dictionaries in a list of dict.
			list_of_dict.append(vars()['dict'+ str(startline)])
			# next line tracker
			startline += 1

		print len(list_of_dict)
		print startline - 1840

		for dic in list_of_dict:
			if dic['var_type'] == 'copy_number_loss':
				orientation = 'TH'
			elif dic['var_type'] == 'copy_number_gain':
				orientation = 'HT'
			else:
				orientation = 'None'
			newline = dic['ID'] + '\t' + dic['Parent'] + '\t' + dic['samples'] + '\t' + dic['var_origin'] + '\t' + dic['Start_range'] + '\t' + dic['End_range'] + '\t' + dic['var_type'] + '\t' + orientation
			print newline
			outf.write(newline + '\n')


format_Tags_Vals(infile, outfile)