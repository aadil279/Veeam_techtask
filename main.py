import hashlib

def hashfile(file):
    BUF_SIZE = 65536    #Buffer size for file reading (64kB)
    md5 = hashlib.md5()

    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)

            if not data:
                break
            md5.update(data)
    return md5.hexdigest()

# Hashes and compares two files to check if they are equal
def isEqual(file1, file2):
    f1Hash = hashfile(file1)
    f2Hash = hashfile(file2)

    if f1Hash == f2Hash:
        return True
    return False

if __name__ == '__main__':
    if(isEqual("source/file1.txt", "replica/file1.txt")):
        print("Files are equal")
    else:
        print("Files are NOT equal")

