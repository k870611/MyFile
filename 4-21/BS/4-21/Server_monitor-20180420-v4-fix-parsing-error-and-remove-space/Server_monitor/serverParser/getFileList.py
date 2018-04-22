import os

class getFileList():
    logDir = "output"
    fileList = list()

    def __init__(self):
        print("getFileList init")

    def Run(self):
        currDir = os.getcwd()
        print("currentdir:",currDir)
        newDir = os.path.join(os.getcwd(),self.logDir)
        print("new dir:",newDir)
        tempFileLists = os.listdir(newDir)
        #print("target files:",tempFileLists)

        for file in tempFileLists:
            targetFile = os.path.join(newDir,file)
            #print("target file:",targetFile)
            self.fileList.append(targetFile)

        #print("\n\n\n final files to be parsed:",self.fileList)
        return self.fileList
