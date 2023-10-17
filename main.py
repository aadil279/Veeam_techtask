import hashlib
import os
import sys
import time
import shutil
from datetime import datetime

REPLICA_PATH = None
SOURCE_PATH = None
LOG_PATH = None
SYNC_INTERVAL = None  # In seconds


def main():
    init_vars()
    while True:
        sync_folders()
        time.sleep(SYNC_INTERVAL)


# Initializes global attributes values, using input arguments from command line
def init_vars():
    if len(sys.argv) < 5:
        print("Please insert all 4 arguments (replica_path, source_path, log_path, sync_interval)")
        exit()
    global REPLICA_PATH
    global SOURCE_PATH
    global LOG_PATH
    global SYNC_INTERVAL

    if not (os.path.isdir(sys.argv[1]) and os.path.isdir(sys.argv[2]) and os.path.isfile(sys.argv[3])):
        print("Please insert valid paths for replica folder, source folder and log file")
        exit()

    REPLICA_PATH = sys.argv[1]
    SOURCE_PATH = sys.argv[2]
    LOG_PATH = sys.argv[3]
    try:
        SYNC_INTERVAL = float(sys.argv[4])
    except ValueError:
        print("Invalid value for synchronization interval")


# Checks both folders and corrects inconsistencies
def sync_folders():
    source_files = os.listdir(SOURCE_PATH)
    replica_files = os.listdir(REPLICA_PATH)

    for file in source_files:
        if os.path.isfile(os.path.join(SOURCE_PATH, file)):

            if file not in replica_files:  # If the file does not exist in replica, copy to it
                replace_file(file)
                log("Added file " + file + " in replica folder")

            else:  # If the file exists in replica but isn't the same as in source, replace it
                if not is_equal_file(os.path.join(SOURCE_PATH, file), os.path.join(REPLICA_PATH, file)):
                    replace_file(file)
                    log("Replaced file " + file + " in replica folder with updated version from source folder.")

    for file in replica_files:
        if file not in source_files and os.path.isfile(os.path.join(REPLICA_PATH, file)):  # If file is in replica but not in source, it is an old deleted file
            os.remove(os.path.join(REPLICA_PATH, file))
            log("Removed file " + file + " from replica folder as it is no longer in source")


def replace_file(file):
    source_file_path = os.path.join(SOURCE_PATH, file)
    replica_file_path = os.path.join(REPLICA_PATH, file)
    if os.path.exists(replica_file_path):
        os.remove(replica_file_path)
    shutil.copy2(source_file_path, REPLICA_PATH)


# Hashes file using MD5 for later comparison
def hash_file(file):
    buf_size = 65536  # Buffer size for file reading (64kB)
    md5 = hashlib.md5()

    with open(file, 'rb') as f:
        while True:
            data = f.read(buf_size)

            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


# Hashes and compares two files to check if they are equal
def is_equal_file(file1, file2):
    f1_hash = hash_file(file1)
    f2_hash = hash_file(file2)

    if f1_hash == f2_hash:
        return True
    return False


def log(text):
    message = "[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + text
    with open(LOG_PATH, 'a') as log:
        log.write(message + '\n')
    print(message)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Closing program...")
        exit()
