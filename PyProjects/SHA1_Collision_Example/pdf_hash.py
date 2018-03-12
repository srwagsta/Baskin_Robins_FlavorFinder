import hashlib

'''
This is quick function that console outputs the SHA1 hash
result for the passed file

@precondition The passed file must be a valid file the is in the
current working directory
@postcondition The file's hash is outputted to the console but not stored,
the argument file remains unchanged and is closed at ed of execution.
@throws FileNotFound exception if passed file does not exsist
'''
def hash(fileName):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(fileName, 'rb') as InFile:
        buf = InFile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = InFile.read(BLOCKSIZE)
    print('{:s} -> {:s}'.format(fileName, hasher.hexdigest()))


# CAUTION: Passed files for the hash function
# must be in the current working directory
print('SHA1 Hashes for different input files')
hash('shattered-1.pdf')
hash('shattered-2.pdf')
