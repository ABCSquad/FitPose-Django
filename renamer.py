import pathlib

# Set relevant path in which you want to rename all image files
path = pathlib.Path('./dataset_in/ohp/')

count = 1
test = None

for p in path.rglob('*.*g'):
    if p.parent != test:
        count = 1
    newpath = p.parent/f'{p.parts[-2]}{str(count)}{p.suffix}'
    if newpath.exists() == False:
        p.rename(newpath)
    print(newpath)
    count+=1
    test = p.parent
