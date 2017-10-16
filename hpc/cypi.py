#!/hpc/local/CentOS7/common/lang/python/3.6.1/bin/python3
#$ -l h_rt=48:00:00,h_vmem=64G
#$ -pe threaded 8
#$ -S /hpc/local/CentOS7/common/lang/python/3.6.1/bin/python3
#$ -cwd
#$ -M a.marcozzi@umcutrecht.nl
#$ -m beas
#$ -v PATH


## Cyclomics Pipeline Part 1: Map and Split
## It requires LAST and Python >= 3.6 wiht the following libs

import warnings, random, string, glob, os, pickle, argparse
from sys import version
from time import time
from itertools import islice
from multiprocessing import Pool, cpu_count
from subprocess import run, check_output
import numpy as np

warnings.filterwarnings("ignore") #ignore numpy warnings

print(f'Python {version}\n')
print(check_output('lastal --version', shell=True).decode('UTF-8'))
#print(check_output('muscle  -version', shell=True).decode('UTF-8'))

assert run('lastal --version', shell=True).returncode == 0
#assert run('muscle  -version', shell=True).returncode == 0


## Funcs ##
def list_of_files(path, extension, recursive=False):
    '''
    Return a list of filepath for each file into path with the target extension.
    If recursive, it will loop over subfolders as well.
    '''
    if not recursive:
        for file_path in glob.iglob(path + '/*.' + extension):
            yield file_path
    else:
        for root, dirs, files in os.walk(path):
            for file_path in glob.iglob(root + '/*.' + extension):
                yield file_path


def chunks(data, size):
    '''dict => chunks_of_dict
    Split a dict in chunks of desired size.
    Useful to pass chunks of data to functions in parallel via Pool.map()
    '''
    it = iter(data)
    for i in range(0, len(data), size):
        yield {k:data[k] for k in islice(it, size)}


def parse_fasta(fasta_file):
    '''file_path => dict
    Return a dict of id:sequences.
    '''
    d = {}
    _id = False
    seq = ''
    with open(fasta_file,'r') as f:
        for line in f:
            if line.startswith('\n'):
                continue
            if line.startswith('>'):
                if not _id:
                    _id = line[1:].strip()
                elif _id and seq:
                    d.update({_id:seq})
                    _id = line[1:].strip()
                    seq = ''
            else:
                seq += line.strip()
        d.update({_id:seq})
    return d


def gen_lastDB(bb, fasta_db_file):
    '''(str, filepath) => run lastdb
    Run lastdb to generate a last-DataBase.
    The sequence is parse from a fasta file containing the desired backbone.
    bb is the name of the backbone as specified in the fasta database.
    If in the fasta database the ID is >BB2_100 (340), then bb is 'BB2_100'
    '''
    print(f'searching for {bb} in {fasta_db_file}')
    backbone = {k.split()[0]:v.upper() for k,v in parse_fasta(fasta_db_file).items()
                if k.split()[0] == bb} #takes [0] because the Cyclomics backbones_db.fasta
                                       #has id line in the form ">ID (len(sequence))"

    assert len(backbone) == 1 #the backbone id must be unique
    print(f'backbone found!')
    print(f'backbone sequence: {backbone[bb]}')
    print(f'backbone length: {len(backbone[bb])}bp')

    print(f'building LAST database for {bb}')
    with open('last_db.fasta', 'w') as f:
        f.write(f'>{bb}\n{backbone[bb]}')    
    run(f'lastdb {bb}_DB last_db.fasta', shell=True)


def parse_fastq(file_path):
    '''file_path => dict
    Return a dict of sequence_id:{'squence':'ACGT',
                                  'qscore'  :'=>?@'}.
    '''
    data = {}
    next_is_score = False
    with open(file_path, 'r') as inp:
        for line in inp:
            if line.startswith('\n'):
                continue

            if line.startswith('@') and not next_is_score:
                ids = line.strip().split()
                runid   = ids[1].split('=')[-1]
                read    = ids[2].split('=')[-1]
                ch      = ids[3].split('=')[-1]
                barcode = ids[-1].split('=')[-1]

                sequence_id = f'{runid}-{read}-{ch}-{barcode}'
            
            elif line == ('+\n'):
                next_is_score = True
                
            else:
                if next_is_score:
                    next_is_score = False
                    
                    #try:
                    assert sequence_id not in data
                    data.update({sequence_id:{'sequence':sequence,
                                              'qscore':line.strip()}}) #quality score
                    #except:
                    #    print(sequence_id)
                    
                    #The character '!' represents the lowest quality while '~' is the highest.
                    #Here are the quality value characters in left-to-right increasing order of quality (ASCII):
                    #!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~

                else:
                    sequence = line.strip()             
    return data


def parse_fast5(file_path):
    '''file_path => dict
    Return a dict of sequence_id:{'squence':'ACGT',
                                  'qscore'  :'=>?@'}.
    '''
    data = {}
    for line in check_output(f'poretools tabular {file_path}', shell=True).decode('UTF-8').split('\n'):
        if not (line.startswith('length') or line == ''):
            d = line.split('\t')
            sequence_id = d[1]
            assert sequence_id not in data
            sequence = d[-2]
            qscore = d[-1]
            data.update({sequence_id:{'sequence':sequence,
                                      'qscore':qscore}}) #quality score
    return data


def map_bb(data, bb):
    '''dict => dict
    Return a dict having as keys the read_id and list of tuples.
    Each tuple contains (start, end) coordinates of the bb mapped on the read.
    bb is the name of the backbone as specified in the fasta database.
    If in the fasta database the ID is >BB2_100 (340), then bb is 'BB2_100' 
    '''
    r = {}
    for k,v in data.items():
        #map to backbone
        out = check_output(f'echo ">{k}\n{v["sequence"]}" | lastal {bb}_DB', shell=True) #> maf/{k}map.maf'
        if len(out) > 1000: #the output of lastal is ~= 500 char long if no sequences were mapped
            r[k] = [] #store the result as a list of tuples
                      #each tuple contain (start, end) coordinates
                      #of the bb mapped on the read
            for line in out.decode('UTF-8').split('\n'):
                if k in line:
                    #print(line)
                    map_start, map_len = [int(n) for n in line.split()[2:4]]
                    #print(map_start, map_length)
                    r[k].append(((map_start, map_start+map_len)))
    return r


def map_overview(map_tuples):
    '''list_of_tuples => tuple
    Return the mean and the standard deviation of the backbone and the insert.
    map_tuples is a list of tuples containing the (start, end) coordinates
    of the bb mapped on the read.
    '''
    last_t = False
    bb_len = [] #distance between start/end
    ins_len = [] #distance between the end of endA and startB
    for t in sorted(map_tuples)[1:-1]:     
        bb_len.append(t[1]-t[0])
        
        if last_t is not False:
            ins_len.append(t[0]-last_t[1])
        
        last_t = t
        
    r = (np.mean(bb_len), np.std(bb_len), np.mean(ins_len), np.std(ins_len))
    return tuple(int(round(n)) if not np.isnan(n) else n for n in r)


def split_data(data):
    '''dict => dict
    Split each sequence based on their mapping coordinates.
    '''    
    r = {}
    for k,v in data.items(): #a filter can be added here to select only good reads
        
        if np.nan not in map_overview(v['bb_map']):
            
            seq = data[k]['sequence']
            backbones = [] #all backbone segments in the read
            inserts = [] #all insert segments in the read
            
            last_e = False
            for ii in sorted(v['bb_map']):
                s, e = ii
                backbones.append(seq[s:e+1])
                
                if last_e:
                    inserts.append(seq[last_e:s])
                elif s > 0:
                    inserts.append(seq[:s])
                last_e = e
                    
        ## Add the list of backbones and inserts to data
        r[k] = {'backbones':backbones,
                'inserts':inserts}
    return r


def _f(x):
    '''
    This is used to pass bb to Pool.map()
    since Pool.map() do not take 2 arguments.
    It works only if it's defined in the global scope.
    '''
    return map_bb(x, bb)


## Pipeline ##
def main(input_folder, file_type, bb, fasta_db_file):


    ## Init
    if fasta_db_file:
        gen_lastDB(bb, fasta_db_file)



    ## Parse in parallel
    print('parsing...')
    start = time()
    if file_type == 'fastq':
        with Pool(cpu_count()) as p:
            data = p.map(parse_fastq, 
                         list_of_files(path=input_folder, extension=file_type, recursive=True))   
    elif file_type == 'fast5':
        with Pool(cpu_count()) as p:
            data = p.map(parse_fast5, 
                         list_of_files(path=input_folder, extension=file_type, recursive=True))
    else:
        raise ValueError('file_type must be "fast5" or "fastq"')

    #convert data to a dict instead of a list of dicts    
    data = {k:v for i in data for k,v in i.items()}
    print(f'done in {round(time()-start,2)} seconds')
    print(f'found {len(data)} reads')



    ## Map in parallel
    #def _f(x): #this is to pass bb to Pool.map()
    #    return map_bb(x, bb)
    print('mapping...')
    start = time()
    with Pool(cpu_count()) as p:
        bb_maps = p.map(_f, chunks(data, 100))
    print(f'done in {round(time()-start,2)} seconds')
    print(f'mapped {len(data)} bb_maps')
    #convert data to a dict instead of a list of dicts
    bb_maps = {k:v for i in bb_maps for k,v in i.items()}



    ## Integrate bb_maps into data
    for k,v in data.items():
        try:
            data[k]['bb_map'] = bb_maps[k]
        except KeyError:
            data[k]['bb_map'] = []



    #Split in parallel
    print('splitting...')
    start = time()
    with Pool(cpu_count()) as p:
        split_sequences = p.map(split_data, chunks(data, 500))
    print(f'done in {round(time()-start,2)} seconds')
    print(f'split {len(split_sequences)} sequences')
    #convert data to a dict instead of a list of dicts
    split_sequences = {k:v for i in split_sequences for k,v in i.items()}



    ## Integrate split_sequences into data
    for k,v in data.items():
        try:
            data[k]['backbones'] = split_sequences[k]['backbones']
        except KeyError:
            data[k]['backbones'] = []
        try:
            data[k]['inserts'] = split_sequences[k]['inserts']
        except KeyError:
            data[k]['inserts'] = []



    ## Dump the data
    print('dumping data...')
    start = time()
    if not os.path.exists(f'{input_folder}/dumps'):
        os.makedirs(f'{input_folder}/dumps')
    #run(f'{input_folder}/dumps', shell=True)
    n = 0
    for d in chunks(data, 1000):
        with open(f'{input_folder}/dumps/data_chunk_{n}.dump', 'wb') as f:
            pickle.dump(d, f)
        n += 1
    print(f'done in {round(time()-start,2)} seconds')


    ## Clean up
    print('cleaning up...')
    files = [f'{bb}_DB.{ext}' for ext in ['bck','suf','prj','tis','des','sds','ssp']]
    files.append('last_db.fasta') #default name for lastdb output
    for f in files:
        os.remove(f)
    print('done')


    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='The analysis of Cyclomics data.')
    parser.add_argument('-i', '--input_folder',
                        help='Where the base-called files are located.',
                        type=str,
                        required=True)

    parser.add_argument('-t', '--file_type',
                        help='Specify wether the files in the input_folder are fast5 of fastq.',
                        type=str,
                        required=True)
    parser.add_argument('-bb', '--backbone',
                        help='The name of the backbone you want to map.',
                        type=str,
                        required=True)
    parser.add_argument('-db', '--database',
                        help='Fasta-formatted file containing the backbone sequences.',
                        type=str,
                        required=True)

    args = parser.parse_args()
    input_folder = args.input_folder
    file_type = args.file_type
    bb = args.backbone
    fasta_db_file = args.database

    main_start = time()
    main(input_folder, file_type, bb, fasta_db_file)
    print(f'Process completed in {round(time()-main_start,2)} seconds')












