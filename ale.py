# My personal colelction of useful functions

__version__ = "0.1"

__help__ = \
'''
Simbol		Read as
->			return
>>			yield
>>>			expected output
infile		input file
outfile		output file
number		int or float
'''



def g4_scanner(sequence):
    '''(str) -> iter, iter
    G-quadruplex motif scanner.
    Scan a sequence for the presence of the regex motif:
        [G]{3,5}[ACGT]{1,7}[G]{3,5}[ACGT]{1,7}[G]{3,5}[ACGT]{1,7}[G]{3,5}
        Reference: http://www.ncbi.nlm.nih.gov/pmc/articles/PMC1636468/
    Return two callable iterators.
    The first one contains G4 found on the + strand.
    The second contains the complementary G4 found on the + strand, i.e. a G4 in the - strand.
    '''
    __version__ = "0.1"
    
    #forward G4
    pattern_f = '[G]{3,5}[ACGT]{1,7}[G]{3,5}[ACGT]{1,7}[G]{3,5}[ACGT]{1,7}[G]{3,5}'
    result_f = re.finditer(pattern_f, sequence)
    #reverse G4
    pattern_r = '[C]{3,5}[ACGT]{1,7}[C]{3,5}[ACGT]{1,7}[C]{3,5}[ACGT]{1,7}[C]{3,5}'
    result_r = re.finditer(pattern_r, sequence)
    
    return result_f, result_r


def check_line(line, skip_lines_starting_with=['#','\n','',' ']):
    '''(str, list) -> bool
    Check if the line starts with an unexpected character.
    If so, return False, else True
    '''
    __version__ = "0.1"

    for item in skip_lines_starting_with:
        if line.startswith(item):
            return False
    return True


def dice_coefficient(sequence_a, sequence_b):
	'''(str, str) -> float
	Return the dice cofficient of two sequences.
	'''
	__version__ = "0.1"

	a = sequence_a
	b = sequence_b
	if not len(a) or not len(b): return 0.0
	# quick case for true duplicates
	if a == b: return 1.0
	# if a != b, and a or b are single chars, then they can't possibly match
	if len(a) == 1 or len(b) == 1: return 0.0
	
	# list comprehension, preferred over list.append() '''
	a_bigram_list = [a[i:i+2] for i in range(len(a)-1)]
	b_bigram_list = [b[i:i+2] for i in range(len(b)-1)]
	
	a_bigram_list.sort()
	b_bigram_list.sort()
	
	# assignments to save function calls
	len_a = len(a_bigram_list)
	len_b = len(b_bigram_list)
	
	# initialize match counters
	matches = i = j = 0
	while (i < len_a and j < len_b):
		if a_bigram_list[i] == b_bigram_list[j]:
			matches += 2
			i += 1
			j += 1
		elif a_bigram_list[i] < b_bigram_list[j]:
			i += 1
		else:
			j += 1
	
	score = float(matches)/float(len_a + len_b)
	return score


def string_to_int(string):
	'''(str) -> int
	Convert a bytes string into a single number.
	'''
	__version__ = "0.1"

	return int.from_bytes(string.encode(), 'little')


def int_to_string(integer):
	'''(int) -> str
	Convert an integer into a bytes string.
	'''
	__version__ = "0.1"

	from math import ceil
	return integer.to_bytes(ceil(integer.bit_length() / 8),'little').decode()


def yield_file(infile):
	'''(file_path) >> line
	A simple generator that yield the lines of a file.
	Good to read large file without running out of memory.
	'''
	__version__ = "0.1"

	with open(infile, 'r') as f:
		for line in f:
			yield line


def read_in_chunks(infile, chunk_size=1024):
	'''(file_path, int) >> str
	Simple generator to read a file in chunks.
	'''
	__version__ = "0.1"

	with open(infile,'r') as f:
		while True:
			data = f.read(chunk_size)
			if not data:
				break
			yield data


def extract_data(infile, 
				 columns=[3,0,1,2,5],
				 header='##',
				 skip_lines_starting_with=['#','\n','',' '],
				 strip_data_containing=['\n', ' '],
				 data_separator='\t',
				 verbose=False ):

	'''(file_path, list, str, list, list, str, bool) -> list_of_tuples
	Extract data from a file.
	Return or Yield a list of tuples. 
	Each tuple contains the data extracted from one line of the file
	in the indicated columns and with the indicated order.
	e.g. using columns=[3,0,1,2,5], it will return items[3,0,1,2,5] of line.split()
	'''
	__version__ = "0.2"

	extracted_data = []
	header_list = []
	header_flag = 0
	line_counter = 0

	for line in yield_file(infile): # Lazely open a file
		line_counter += 1

		if line.startswith(header): # get a clean header
			header_list = line.split(data_separator)
			header_list[0] = header_list[0].replace(header,'')
			header_list[-1] = header_list[-1].strip()
			header_flag += 1
			if header_flag > 1: # there should be only one header
				raise ValueError('More than one line seems to contain the header identificator {} .'\
				                 .format(header))
		
		elif line[0] in skip_lines_starting_with: # skips comments and blank lines
			pass
		
		else:
			tmp = line.split(data_separator) # get all the data
			result = []
			for i in columns: # get only desired columns
				item = tmp[i]
				for char in strip_data_containing: # clean the data
					item = item.replace(char,'')
				result.append(item)
			
			extracted_data.append(tuple(result))

	if verbose: # Prints out a brief report
		print('Data extracted from: {}\nHeader: {}\nTotal lines: {}'\
			  .format(infile, header_list, line_counter))
	
	return extracted_data


def probability(p,n,k):
	'''(number, number, number) -> float
	Simple probability calculator.
	Calculates what is the probability that k events occur in n trials.
	Each event have p probability of occurring once.
	e.g.: What is the probability of having 3 Heads by flipping a coin 10 times?
	probability = prob(0.5,10,3)
	>>> 0.1171875
	'''
	from math import factorial
	p = float(p)
	n = float(n)
	k = float(k)
	C = factorial(n) / ( factorial(k) * factorial(n-k) )
	probability = C * (p**k) * (1-p)**(n-k)
	return probability


def gc_content(sequence,percent=True):
    '''(str,bool) -> float
    Return the GC content of a sequence.
    '''
    sequence = sequence.upper()
    g = sequence.count("G")
    c = sequence.count("C")
    t = sequence.count("T")
    a = sequence.count("A")
    gc_count = g+c
    total_bases_count = g+c+t+a
    gc_fraction = float(gc_count) / total_bases_count
    
    if percent:
        return gc_fraction * 100
    else:
        return gc_fraction
