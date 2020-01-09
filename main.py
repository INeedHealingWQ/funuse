#!/usr/bin/python3

import sys
import subprocess

''' some common tmp file for storing tmp data '''
gObjdumpToolPath = '/opt/toolchain/iProcLDK_3.4.6/usr/bin/arm-linux-objdump'
gObjdumpArgs = '-D'
gSectionData = ".data:"
gSectionText = ".text:"
gOutFileData = '/tmp/outfile_data'
gOutFileText = '/tmp/outfile_text'
gObjdumpSectionPrompt = "Disassembly of section "

''' class for processing .data section '''
class dataProcessObj:
    def __init__(self, dataFile, textFile):
        self.dataFile = open(dataFile, 'r')
        self.textFile = open(textFile, 'r')
        self.dataFileCut = '/tmp/dataFileCut' + str(self.__name__)
        self.textFileCut = '/tmp/textFileCut' + str(self.__name__)
        self.dataDict = {}
        ''' self.dataDict = {0 : ['', 0, 0, ...]} '''
    def start(self):
        pass
    def __name__(self):
        return 'dataProcessObj'


''' class for processing .text section '''
class textProcessObj:
    def __init__(self, dataFile, textFile):
        self.dataFile = open(dataFile, 'r')
        self.textFile = open(textFile, 'r')
        self.dataFileCut = '/tmp/dataFileCut' + str(self.__name__)
        self.textFileCut = '/tmp/textFileCut' + str(self.__name__)

    def __name__(self):
        return 'textProcessObj'

if __name__ == '__main__':
    finalArgs = [gObjdumpToolPath, gObjdumpArgs,
                 sys.argv[1]]
    try:
        oTmpFileData = open(gOutFileData, 'w')
    except OSError:
        print('Open file %s for writing failed.' % (gOutFileData))

    try:
        oTmpFileText = open(gOutFileText, 'w')
    except OSError:
        print('Open file %s for writing failed' % (gOutFileText))

    popen = subprocess.Popen(finalArgs, stdout=subprocess.PIPE)
    dataFlag, dataGot = False, False
    textFlag, textGot = False, False
    lineTokenData = gObjdumpSectionPrompt + gSectionData
    lineTokenText = gObjdumpSectionPrompt + gSectionText
    while popen.poll() is None:
        line = popen.stdout.readline().decode('gbk')
        if line.find(lineTokenData) != -1:
            dataFlag, dataGot = True, True
            textFlag = False
            continue
        elif line.find(lineTokenText) != -1:
            textFlag, textGot = True, True
            dataFlag = False
            continue
        elif line.find(gObjdumpSectionPrompt) != -1:
            textFlag = dataFlag = False
            continue

        if dataFlag is True:
            oTmpFileData.writelines(line)
        elif textFlag is True:
            oTmpFileText.writelines(line)

        if dataGot is True and dataFlag is False \
            and textGot is True and textFlag is False:
            popen.kill()
            break

    oTmpFileData.close()
    oTmpFileText.close()
