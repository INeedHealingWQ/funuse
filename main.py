#!/usr/bin/python3

import sys
import subprocess
import re

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
        self.__DATA = 0
        self.__TEXT = 1
        self.__dataFile = open(dataFile, 'r')
        self.__textFile = open(textFile, 'r')
        self.__dataFileCut = '/tmp/dataFileCut' + str(self.__name__)
        self.__textFileCut = '/tmp/textFileCut' + str(self.__name__)
        self.__dataDict = {}
        self.__textDict = {}
        self.dataDownFlag = False
        self.textDownFlag = False
        ''' self.dataDict = {0 : ['', 0, 0, ...]} '''
        self.unused = {}

    def __del__(self):
        self.__dataFile.close()
        self.__textFile.close()

    def roughCount(self):
        assert self.dataDownFlag is True \
            and self.textDownFlag is True
#        map = [c - c for c in range(0, len(self.__dataDict))]
        for e in self.__textDict:
            for i in self.__textDict[e][1:]:
                g = self.__dataDict.get(i)
                if g != None:
                    self.__dataDict[i].append("TextUsedIt")
        ''' can not del elem during traversing '''
        for e in self.__dataDict:
            for i in self.__dataDict[e][1:]:
                g = self.__dataDict.get(i)
                if g != None:
                    if g[-1] == "TextUsedIt":
                        g[-1] = "AllUsedIt"
                    else:
                        g.append("DataUsedIt")
        for e in self.__dataDict:
            elem = self.__dataDict[e][-1]
            if elem == "AllUsedIt" \
                or elem == "TextUsedIt" \
                    or elem == "DataUsedIt":
                continue
            else:
                self.unused[e] = self.__dataDict[e]

    def deepCount(self):
        assert self.dataDownFlag is True \
               and self.textDownFlag is True

    def start(self):
        self.__stripData()
        self.__stripText()

    def __name__(self):
        return 'dataProcessObj'

    def __stripData(self):
        self.__strip(self.__DATA)

    def __stripText(self):
        self.__strip(self.__TEXT)

    def __strip(self, type):
        elemId = ()
        elem = []
        if type == self.__DATA:
            lines = self.__dataFile.readlines()
            dict = self.__dataDict
        elif type == self.__TEXT:
            lines = self.__textFile.readlines()
            dict = self.__textDict

        for l in lines:
            if l.isspace():
                if elem != []:
                    dict[elemId] = elem
                elemAddr = 0
                elem = []
                continue
            elif not re.findall(r'[0-9a-zA-Z_]+', l):
                continue
            firstWord = re.findall(r'^[0-9a-zA-Z]+', l)
            secondWord = re.findall(r'<[_a-zA-Z0-9.]+>', l)
            if firstWord != [] and secondWord != []:
                elemId = int(firstWord[0], base=16)
                elem.append(secondWord[0].strip('<>'))
                continue
            content = l.split()
            elem.append(int(content[1], base=16))

        if type == self.__DATA:
            self.dataDownFlag = True
        elif type == self.__TEXT:
            self.textDownFlag = True

    def dumpData(self):
        print(self.__dataDict)
        print(self.__textDict)


''' class for processing .text section '''
class textProcessObj:
    def __init__(self, dataFile, textFile):
        self.__dataFile = open(dataFile, 'r')
        self.__textFile = open(textFile, 'r')
        self.__textFileCut = '/tmp/textFileCut_textProcessObj'
        self.__dict_out = '/tmp/dict_out'
        self.__dataDict = {}
        ''' self.__dataDict = {0 : ['', 0, 0, ...]} '''
        self.__textDict = {}
        ''' self.__textDict = {0 : ['', [0, ''], [0, ''], ...]} '''
        self.dataDownFlag = False
        self.textDownFlag = False
        self.unused = {}

    def __del__(self):
        self.__dataFile.close()
        self.__textFile.close()

    def roughCount(self):
        assert self.dataDownFlag is True \
            and self.textDownFlag is True
#        map = [c - c for c in range(0, len(self.__dataDict))]
        for e in self.__dataDict:
            for i in self.__dataDict[e][1:]:
                g = self.__textDict.get(i)
                if g != None:
                    if (g[-1] == 'TextUsedIt'):
                        g[-1] = 'AllUsedIt'
                    elif g[-1] != 'DataUsedIt' and g[-1] != 'AllUsedIt':
                        g.append('DataUsedIt')
        for e in self.__textDict:
            for i in self.__textDict[e][1:]:
                g = self.__textDict.get(i[0])
                if g != None:
                    if g[-1] == 'DataUsedIt':
                        g[-1]  = 'AllUsedIt'
                    elif g[-1] != 'TextUsedIt' and g[-1] != 'AllUsedIt':
                        g.append('TextUsedIt')
        for e in self.__textDict:
            elem = self.__textDict[e][-1]
            if elem == "AllUsedIt" \
                or elem == "TextUsedIt" \
                    or elem == "DataUsedIt":
                continue
            else:
                self.unused[e] = self.__textDict[e]

        fcut = open(self.__textFileCut, 'w')
        for e in self.unused:
            fcut.write('%s: %s\n' %(str(hex(e)), str(self.unused[e])))
        fcut.close()

        dict_out = open(self.__dict_out, 'w')
        for d in self.__textDict:
            dict_out.write('%x-%s:\n' % (d, self.__textDict[d][0]))
            for i in self.__textDict[d][1:-1]:
                dict_out.write('\t%x-%s\n' % (i[0], i[1]))
            dict_out.write('%s\n' % self.__textDict[d][-1])
            dict_out.write('\n')
        dict_out.close()

    def deepCount(self):
       assert self.dataDownFlag is True \
              and self.textDownFlag is True

    def start(self):
        self.__stripData()
        self.__stripText()

    def __name__(self):
        return 'textProcessObj'

    def __stripData(self):
        elemId = ()
        elem = []
        lines = self.__dataFile.readlines()
        dict = self.__dataDict

        for l in lines:
            if l.isspace():
                if elem != []:
                    dict[elemId] = elem
                elem = []
                continue
            elif not re.findall(r'[0-9a-zA-Z_]+', l):
                continue
            firstWord = re.findall(r'^[0-9a-zA-Z]+', l)
            secondWord = re.findall(r'<[_a-zA-Z0-9.]+>', l)
            if firstWord != [] and secondWord != []:
                elemId = int(firstWord[0], base=16)
                elem.append(secondWord[0].strip('<>'))
                continue
            content = l.split()
            elem.append(int(content[1], base=16))

        self.dataDownFlag = True

    def __stripText(self):
        elemId = ()
        elem = []
        lines = self.__textFile.readlines()
        dict = self.__textDict
        pre_elem_movw = None

        for l in lines:
            if l.isspace():
                if elem != []:
                    dict[elemId] = elem
                    elem = []
                continue
            elif not re.findall(r'[0-9a-zA-Z]+', l):
                continue
            firstWord = re.findall(r'^[0-9a-zA-Z]+', l)
            secondWord = re.findall(r'<[_a-zA-Z0-9.]+>', l)
            if firstWord != [] and secondWord != []:
                elemId = int(firstWord[0], base=16)
                elem.append(secondWord[0].strip('<>'))
                continue
            content = l.split()
            if content[2] == 'bl' and [] == re.findall(r'_[a-zA-Z_]+\+', content[4]):
                callFuncAddr = content[3]
                callFuncName = content[4].strip('<>')
                elem.append([int(callFuncAddr, base=16), callFuncName])
                pre_elem_movw = None
            elif content[2] == 'movw' or content[2] == 'movt':
                if content[2] == 'movw':
                    pre_elem_movw = int(content[4][1:], base=10)
                else:
                    if pre_elem_movw != None:
                        cur_elem_movt = int(content[4][1:], base=10) << 16
                        address = pre_elem_movw + cur_elem_movt
                        name = 'UnRegName'
                        elem.append([address, name])
                    pre_elem_movw = None
            else:
                pre_elem_movw = None

        self.textDownFlag = True

    def dumpData(self):
        print(self.__dataDict)
        print(self.__textDict)

class future_filter:
    def __init__(self, data_file, text_file):
        self.__final_text_out = "/tmp/FinalTextOut"
        self.__future_tags_file = "/home/wang/dlinkme/DGS-1210-28PME-B1/core/code/future/tags"
        self.__text_process_obj = textProcessObj(dataFile=data_file, textFile=text_file)
        self.tag_dict = {}
        self.dir_dict = {}
        self.final_out_dict = {}
        self.init_tag_dict()
        self.start()

    def final_trip(self):
        for e in self.tag_dict:
            if self.tag_dict[e][-1] == 'xxxhit':
                dir = self.tag_dict[e][0]
                g = self.dir_dict.get(dir)
                if g == None:
                    self.dir_dict[dir] = [e]
                else:
                    self.dir_dict[dir].append(e)

    def init_tag_dict(self):
        tags_file = open(self.__future_tags_file, 'r')
        tag_lines = tags_file.readlines()
        for line in tag_lines:
            if [] == re.findall(r'^!', line):
                tag_list = line.split()
                dir_list = tag_list[1].split('/')
                self.tag_dict[tag_list[0]] = dir_list
        tags_file.close()

        debug_tag_list = open('/tmp/debugTagList', 'w')
        for e in self.tag_dict:
            debug_tag_list.write('%s: %s\n' %(e, self.tag_dict[e]))
        debug_tag_list.close()

    def start(self):
        self.__text_process_obj.start()
        self.__text_process_obj.roughCount()
        unused = self.__text_process_obj.unused
        for e in unused:
            g = self.tag_dict.get(unused[e][0])
            if g != None:
                self.final_out_dict[e] = unused[e]
                self.tag_dict[unused[e][0]].append('xxxhit')
        self.final_trip()
        final_text_out = open(self.__final_text_out, 'w')
        for e in self.dir_dict:
            final_text_out.write('%s:\n' %e)
            for i in self.dir_dict[e]:
                final_text_out.write('\t%s\n' %i)
            final_text_out.write('\n\n')

        final_text_out.close()

if __name__ == '__main__':
#    finalArgs = [gObjdumpToolPath, gObjdumpArgs,
#                 sys.argv[1]]
#    try:
#        oTmpFileData = open(gOutFileData, 'w')
#    except OSError:
#        print('Open file %s for writing failed.' % (gOutFileData))
#
#    try:
#        oTmpFileText = open(gOutFileText, 'w')
#    except OSError:
#        print('Open file %s for writing failed' % (gOutFileText))
#
#    popen = subprocess.Popen(finalArgs, stdout=subprocess.PIPE)
#    dataFlag, dataGot = False, False
#    textFlag, textGot = False, False
#    lineTokenData = gObjdumpSectionPrompt + gSectionData
#    lineTokenText = gObjdumpSectionPrompt + gSectionText
#    while popen.poll() is None:
#        line = popen.stdout.readline().decode('gbk')
#        if line.find(lineTokenData) != -1:
#            dataFlag, dataGot = True, True
#            textFlag = False
#            continue
#        elif line.find(lineTokenText) != -1:
#            textFlag, textGot = True, True
#            dataFlag = False
#            continue
#        elif line.find(gObjdumpSectionPrompt) != -1:
#            textFlag = dataFlag = False
#            continue
#
#        if dataFlag is True:
#            oTmpFileData.writelines(line)
#        elif textFlag is True:
#            oTmpFileText.writelines(line)
#
#        if dataGot is True and dataFlag is False \
#            and textGot is True and textFlag is False:
#            popen.kill()
#            break
#
#    oTmpFileData.close()
#    oTmpFileText.close()
#
#    dataProcessObj_v = dataProcessObj(gOutFileData, gOutFileText)
#    dataProcessObj_v.start()
#    dataProcessObj_v.roughCount()

    future = future_filter(gOutFileData, gOutFileText)
    future.start()
