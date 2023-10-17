# Veeam Technical Task
This is the technical task for the role of Internal Development in QA (SDET) Team at Veeam Software.

The task consists in guaranteeing one-way synchronization between two directories: *source* and *replica*. Periodically, the program will check if the content in the replica directory is equal to the source. If there is any discrepancy, such as a file that exists in one but not the other, it will correct it accordingly.

## Getting Started
No prerequisites or dependencies are required for the program to work. All that is required is to supply the program with 4 command line arguments:
- **Replica Path** - Path to the directory that will contain a copy of everything in the source folder.
- **Source Path** - Path to the source directory.
- **Log Path** - Path to the log text file.
- **Sync Interval** - Interval between each synchronization, in seconds.
