


def find(string, char):
	'''Looks for a character in a sctring and retrurns its indes.'''
	return [index for index, letter in enumerate(string) if letter == char]

def line_to_list(line, char):
	'''Makes a list of string out of a line. Splits the word at char.'''
	
	split_indexes = find(line, char)
	list_ = []
	n = 0
	for index in split_indexes:
		list_.append(line[n:index])
		n = index + 1
	list_.append(line[n:])	
	return list_

def compare(list1, list2):
	'''Compare two list and returns truw if the two list contains the same items.
	Return False otherwise'''
	if list1 == list2:
		return True
	else:
		return False

def item_to_item(list1, item1_index, list2, item2_index):
	'''Takes the value of item1 in list1 and assign item2 in list2 to that value'''
	list2[item2_index] = list1[item1_index]

with open(original_file) as infile:
	lines = infile.readlines()
	list_0 = []
	for line in lines:
		if '#' not in line: # skip comments
		#new_line = line[:-1] # to remove the \n char
		list_0.append(line_to_list(new_line, '\t'))

with open(failed_conversions) as infile:
	lines = infile.readlines()
	list_1 = []
	for line in lines:
		if '#' not in line: # skip comments
		#new_line = line[:-1] # to remove the \n char
		list_1.append(line_to_list(new_line, '\t'))


with open('outpu.txt', 'w') as outfile:
	for item_0 in list_0:
		for item_1 in list_1:
			if item_0[6] != item_1[1]:
				line_to_write = item_0[0]
				outfile.write(line_to_write + '\n')
		


