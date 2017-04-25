import re

# Regex to check that a cap exist in string.
pattern1 = re.compile(r'\d.*?[A-Z].*?[a-z]')
vocab = ['dog', 'lazy', 'the', 'fly'] # Imagine it's a longer list.

def check_no_caps(s):
    return None if re.match(pattern1, s) else s

def check_nomorethan_five(s):
    return s if len(s) <= 5 else None

def check_in_vocab_plus_x(s,x):
    # s and x are both str.
    return None if s not in vocab else s+x

for n in range(1000):
	slist = ['the', 'dog', 'jumps', 'over', 'the', 'fly']
	# filter with check_no_caps
	slist = [check_no_caps(s) for s in slist]
	# filter no more than 5.
	slist = [check_nomorethan_five(s) for s in slist if s is not None]
	# filter in vocab
	slist = [check_in_vocab_plus_x(s, str(i)) for i,s in enumerate(slist) if s is not None]