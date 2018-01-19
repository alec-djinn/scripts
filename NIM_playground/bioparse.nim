import commandeer

commandline:
  argument inputFile, string, "infile","f"
  argument inputFile, string, "indir" ,"d"
  option fasta, bool, "fasta","a"
  option fast5, bool, "fast5","5"
  option fastq, bool, "fastq","q"
  exitoption "help", "h",
             "Usage: bioparse [--infile <path>|--indir <path>] [--fasta|--fast5|--fastq] " &
             "..."
  errormsg "Failed parsing arguments, please check and try again."


echo("integer = ", integer)
echo("floatingPoint = ", floatingPoint)
echo("character = ", character)
echo("strings (one or more) = ", strings)

if optionalInteger != 0:
  echo("optionalInteger = ", optionalInteger)

if testing:
  echo("Testing enabled")