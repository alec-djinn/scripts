import strutils, tables, parseopt2, system, algorithm, future

##Docs
var doc = """
Welcome to aMOF basic documentation!

Argument           Key    Description

config. file       -c     path/to/your/config.cfg
input file         -i     path/to/your/input.fasta
output file        -o     path/to/your/output.txt
algorithm          -a     run a particular algorithm
method             -m     load a predefined method 

help               -h     print this help
"""

##Parse arguments
var args = initTable[string, string]() #arg:val

for kind, key, val in getopt():
    #echo "kind:", kind
    #echo "key :", key
    #echo "val :", val
    args.add(key,val)

if args.hasKey("h"):
    echo doc
    quit()

##Start
echo "running aMOF using the following params: ", args
echo "input file:", args["i"]

##Parse input
var
    input = readFile(args["i"])
    seqs  = initTable[string, string]() #id:seq
    id    : string
    n     : int

n = 0
for line in input.split("\n"):
    n += 1
    if line != "": #skip empty lines
        if ">" in line:
            if id == nil:
                id = line[1..high(line)]
            else: #sequence missing
                echo "Error while parsing the input file at line ", n
                echo "::'$#'is not a valid FASTA::" % args["i"]
                quit()
        else:
            if id != nil:
                seqs.add(id,line)
                id = nil
            else: #id missing
                echo "Error while parsing the input file at line ", n
                echo "::'$#' is not a valid FASTA::" % args["i"]
                quit()
if id != nil: #last sequence is missing
    echo "Error while parsing the input file at line ", n
    echo "::'$#' is not a valid FASTA::" % args["i"]
    quit()


##Summary
echo "Found ",len(seqs)," sequences:"
echo seqs


##Algos##

##Frequent words
var
    fwords    = initCountTable[string]() #seq:count
    motif_len = 5
    motif : string

for k, v in seqs:
    for n in 0..len(v): 
        motif = v[n..<n+motif_len]
        if len(motif) != motif_len:
            break
        else:
            fwords.inc(motif.toLowerAscii())

fwords.sort
echo fwords