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


source_files = [f.split('/')[-1] for f in list_of_files(source, 'dat')]
dest_files = [f.split('/')[-1] for f in list_of_files(dest, 'dat')]

##move/link all but last ones
blk_to_link = sorted([f for f in dest_files if ('blk' in f and f not in source_files)])
rev_to_link = sorted([f for f in dest_files if ('rev' in f and f not in source_files)])


#print(source_files)
#print(dest)
print('The following files will be linked')
print(blk_to_link)
print(rev_to_link)

for f in blk_to_link:
    os.system(f"ln -s {dest}/{f} {source_}/{f}")

for f in rev_to_link:
    os.system(f"ln -s {dest}/{f} {source_}/{f}")