#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#from __future__ import absolute_import, division, print_function
from collections import OrderedDict
from operator import itemgetter
from datetime import datetime
import os
import glob
import shutil

#DNA to bit {'A':bit(00), C:01, G:10, T:11}


def is_id(line):
	'''str -> bool
	Determine if a line of text contains a sequence _id.
	Return True of False.
	'''
	specials = ['>','<',':','.','_','-','[',']''{','}',
							'0','1','2','3','4','5','6','7','8','9']
	for s in specials:
		if s in line[:50]:
			return True
	return False


def reverse_complement(sequence):
	'''str -> str
	Return the reverse complement of a DNA sequence.
	'''
	sequence = sequence.upper()
	reverse_complement = ''
	n = len(sequence)-1
	while n >= 0:
		if sequence[n] == 'A':
			reverse_complement += 'T'

		elif sequence[n] == 'T':
			reverse_complement += 'A'

		elif sequence[n] == 'C':
			reverse_complement += 'G'

		elif sequence[n] == 'G':
			reverse_complement += 'C'

		elif sequence[n] == 'N':
			reverse_complement += 'N'

		else:
			raise ValueError("sequence is supposed to contain only 'A','T','C','G' and 'N' "+\
							 "but {} was found.".format(sequence[n]))
		n -= 1
	return reverse_complement


def translate_dna(sequence, experiment):
	'''str -> str
	Return the first frame translation of DNA sequence following the experiment rules.
	'''
	sequence = sequence.upper()
	gencode = {
			'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
			'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
			'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
			'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
			'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
			'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
			'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
			'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
			'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
			'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
			'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
			'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
			'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
			'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
			'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
			'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W',
			}

	# if amber mutant
	if experiment in [1,2,3,4]:
		gencode['TAG'] = 'Q'

	proteinseq = ''
	for n in range(0,len(sequence),3):
		if gencode.has_key(sequence[n:n+3]) == True:
			proteinseq += gencode[sequence[n:n+3]]
		else:
			proteinseq += '#'	
	return proteinseq


def parse_seq(text, trim=False):
	'''(text, False/[idx0, idx1]) -> OrderedDict([('_id':'sequence'),...])
	Parse a text looking for biological sequence/s and relative _id/s.
	Return an OrderedDict having _id:sequence as key:value in a FASTA format.
	trim is used to trim the id of a sequence in case the id is too long. trim=[0,10] -> _id = _id[0,10]
	If one ore more id are missing a random id with the 'amof_' suffix will be generated instead.
	'''
	comments = ['/','\\','#']
	blanks   = ['',' ','\t','\n']
	
	_id  = False
	id_counter = 0
	sequence		= None
	input_error = False
	duplicate 	= 0

	d = OrderedDict()

	lines = text.split('\n')
	for line in lines:
		if len(line):
			if line[0] not in (comments+blanks): #skip comments and blanks
				if is_id(line):
					_id = line.strip()
					if trim:
						_id = _id[trim[0]:trim[1]]
					if not _id.startswith('>'):
						_id = '>'+_id
					if _id not in d:
						d.update({_id:''})
					else:
						_id += '_'+duplicate
						duplicate += 1

				else:
					if not _id:
						_id = '>amof_{}'.format(_idcounter)
						d.update({_id:''})
						_idcounter += 1
					sequence = line.strip().replace(' ','').replace('\t','')
					d[_id] += sequence
	return d


def preprocess_from_file(inputfile, experiment, reverse=False, trim=False, verbose=False):
	'''('path', int, bool, bool) -> OrderedDict()
	Read a file containing a list of sequences preceded by a unique sequence id.
	reverse should be set on True if a 'reverse primer' was used for sequencing. <<-Explain better
	trim is used to trim the id of a sequence in case the id is too long. trim=[0,10] -> _id = _id[0,10]
	Remove blank lines.
	Checks if id is unique.
	If verbose: print sequences and stats.
	Precondition: inputfile format is FASTA_like. 
	'''
	infile = inputfile
	d = parse_sequence(open(inputfile,'r').read(),trim=trim)
	count = len(d)
	sequence_dict = OrderedDict()
	corrupted_list = []
	unreadable_list = []
	wildtype_list = []
	
	wildtype = 0
	corrupted = 0
	unreadable = 0

	if verbose:
		print(':::sequences found in {} formatted following rules from experiment #{}\n'.format(infile,str(experiment)))

	for _id in d:
		sequence = d[_id].upper()

		# if PhD-7 and PhD-12
		if experiment == 1 or 2:
			left_flank = 'GTGGTACCTTTCTATTCTCACTCT'
			right_flank = 'GGTGGAGGTTCGGCCGAAACTGTTGAAAGTTGTTTAGCA'
			wild_type = 'GTTGTTCCTTTCTATTCTCACTCCGCTGAAACTGTTGAAAGTTGTTTAGCA'
		
		# if PhD-C7C
		if experiment == 3:
			left_flank = 'GTGGTACCTTTCTATTCTCACTCTGCTTGT'
			right_flank = 'TGCGGTGGAGGTTCGGCCGAAACTGTT'
			wild_type = 'GTACCTTTCTATTCTCACTCGGCCGAAACTGTTGAAAGTTGTTTAGCAAAA'

		# if M13 - p8 N-term display
		if experiment == 4:
			left_flank = 'TTCCGATGCTGTCTTTCGCT'
			right_flank = 'GCTGAGGGTGACGATCCCGCAAA'
			wild_type = 'GTCTTTCGCTGCTGAGGGTGACGATCCCGCAAAAG'
		
		# analyze sequence
		if reverse:
			sequence = reverse_complement_dna(sequence)

		if wild_type in sequence:
			wildtype += 1
			wildtype_list += [_id]
		elif left_flank and right_flank in sequence:
			sequence = sequence[sequence.rfind(left_flank)+len(left_flank):sequence.rfind(right_flank)]
			sequence = translate_dna(sequence, experiment)
			
			if '#' in sequence:
				corrupted += 1
				corrupted_list += [_id]
		else:
			unreadable += 1
			unreadable_list += [_id]

		# save good sequences
		if _id not in corrupted_list:
			if _id not in unreadable_list:
				if _id not in wildtype_list:
					if _id not in sequence_dict:
						sequence_dict[_id] = sequence			
					else:
						sys.exit(str('File format error: {} is not an unique sequence id.\nPlease check the sequence file and try again.').format(_id))
		
		if verbose:
			print(_id + '\n' + sequence + '\n')

	if verbose:
		print()
		print(':::::::::::::::::   summary   :::::::::::::::::')
		print()
		print(':::Total sequences  : ' + str(count))
		print(':::Unreadable		   : ' + str(unreadable) + ' --> ' + str(unreadable_list))
		print(':::Corrupted				: ' + str(corrupted) + ' --> ' + str(corrupted_list))
		print(':::Wild Type				: ' + str(wildtype) + ' --> ' + str(wildtype_list))
		print(':::Good						 : ' + str(count - (corrupted + wildtype + unreadable)))

	return sequence_dict


def merge_from_directory(inputdir, ext='txt', outfilename='raw_inputfile.txt', verbose=False):
	'''('path', 'path') -> textfile
	Merge all the files in inputdir into a unique text file.
	Precondition: the folder must be in the same main-folder of the script. <<-Check
	'''
	counter = 0
	with open(outfilename, 'wb') as outfile:
		for filename in glob.glob(inputdir+'*.'+ext):
			if verbose: print(filename)
			with open(filename, 'r') as readfile:
				shutil.copyfileobj(readfile, outfile)
			counter += 1
	if verbose: print('{} files merged from {}'.format(counter,inputdir))


def parse_job(sentence):
	'''str -> str
	Parse a sentence and return a function call.
	Example:
	input = 'find all kmers of length 4 repeated at least 6 times'
	output = simple_finder(parsed_sequence, motif_length=4, min_repetition=6)
	'''

	main_dict   = {
					'algorithms':['simple_finder','mismatch_finder']

				  }

	helper_dict = {
					'simple_finder':['find','all', 'kmers','motifs'],
					'motif_length':['length','long','bases','letters'],
					'min_repetition':['repeated','at','least','times'],
					'sequence':'',
					'sequence_dict':''
				  }


	counter_dict = {}
	for key in helper_dict:
		counter_dict.update({key:[0,'']})

	words = sentence.split()

	i = 0
	for word in words:
		for key in helper_dict:
			if word in helper_dict[key]:
				print(word,key)
				counter_dict[key][0] += 1
				try:
					counter_dict[key][1] = int(words[i+1])
				except:
					pass

		i+=1


	return counter_dict
#print(parse_job('find all kmers of length 4 repeated at least 6 times'))

def simple_finder(sequence_dict, motif_length, min_repetition):
	'''(dict, int, int) -> OrderedDict(sorted(list))
	Find all the motifs long 'motif_length' and repeated at least 'min_repetition' times.
	Return an OrderedDict having motif:repetition as key:value sorted by value. 
	'''
	motif_dict = {}
	for _id, sequence in sequence_dict.items():
		#populate a dictionary of motifs (motif_dict)
		for i in range(len(sequence) - motif_length +1):
			motif = sequence[i:i+motif_length]
			if motif not in motif_dict:
				motif_dict[motif] = 1
			else:
				motif_dict[motif] += 1

	#remove from motif_dict all the motifs repeated less than 'repetition' times
	keys_to_remove = [key for key, value in motif_dict.items() if value < min_repetition]
	for key in keys_to_remove:
		del motif_dict[key]
	
	#Return a sorted dictionary
	return OrderedDict(sorted(motif_dict.items(), key=itemgetter(1), reverse=True))


def simple_mismatches(sequence, motif_length, max_mismatches, most_common=False):
	'''(str, int, int) -> sorted(list)
	Find the most frequent k-mers with mismatches in a string.
	Input: A sequence and a pair of integers: motif_length (<=12) and max_mismatch (<= 3).
	Output: An OrderedDict containing all k-mers with up to d mismatches in string.

	Sample Input:	ACGTTGCATGTCGCATGATGCATGAGAGCT 4 1
	Sample Output:	OrderedDict([('ATGC', 5), ('ATGT', 5), ('GATG', 5),...])
	'''
	#from collections import OrderedDict
	#from operator import itemgetter

	#check passed variables
	if not motif_length <= 12 and motif_length >= 1:
		raise ValueError("motif_length must be between 0 and 12. {} was passed.".format(motif_length))
	if not max_mismatches <= 3 and max_mismatches >= 1:
		raise ValueError("max_mismatch must be between 0 and 3. {} was passed.".format(max_mismatches))

	motif_dict = {}
	for i in range(len(sequence) - motif_length +1):
		motif = sequence[i:i+motif_length]
		if motif not in motif_dict:
			motif_dict[motif] = 1
		else:
			motif_dict[motif] += 1

	motif_dict_with_mismatches = {}

	for kmer in motif_dict:
		motif_dict_with_mismatches.update({kmer:[]})
			
		for other_kmer in motif_dict:
			mismatches = 0
			for i in range(len(kmer)):
				if kmer[i] != other_kmer[i]:
					mismatches += 1
			if mismatches <= max_mismatches:
				motif_dict_with_mismatches[kmer].append([other_kmer,motif_dict[other_kmer]])

	tmp = {}
	for item in motif_dict_with_mismatches:
		count = 0
		for motif in motif_dict_with_mismatches[item]:
			count += motif[-1]
		tmp.update({item:count})

	result = OrderedDict(sorted(tmp.items(), key=itemgetter(1), reverse=True))
	if most_common:
		commons = OrderedDict()
		_max = result.items()[0][1]
		for item in result:
			if result[item] == _max:
				commons.update({item:result[item]})
			else:
				return commons

	return result


def kmer_mismatches(kmer, d):
	'''(str, int) -> list()
	Returns all kmers that are within d mismatches of the given kmer.
	'''
	mismatches = [kmer]  # Initialize mismatches with the k-mer itself (i.e. d=0).
	alt_bases = {'A':'CGT', 'C':'AGT', 'G':'ACT', 'T':'ACG'}
	for dist in xrange(1, d+1):
		for change_indices in combinations(xrange(len(kmer)), dist):
			for substitutions in product(*[alt_bases[kmer[i]] for i in change_indices]):
				new_mistmatch = list(kmer)
				for idx, sub in izip(change_indices, substitutions):
					new_mistmatch[idx] = sub
				mismatches.append(''.join(new_mistmatch))
	return mismatches


def rosa_mismatches(sequence, k, d):
	'''(str, int, int) -> list()
	Returns all most frequent kmers of lenght k with up to d mismatches in a sequence.
	Code from ROSALIND.
	'''
	# Frequency analysis so we don't generate mismatches for the same k-mer more than once.
	kmer_freq = defaultdict(int)
	for i in xrange(len(sequence)-k+1):
		kmer_freq[sequence[i:i+k]] += 1

	# Get all of the mismatches for each unique k-mer in the sequence, appearing freq times.
	mismatch_count = defaultdict(int)
	for kmer, freq in kmer_freq.iteritems():
		for mismatch in kmer_mismatches(kmer, d):
			mismatch_count[mismatch] += freq

	# Computing the maximum value is somewhat time consuming to repeat, so only do it once!
	max_count = max(mismatch_count.values())
	return sorted([kmer for kmer, count in mismatch_count.iteritems() if count == max_count])


def hamming_distance(sequence_a,sequence_b):
	'''(str, str) -> int
	Return the Hamming distance between equal-length sequences
	'''
	a = sequence_a
	b = sequence_b
	if len(a) != len(b):	
		raise ValueError("Undefined for sequences of unequal length")
	return sum(_a != _b for _a, _b in zip(a, b))


def levenshtein_distance(sequence_a,sequence_b):
	'''(str, str) -> int
	Returns the Levenshtein's distance among two sequences.
	'''
	a = sequence_a
	b = sequence_b

	if len(a) < len(b):
		return levenshtein(b, a)

	# len(a) >= len(b)
	if len(b) == 0:
		return len(a)

	previous_row = range(len(b) + 1)
	for i, c1 in enumerate(a):
		current_row = [i + 1]
		for j, c2 in enumerate(b):
			insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
			deletions = current_row[j] + 1		   # than b
			substitutions = previous_row[j] + (c1 != c2)
			current_row.append(min(insertions, deletions, substitutions))
		previous_row = current_row
	
	return previous_row[-1]


def dice_coefficient(sequence_a,sequence_b):
	'''(str, str) -> float
	Return the dice cofficient of two sequences.
	'''
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
	lena = len(a_bigram_list)
	lenb = len(b_bigram_list)
	# initialize match counters
	matches = i = j = 0
	while (i < lena and j < lenb):
		if a_bigram_list[i] == b_bigram_list[j]:
			matches += 2
			i += 1
			j += 1
		elif a_bigram_list[i] < b_bigram_list[j]:
			i += 1
		else:
			j += 1
	
	score = float(matches)/float(lena + lenb)
	return score




if __name__ == '__main__':
	import sys
	import argparse

	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
	exclusive = parser.add_mutually_exclusive_group()


	parser.add_argument('-v','--verbose',
						help='displays lots of prints in the console',
						action='store_true')
	parser.add_argument('-o','--outputfile',
						help='writes the results to a text file',
						type=str)
	exclusive.add_argument('-f','--inputfile',
						help='reads data from a text file: file.txt',
						type=str)
	exclusive.add_argument('-d','--inputdir',
						help='reads data from text files in a directory: /myDir/mySubdir',
						type=str)
	exclusive.add_argument('-s','--sequence',
						help="takes a sequence as input : 'aGtcAATGa'",
						type=str)
	exclusive.add_argument('-ss','--sequences',
						help="takes a list of sequences as insput: ['ATCG','GGGG',...]",
						nargs='*',
						type=list)
	parser.add_argument('-e','--experiment',
						help='takes the experiment you want to run as input: int'+\
							'\n*******************************************'+\
							'\nM13KE - p3 N-term display - NEB PhD-12  : 1'+\
							'\nM13KE - p3 N-term display - NEB PhD-7   : 2'+\
							'\nM13KE - p3 N-term display - NEB PhD-C7C : 3'+\
							'\nM13KE - p8 N-term display - custom      : 4'+\
							'\nDNA SELEX                               : 5'+\
							'\nRNA SELEX                               : 6'+\
							'\n*******************************************',
						type=int)


	args = parser.parse_args()
	
	if args.verbose:
		print('::::::::::::::::')
		print('::verbose mode::')
		print('::::::::::::::::')

		print('\n\n###system info:')
		print('\n'+sys.version)


		print('\n\n###job info:')
		print('\narguments:')
		for item in str(args).split(','):
			item = item.replace('Namespace(','')
			item = item.replace(')','')
			print('\t'+item.strip())


		print('\n\n###execution log:')
		print()

	if args.sequence:
		#parse the input and return OrderedDict([('>id', 'AGGTC')])
		seq_dict = parse_sequence(args.sequence)
		

	if args.inputdir:
		#parse the input and return OrderedDict([('>id', 'AGGTC'),...])
		seq_dict = parse_directory(args.inputdir)
		#code from seqPrep.py


