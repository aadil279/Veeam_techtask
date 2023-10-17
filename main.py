import hashlib
import os
import time
import shutil

replica_path = os.path.join("replica")
source_path = os.path.join("source")
log_path = os.path.join("operations.log")
sync_interval = 5   #in seconds

def main():
    while True:
        compareFolders()
        time.sleep(sync_interval)

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

def compareFolders():
    sourceFiles = os.listdir(source_path)
    replicaFiles = os.listdir(replica_path)
    for file in sourceFiles:
        if file not in replicaFiles:
            replaceFile(file)
            log("Added file " + file + " in replica folder")
        if file in replicaFiles:
            if not isEqual(os.path.join(source_path, file), os.path.join(replica_path, file)):
                replaceFile(file)
                log("Replaced file " + file + " in replica folder with updated version from source folder.")
                #replicaFiles.remove(file)  # Does not delete the file, just removes it from replicaFiles array for shorter iterations


        #sourceFiles.remove(file)        # Does not delete the file, just removes it from sourceFiles list for shorter iterations

    for file in replicaFiles:
        if file not in sourceFiles:     # If file is in replica but not in source, it is an old deleted file
            os.remove(os.path.join(replica_path, file))
            log("Removed file " + file + " from replica folder as it is no longer in source")

def replaceFile(file):
    sourceFilePath = os.path.join(source_path, file)
    replicaFilePath = os.path.join(replica_path, file)
    if os.path.exists(replicaFilePath):
        os.remove(replicaFilePath)
    shutil.copy2(sourceFilePath, replica_path)

def log(text):
    with open(log_path, 'a') as log:
        log.write(text + '\n')
    print(text)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Closing program...")
        exit()