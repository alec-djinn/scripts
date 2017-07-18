import strutils, tables, parseopt2, system, algorithm, future

##Docs
var doc = """
Compute the Dice coefficient of two strings.

Argument      Key    Description

string A      -a     First input string
string B      -b     Second input string

help          -h     print this help
"""

##Parse arguments
var args = initTable[string, string]() #arg:val

for kind, key, val in getopt():
    echo "kind:", kind
    echo "key :", key
    echo "val :", val
    args.add(key,val)

if args.hasKey("h"):
    echo doc
    quit()

proc dice_coefficient(a:string, b:string): float =

    if len(a) == 0 or len(b) == 0: return 0.0
    # quick case for true duplicates
    if a == b: return 1.0
    # if a != b, and a or b are single chars, then they can't possibly match
    if len(a) == 1 or len(b) == 1: return 0.0

    var
        a_bigram_list = lc[a[i..<i+2] | (i <- 0..<len(a)-1), string]
        b_bigram_list = lc[b[i..<i+2] | (i <- 0..<len(b)-1), string]
        lena = len(a_bigram_list)
        lenb = len(b_bigram_list)
        matches = 0
        i = 0
        j = 0

    sort(a_bigram_list, system.cmp)
    sort(b_bigram_list, system.cmp)
        
    while i < lena and j < lenb:
        if a_bigram_list[i] == b_bigram_list[j]:
            matches += 2
            i += 1
            j += 1
        elif a_bigram_list[i] < b_bigram_list[j]:
            i += 1
        else:
            j += 1
    
    return matches/(lena + lenb)

echo dice_coefficient(args["a"],args["b"])