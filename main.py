#!/usr/bin/python3

import sys
import subprocess
import re

''' some common tmp file for storing tmp data '''
g_object_dump_tool_path = '/opt/toolchain/iProcLDK_3.4.6/usr/bin/arm-linux-objdump'
g_object_dump_args = '-D'
g_section_data = ".data:"
g_section_text = ".text:"
g_out_file_data = '/tmp/outfile_data'
g_out_file_text = '/tmp/outfile_text'
g_object_dump_section_prompt = "Disassembly of section "


''' class for processing .data section '''


class DataProcessObj:
    def __init__(self, data_file, text_file):
        self.__DATA = 0
        self.__TEXT = 1
        self.__data_file = open(data_file, 'r')
        self.__text_file = open(text_file, 'r')
        self.__data_dict = {}
        self.__text_dict = {}
        self.data_down_flag = False
        self.text_down_flag = False
        ''' self.dataDict = {0 : ['', 0, 0, ...]} '''
        self.unused = {}

    def __del__(self):
        self.__data_file.close()
        self.__text_file.close()

    def cough_count(self):
        assert self.data_down_flag is True \
            and self.text_down_flag is True
#        map = [c - c for c in range(0, len(self.__data_dict))]
        for e in self.__text_dict:
            for i in self.__text_dict[e][1:]:
                g = self.__data_dict.get(i)
                if g is not None:
                    self.__data_dict[i].append("TextUsedIt")
        ''' can not del elem during traversing '''
        for e in self.__data_dict:
            for i in self.__data_dict[e][1:]:
                g = self.__data_dict.get(i)
                if g is not None:
                    if g[-1] == "TextUsedIt":
                        g[-1] = "AllUsedIt"
                    else:
                        g.append("DataUsedIt")
        for e in self.__data_dict:
            elem = self.__data_dict[e][-1]
            if elem == "AllUsedIt" \
                or elem == "TextUsedIt" \
                    or elem == "DataUsedIt":
                continue
            else:
                self.unused[e] = self.__data_dict[e]

        print(self.unused)

    def deep_count(self):
        assert self.data_down_flag is True \
               and self.text_down_flag is True

    def start(self):
        self.__strip_data()
        self.__strip_text()

    def __strip_data(self):
        self.__strip(self.__DATA)

    def __strip_text(self):
        self.__strip(self.__TEXT)

    def __strip(self, strip_type):
        elem_id = ()
        elem = []
        assert strip_type == self.__DATA or strip_type == self.__TEXT
        if type == self.__DATA:
            lines = self.__data_file.readlines()
            dict_tmp = self.__data_dict
        else:
            lines = self.__text_file.readlines()
            dict_tmp = self.__text_dict

        for single_line in lines:
            if single_line.isspace():
                if elem:
                    dict_tmp[elem_id] = elem
                elem = []
                continue
            elif not re.findall(r'[0-9a-zA-Z_]+', single_line):
                continue
            first_world = re.findall(r'^[0-9a-zA-Z]+', single_line)
            second_world = re.findall(r'<[_a-zA-Z0-9.]+>', single_line)
            if first_world != [] and second_world != []:
                elem_id = int(first_world[0], base=16)
                elem.append(second_world[0].strip('<>'))
                continue
            content = single_line.split()
            elem.append(int(content[1], base=16))

        if type == self.__DATA:
            self.data_down_flag = True
        else:
            self.text_down_flag = True

    def dump_data(self):
        print(self.__data_dict)
        print(self.__text_dict)


''' class for processing .text section '''


class TextProcessObj:
    def __init__(self, data_file, text_file):
        self.__data_file = open(data_file, 'r')
        self.__text_file = open(text_file, 'r')
        self.__text_file_cut = '/tmp/text_fileCut_TextProcessObj'
        self.__data_dict = {}
        ''' self.__data_dict = {0 : ['', 0, 0, ...]} '''
        self.__text_dict = {}
        ''' self.__text_dict = {0 : ['', [0, ''], [0, ''], ...]} '''
        self.data_down_flag = False
        self.text_down_flag = False
        self.unused = {}

    def __del__(self):
        self.__data_file.close()
        self.__text_file.close()

    def cough_count(self):
        assert self.data_down_flag is True \
            and self.text_down_flag is True
#        map = [c - c for c in range(0, len(self.__data_dict))]
        for e in self.__data_dict:
            for i in self.__data_dict[e][1:]:
                g = self.__text_dict.get(i)
                if g is not None:
                    g.append('DataUsedIt')
        for e in self.__text_dict:
            for i in self.__text_dict[e][1:]:
                g = self.__data_dict.get(i[0])
                if g is not None:
                    if g[-1] == 'DataUsedIt':
                        g[-1] = 'AllUsedIt'
                    else:
                        g[-1] = 'TextUsedIt'
        for e in self.__text_dict:
            elem = self.__text_dict[e][-1]
            if elem == "AllUsedIt" \
                or elem == "TextUsedIt" \
                    or elem == "DataUsedIt":
                continue
            else:
                self.unused[e] = self.__text_dict[e]

        file_cut = open(self.__text_file_cut, 'w')
        for e in self.unused:
            file_cut.write('%s: %s\n' % (str(hex(e)), str(self.unused[e])))
        file_cut.close()

    def deep_count(self):
        assert self.data_down_flag is True \
               and self.text_down_flag is True

    def start(self):
        self.__strip_data()
        self.__strip_text()

    def __strip_data(self):
        elem_id = ()
        elem = []
        lines = self.__data_file.readlines()
        dict_tmp = self.__data_dict

        for single_line in lines:
            if single_line.isspace():
                if elem:
                    dict_tmp[elem_id] = elem
                elem = []
                continue
            elif not re.findall(r'[0-9a-zA-Z_]+', single_line):
                continue
            first_world = re.findall(r'^[0-9a-zA-Z]+', single_line)
            second_world = re.findall(r'<[_a-zA-Z0-9.]+>', single_line)
            if first_world != [] and second_world != []:
                elem_id = int(first_world[0], base=16)
                elem.append(second_world[0].strip('<>'))
                continue
            content = single_line.split()
            elem.append(int(content[1], base=16))

        self.data_down_flag = True

    def __strip_text(self):
        elem_id = ()
        elem = []
        lines = self.__text_file.readlines()
        dict_tmp = self.__text_dict

        for single_line in lines:
            if single_line.isspace():
                if elem:
                    dict_tmp[elem_id] = elem
                elem = []
                continue
            elif not re.findall(r'[0-9a-zA-Z]+', single_line):
                continue
            first_world = re.findall(r'^[0-9a-zA-Z]+', single_line)
            second_world = re.findall(r'<[_a-zA-Z0-9.]+>', single_line)
            if first_world != [] and second_world != []:
                elem_id = int(first_world[0], base=16)
                elem.append(second_world[0].strip('<>'))
                continue
            content = single_line.split()
            if content[2] == 'bl' and \
                    [] == re.findall(r'_[a-zA-Z_]+\+', content[4]):
                call_func_address = content[3]
                call_func_name = content[4].strip('<>')
                elem.append((int(call_func_address, base=16), call_func_name))

        self.text_down_flag = True

    def dump_data(self):
        print(self.__data_dict)
        print(self.__text_dict)


if __name__ == '__main__':
    final_args = [g_object_dump_tool_path, g_object_dump_args, sys.argv[1]]
    out_tmp_file_data = open(g_out_file_data, 'w')
    out_tmp_file_text = open(g_out_file_text, 'w')

    sub_process = subprocess.Popen(final_args, stdout=subprocess.PIPE)
    data_flag, dataGot = False, False
    text_flag, textGot = False, False
    line_token_data = g_object_dump_section_prompt + g_section_data
    line_token_text = g_object_dump_section_prompt + g_section_text
    while sub_process.poll() is None:
        line = sub_process.stdout.readline().decode('gbk')
        if line.find(line_token_data) != -1:
            data_flag, dataGot = True, True
            text_flag = False
            continue
        elif line.find(line_token_text) != -1:
            text_flag, textGot = True, True
            data_flag = False
            continue
        elif line.find(g_object_dump_section_prompt) != -1:
            text_flag = data_flag = False
            continue

        if data_flag is True:
            out_tmp_file_data.writelines(line)
        elif text_flag is True:
            out_tmp_file_text.writelines(line)

        if dataGot is True and data_flag is False \
                and textGot is True and text_flag is False:
            sub_process.kill()
            break

    out_tmp_file_data.close()
    out_tmp_file_text.close()

    DataProcessObj_v = DataProcessObj(g_out_file_data, g_out_file_text)
    DataProcessObj_v.start()
    DataProcessObj_v.cough_count()

    TextProcessObj_v = TextProcessObj(g_out_file_data, g_out_file_text)
    TextProcessObj_v.start()
    TextProcessObj_v.cough_count()
