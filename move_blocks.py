import os, glob, time


def list_of_files(path, extension, recursive=False):
    '''
    Return a list of filepaths for each file into path with the target extension.
    If recursive, it will loop over subfolders as well.
    '''
    if not recursive:
        for file_path in glob.iglob(path + '/*.' + extension):
            yield file_path
    else:
        for root, dirs, files in os.walk(path):
            for file_path in glob.iglob(root + '/*.' + extension):
                yield file_path



source = '/Users/wpauli/Library/Application Support/Bitcoin/blocks'
source_ = '/Users/wpauli/Library/Application\ Support/Bitcoin/blocks'
dest = '/Volumes/1TB/Bitcoin/blocks'
n = 10
while True:
    source_files = [f.split('/')[-1] for f in list_of_files(source, 'dat')]
    dest_files = [f.split('/')[-1] for f in list_of_files(dest, 'dat')]

    ##move/link all but last ones
    blk_to_move = sorted([f for f in source_files if ('blk' in f and f not in dest_files)])[:-1]
    rev_to_move = sorted([f for f in source_files if ('rev' in f and f not in dest_files)])[:-1]


    if not len(blk_to_move):
        print(f'No files to move, checking again in {n} minutes...')
        time.sleep(60*n)
        if n > 60:
            n = 60
        else:
            n *= 2
        continue
    else:
        n = 10

    #print(source_files)
    #print(dest)
    print('The following files will be moved and linked back')
    print(blk_to_move)
    print(rev_to_move)

    for f in blk_to_move:
        os.system(f"mv {source_}/{f} {dest}/{f}")
        os.system(f"ln -s {dest}/{f} {source_}/{f}")

    for f in rev_to_move:
        os.system(f"mv {source_}/{f} {dest}/{f}")
        os.system(f"ln -s {dest}/{f} {source_}/{f}")