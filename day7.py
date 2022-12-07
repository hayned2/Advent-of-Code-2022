import os

class Directory:

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.subDirectories = []
        self.files = []

    def addSubDirectory(self, directory):
        if self.getSubDirectory(directory) == None:
            self.subDirectories.append(Directory(directory, self))
    
    def addFile(self, size, name):
        if self.getFile(name) == None:
            self.files.append(File(name, size))
    
    def calculateSize(self):
        size = 0
        for file in self.files:
            size += file.size
        for subDirectory in self.subDirectories:
            size += subDirectory.calculateSize()
        return size
    
    def getSubDirectory(self, name):
        for directory in self.subDirectories:
            if directory.name == name:
                return directory
        return None
    
    def getFile(self, name):
        for file in self.files:
            if file.name == name:
                return file
        return None

class File:

    def __init__(self, name, size):
        self.name = name
        self.size = size


input1 = open(os.path.dirname(os.path.realpath(__file__)) + '/day7_input1.txt')
topDirectory = Directory('/', None)
currDirectory = None

for line in input1:
    line = line.strip()
    if line == '$ cd ..':
        currDirectory = currDirectory.parent
    elif line == '$ cd /':
        currDirectory = topDirectory
    elif '$ cd' in line:
        target = line.split()[-1]
        if currDirectory.getSubDirectory(target) == None:
            currDirectory.addSubDirectory(target)
        currDirectory = currDirectory.getSubDirectory(target)
    elif '$' not in line:
        [info, name] = line.split()
        if info.isdigit():
            currDirectory.addFile(int(info), name)
        else:
            currDirectory.addSubDirectory(name)

input1.close()
spaceToClear = 30000000 - (70000000 - topDirectory.calculateSize())
bestCandidate = None
bestCandidateSize = 70000000

def calculateDeletionCandidates(topDirectory, totalSize):
    global bestCandidate, bestCandidateSize, spaceToClear
    topDirectorySize = topDirectory.calculateSize()
    if topDirectorySize > spaceToClear and topDirectorySize < bestCandidateSize:
        bestCandidateSize = topDirectorySize
        bestCandidate = topDirectory.name
    if topDirectorySize <= 100000:
        totalSize += topDirectorySize
    for subDirectory in topDirectory.subDirectories:
        totalSize = calculateDeletionCandidates(subDirectory, totalSize)
    return totalSize

print("The total size of all directories less than 100000 is", calculateDeletionCandidates(topDirectory, 0))
print("The best directory to delete is", bestCandidate, "with a size of", bestCandidateSize)
exit()