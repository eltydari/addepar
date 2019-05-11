import argparse
import sys
import os, os.path
import tempfile
from   collections import deque
from   shutil import copyfile

class FileMerger(object):
    def __init__(self):
        self._inputPath = None
        self._outputFile = None
        self._fileId = 0
        self._queue = deque()

        self._prevline = ''

    def setInputPath(self, directory):
        assert os.path.exists(directory), "Input directory does not exist: {}".format(directory)
        self._inputPath = directory

    def setOutputFile(self, fileName):
        path = os.path.split(fileName)[0]
        assert os.access(path, os.W_OK), "Output directory is not writeable: {}".format(path)
        self._outputFile = fileName

    def _writeLine(self, line, file, fromFile):
        line = line.strip()
        assert line >= self._prevline, "File is not sorted: {}".format(fromFile)
        if line != self._prevline:
            file.write(line + '\n')
            self._prevline = line

    def _walkInput(self):
        self._queue = deque(os.path.join(self._inputPath, f) \
                            for f in os.listdir(self._inputPath) \
                            if os.path.isfile(os.path.join(self._inputPath,f)))
        self._queue.append("END")

    def _walkFiles(self, nfile1, nfile2, destDir):
        tempfileName = os.path.join(destDir,str(self._fileId)+".txt")
        with open(nfile1, 'r') as file1,\
             open(nfile2, 'r') as file2,\
             open(tempfileName, 'w') as wfile:

            self._prevline = ''            
            lineFile1 = file1.readline()
            lineFile2 = file2.readline()
            while lineFile1 != '' or lineFile2 != '':
                if lineFile1 == '\n':
                    lineFile1 = file1.readline()
                elif lineFile2 == '\n':
                    lineFile2 = file2.readline()
                elif lineFile1 == '':
                    self._writeLine(lineFile2, wfile, nfile2)
                    lineFile2 = file2.readline()
                elif lineFile2 == '':
                    self._writeLine(lineFile1, wfile, nfile1)
                    lineFile1 = file1.readline()
                else:
                    if lineFile2 < lineFile1:
                        self._writeLine(lineFile2, wfile, nfile2)
                        lineFile2 = file2.readline()
                    elif lineFile1 < lineFile2:
                        self._writeLine(lineFile1, wfile, nfile1)
                        lineFile1 = file1.readline()
                    else:
                        self._writeLine(lineFile1, wfile, nfile1)
                        lineFile2 = file2.readline()
                        lineFile1 = file1.readline()
        return tempfileName

    def mergeAll(self):
        self._walkInput()
        with tempfile.TemporaryDirectory() as tempDir:
            while len(self._queue) > 2: #We are at the end if there's only one file + 'END'
                firstFile = self._queue.popleft()
                if firstFile == "END":
                    self._queue.append("END")
                    continue
                if self._queue[0] == "END":
                    self._queue.append(firstFile)
                    self._queue.popleft()
                    self._queue.append("END")
                    continue
                secondFile = self._queue.popleft()
                outputFile = self._walkFiles(firstFile,secondFile,tempDir)
                self._queue.append(outputFile)
                self._fileId += 1
            for fileName in self._queue:
                if fileName != "END":
                    copyfile(fileName, self._outputFile)
                    print("Success!")
                    return 0
        return 1


def main():
    parser = argparse.ArgumentParser(description="Merge sorted files.")
    parser.add_argument("input_path", type=str, help="Path of the folder containing text files.")
    parser.add_argument("output_file_path", type=str, help="Path of the output file.")
    args = parser.parse_args()
    
    fm = FileMerger()
    fm.setInputPath(args.input_path)
    fm.setOutputFile(args.output_file_path)
    sys.exit(fm.mergeAll())

if __name__ == "__main__":
    main()
