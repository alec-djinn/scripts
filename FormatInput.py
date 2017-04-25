
def find(string, char):
	'''Looks for a character in a sctring and retrurns its indes.'''
	return [index for index, letter in enumerate(string) if letter == char]


complete_tags_list = ['ID', 'Name', 'Parent', 'var_origin', 'Start_range', 'End_range', 'clinical_int', 'copy_number', 'validated', 'validated_2', 'samples', 'phenotype', 'phenotype_id', 'var_type']
infile = "input.txt"
with open(infile) as f:
	lines = f.readlines()

print 'found',len(lines), 'lines'



with open("output.txt", 'w') as outfile:
	first_line = ""
	for item in complete_tags_list:			
		first_line += item + "\t"
	print first_line
	outfile.write(first_line + '\n')
   
	# divedes the line in two string at the TAB
	# the first string contains the tags and the second the data
	for line in lines:
		# find the TAB index
		tab_index = find(line, '\t')[0]
		print
		tags_string = line[:tab_index].rstrip().rstrip(",")
		data_string = line[tab_index+1:].rstrip().rstrip(",")
		print tags_string
		print data_string
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
			data_list.append(data_string[n:index])
			n = index + 1
		data_list.append(data_string[n:])	
		print data_list

		# # check for the longest list
		# # run it just once to determine the longest tags list then assign it to complete_tags_list
		# if len(tags_list) > len(longest_list):
		# 	longest_list = tags_list

		# Format tags and data
		n = 0
		correct_data = []
		for item in complete_tags_list:
			if item in tags_list:
				correct_data.append(data_list[n])
				n += 1
			else:
				correct_data.append('None')

		# Checks for known errors		
		if correct_data[-3] == 'Unknown' and correct_data[-1] == 'Developmental Delay and additional significant developmental and morphological phenotypes referred for genetic testing':
			correct_data[-3] = 'Developmental Delay and additional significant developmental and morphological phenotypes referred for genetic testing'
			correct_data[-1] = 'Unknown'
		if correct_data[-1] == 'Developmental Delay and additional significant developmental and morphological phenotypes referred for genetic testing' and 'ISCA' in correct_data[-3]:
			correct_data[-4] = correct_data[-3].rstrip('%2CUnknown')
			correct_data[-3] = 'Developmental Delay and additional significant developmental and morphological phenotypes referred for genetic testing'
			correct_data[-1] = 'None'
		print correct_data

		final_data_line = ""
		for item in correct_data:			
			final_data_line += item + "\t"



		 
		print final_data_line
		outfile.write(final_data_line + '\n')



	

