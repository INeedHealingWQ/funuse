#!/usr/bin/python3

import sys
import subprocess
import re

''' some common tmp file for storing tmp data '''
g_objdump_tool_path = '/opt/toolchain/iProcLDK_3.4.6/usr/bin/arm-linux-objdump'
g_objdump_args = '-D'
g_section_data = ".data:"
g_section_text = ".text:"
g_out_file_data = '/tmp/outfile_data'
g_out_file_text = '/tmp/outfile_text'
g_objdump_section_prompt = "Disassembly of section "

''' class for processing .data section '''
class DataProcessObj:
    def __init__(self, data_file, text_file):
        self.__DATA = 0
        self.__TEXT = 1
        self.__data_file = open(data_file, 'r')
        self.__text_file = open(text_file, 'r')
        self.__data_file_cut = '/tmp/data_file_cut' + str(self.__name__)
        self.__text_file_cut = '/tmp/text_file_cut' + str(self.__name__)
        self.__data_dict = {}
        self.__text_dict = {}
        self.data_down_flag = False
        self.text_down_flag = False
        ''' self.__data_dict = {0 : ['', 0, 0, ...]} '''
        self.unused = {}

    def __del__(self):
        self.__data_file.close()
        self.__text_file.close()

    def rough_count(self):
        assert self.data_down_flag is True \
               and self.text_down_flag is True
#        map = [c - c for c in range(0, len(self.__dataDict))]
        for e in self.__text_dict:
            for i in self.__text_dict[e][1:]:
                g = self.__data_dict.get(i)
                if g != None:
                    self.__data_dict[i].append("***TextUsedIt")
        ''' can not del elem during traversing '''
        for e in self.__data_dict:
            for i in self.__data_dict[e][1:]:
                g = self.__data_dict.get(i)
                if g != None:
                    if g[-1] == "***TextUsedIt":
                        g[-1] = "***AllUsedIt"
                    else:
                        g.append("***DataUsedIt")
        for e in self.__data_dict:
            elem = self.__data_dict[e][-1]
            if elem == "***AllUsedIt" \
                or elem == "***TextUsedIt" \
                    or elem == "***DataUsedIt":
                continue
            else:
                self.unused[e] = self.__data_dict[e]

    def deep_count(self):
        assert self.data_down_flag is True \
               and self.text_down_flag is True

    def start(self):
        self.__strip_data()
        self.__strip_text()

    def __name__(self):
        return 'dataProcessObj'

    def __strip_data(self):
        self.__strip(self.__DATA)

    def __strip_text(self):
        self.__strip(self.__TEXT)

    def __strip(self, type):
        elem_id = ()
        elem = []
        if type == self.__DATA:
            lines = self.__data_file.readlines()
            dict = self.__data_dict
        elif type == self.__TEXT:
            lines = self.__text_file.readlines()
            dict = self.__text_dict

        for l in lines:
            if l.isspace():
                if elem != []:
                    dict[elem_id] = elem
                elemAddr = 0
                elem = []
                continue
            elif not re.findall(r'[0-9a-zA-Z_]+', l):
                continue
            first_word = re.findall(r'^[0-9a-zA-Z]+', l)
            second_word = re.findall(r'<[_a-zA-Z0-9.]+>', l)
            if first_word != [] and second_word != []:
                elem_id = int(first_word[0], base=16)
                elem.append(second_word[0].strip('<>'))
                continue
            content = l.split()
            elem.append(int(content[1], base=16))

        if type == self.__DATA:
            self.data_down_flag = True
        elif type == self.__TEXT:
            self.text_down_flag = True

    def dump_data(self):
        print(self.__data_dict)
        print(self.__text_dict)


''' class for processing .text section '''
class text_process_obj:
    def __init__(self, data_file, text_file):
        self.__data_file = open(data_file, 'r')
        self.__text_file = open(text_file, 'r')
        self.__text_file_cut = '/tmp/textFileCut_textProcessObj'
        self.__dict_out = '/tmp/dict_out'
        self.__data_dict = {}
        ''' self.__dataDict = {0 : ['', 0, 0, ...]} '''
        self.__text_dict = {}
        ''' self.__textDict = {0 : ['', [0, ''], [0, ''], ...]} '''
        self.data_down_flag = False
        self.text_down_flag = False
        self.unused = {}

    def __del__(self):
        self.__data_file.close()
        self.__text_file.close()

    def rough_count(self):
        assert self.data_down_flag is True \
               and self.text_down_flag is True
#        map = [c - c for c in range(0, len(self.__dataDict))]
        for e in self.__data_dict:
            for i in self.__data_dict[e][1:]:
                g = self.__text_dict.get(i)
                if g != None:
                    if (g[-1] == '***TextUsedIt'):
                        g[-1] = '***AllUsedIt'
                    elif g[-1] != '***DataUsedIt' and g[-1] != '***AllUsedIt':
                        g.append('***DataUsedIt')
        for e in self.__text_dict:
            for i in self.__text_dict[e][1:]:
                g = self.__text_dict.get(i[0])
                if g != None:
                    if g[-1] == '***DataUsedIt':
                        g[-1]  = '***AllUsedIt'
                    elif g[-1] != '***TextUsedIt' and g[-1] != '***AllUsedIt':
                        g.append('***TextUsedIt')
        for e in self.__text_dict:
            elem = self.__text_dict[e][-1]
            if elem == "***AllUsedIt" \
                or elem == "***TextUsedIt" \
                    or elem == "***DataUsedIt":
                continue
            else:
                self.unused[e] = self.__text_dict[e]

        fcut = open(self.__text_file_cut, 'w')
        for e in self.unused:
            fcut.write('%s: %s\n' %(str(hex(e)), str(self.unused[e])))
        fcut.close()

        dict_out = open(self.__dict_out, 'w')
        for d in self.__text_dict:
            dict_out.write('%x-%s:\n' % (d, self.__text_dict[d][0]))
            for i in self.__text_dict[d][1:-1]:
                dict_out.write('\t%x-%s\n' % (i[0], i[1]))
            dict_out.write('%s\n' % self.__text_dict[d][-1])
            dict_out.write('\n')
        dict_out.close()

    def deepCount(self):
       assert self.data_down_flag is True \
              and self.text_down_flag is True

    def start(self):
        self.__stripData()
        self.__strip_text()

    def __name__(self):
        return 'textProcessObj'

    def __stripData(self):
        elem_id = ()
        elem = []
        lines = self.__data_file.readlines()
        dict = self.__data_dict

        for l in lines:
            if l.isspace():
                if elem != []:
                    dict[elem_id] = elem
                elem = []
                continue
            elif not re.findall(r'[0-9a-zA-Z_]+', l):
                continue
            first_word = re.findall(r'^[0-9a-zA-Z]+', l)
            second_word = re.findall(r'<[_a-zA-Z0-9.]+>', l)
            if first_word != [] and second_word != []:
                elem_id = int(first_word[0], base=16)
                elem.append(second_word[0].strip('<>'))
                continue
            content = l.split()
            elem.append(int(content[1], base=16))

        self.data_down_flag = True

    def __strip_text(self):
        elem_id = ()
        elem = []
        lines = self.__text_file.readlines()
        dict = self.__text_dict
        pre_elem_movw = None

        for l in lines:
            if l.isspace():
                if elem != []:
                    dict[elem_id] = elem
                    elem = []
                continue
            elif not re.findall(r'[0-9a-zA-Z]+', l):
                continue
            first_word = re.findall(r'^[0-9a-zA-Z]+', l)
            second_word = re.findall(r'<[_a-zA-Z0-9.]+>', l)
            if first_word != [] and second_word != []:
                elem_id = int(first_word[0], base=16)
                elem.append(second_word[0].strip('<>'))
                continue
            content = l.split()
            if content[2] == 'bl' and [] == re.findall(r'_[a-zA-Z_]+\+', content[4]):
                call_func_addr = content[3]
                call_func_name = content[4].strip('<>')
                elem.append([int(call_func_addr, base=16), call_func_name])
                pre_elem_movw = None
            elif content[2] == 'movw' or content[2] == 'movt':
                if content[2] == 'movw':
                    pre_elem_movw = int(content[4][1:], base=10)
                else:
                    if pre_elem_movw != None:
                        cur_elem_movt = int(content[4][1:], base=10) << 16
                        address = pre_elem_movw + cur_elem_movt
                        name = '***UnRegName'
                        elem.append([address, name])
                    pre_elem_movw = None
            else:
                pre_elem_movw = None

        self.text_down_flag = True

    def dump_data(self):
        print(self.__data_dict)
        print(self.__text_dict)

class future_filter:
    def __init__(self, data_file, text_file):
        self.__final_text_out = "/tmp/FinalTextOut"
        self.__future_tags_file = "/home/wang/dlinkme/DGS-1210-28PME-B1/core/code/future/tags"
        self.__text_process_obj = text_process_obj(data_file=data_file, text_file=text_file)
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
        self.__text_process_obj.rough_count()
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
    finalArgs = [g_objdump_tool_path, g_objdump_args,
                 sys.argv[1]]
    try:
        o_tmp_file_data = open(g_out_file_data, 'w')
    except OSError:
        print('Open file %s for writing failed.' % (g_out_file_data))

    try:
        o_tmp_file_text = open(g_out_file_text, 'w')
    except OSError:
        print('Open file %s for writing failed' % (g_out_file_text))

    popen = subprocess.Popen(finalArgs, stdout=subprocess.PIPE)
    dataFlag, dataGot = False, False
    textFlag, textGot = False, False
    lineTokenData = g_objdump_section_prompt + g_section_data
    lineTokenText = g_objdump_section_prompt + g_section_text
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
        elif line.find(g_objdump_section_prompt) != -1:
            textFlag = dataFlag = False
            continue

        if dataFlag is True:
            o_tmp_file_data.writelines(line)
        elif textFlag is True:
            o_tmp_file_text.writelines(line)

        if dataGot is True and dataFlag is False \
            and textGot is True and textFlag is False:
            popen.kill()
            break

    o_tmp_file_data.close()
    o_tmp_file_text.close()

    future = future_filter(g_out_file_data, g_out_file_text)
    future.start()
