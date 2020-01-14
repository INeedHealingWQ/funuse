import re


# class for processing .text section
class TextProcessObj:
    def __init__(self, data_section_file, text_section_file):
        self.__data_section_file = open(data_section_file, 'r')
        self.__text_section_file = open(text_section_file, 'r')
        # self.__text_file_cut = '/tmp/textFileCut_textProcessObj'
        # self.__dict_out = '/tmp/dict_out'
        self.__data_dict = {}
        # self.__dataDict = {0 : ['', 0, 0, ...]}
        self.__text_dict = {}
        # self.__textDict = {0 : ['', [0, ''], [0, ''], ...]}
        self.data_down_flag = False
        self.text_down_flag = False
        self.unused = {}

    def __del__(self):
        self.__data_section_file.close()
        self.__text_section_file.close()

    def rough_count(self):
        assert self.data_down_flag is True \
               and self.text_down_flag is True
        for e in self.__data_dict:
            for i in self.__data_dict[e][1:]:
                g = self.__text_dict.get(i)
                if g is not None:
                    if g[-1] == '***TextUsedIt':
                        g[-1] = '***AllUsedIt'
                    elif g[-1] != '***DataUsedIt' and g[-1] != '***AllUsedIt':
                        g.append('***DataUsedIt')
        for e in self.__text_dict:
            for i in self.__text_dict[e][1:]:
                g = self.__text_dict.get(i[0])
                if g is not None:
                    if g[-1] == '***DataUsedIt':
                        g[-1] = '***AllUsedIt'
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
        # fcut = open(self.__text_file_cut, 'w')
        # for e in self.unused:
        #     fcut.write('%s: %s\n' % (str(hex(e)), str(self.unused[e])))
        # fcut.close()
        # dict_out = open(self.__dict_out, 'w')
        # for d in self.__text_dict:
        #     dict_out.write('%x-%s:\n' % (d, self.__text_dict[d][0]))
        #     for i in self.__text_dict[d][1:-1]:
        #         dict_out.write('\t%x-%s\n' % (i[0], i[1]))
        #     dict_out.write('%s\n' % self.__text_dict[d][-1])
        #     dict_out.write('\n')
        # dict_out.close()

    def deep_count(self):
        assert self.data_down_flag is True and self.text_down_flag is True

    def start_strip(self):
        self.__strip_data()
        self.__strip_text()

    def __strip_data(self):
        elem_id = ()
        elem = []
        lines = self.__data_section_file.readlines()
        local_dict = self.__data_dict

        for single_line in lines:
            if single_line.isspace():
                if elem:
                    local_dict[elem_id] = elem
                elem = []
                continue
            elif not re.findall(r'[0-9a-zA-Z_]+', single_line):
                continue
            first_word = re.findall(r'^[0-9a-zA-Z]+', single_line)
            second_word = re.findall(r'<[_a-zA-Z0-9.]+>', single_line)
            if first_word != [] and second_word != []:
                elem_id = int(first_word[0], base=16)
                elem.append(second_word[0].strip('<>'))
                continue
            content = single_line.split()
            elem.append(int(content[1], base=16))

        self.data_down_flag = True

    def __strip_text(self):
        elem_id = ()
        elem = []
        lines = self.__text_section_file.readlines()
        local_dict = self.__text_dict
        pre_elem_movw = None

        for single_line in lines:
            if single_line.isspace():
                if elem:
                    local_dict[elem_id] = elem
                    elem = []
                continue
            elif not re.findall(r'[0-9a-zA-Z]+', single_line):
                continue
            first_word = re.findall(r'^[0-9a-zA-Z]+', single_line)
            second_word = re.findall(r'<[_a-zA-Z0-9.]+>', single_line)
            if first_word != [] and second_word != []:
                elem_id = int(first_word[0], base=16)
                elem.append(second_word[0].strip('<>'))
                continue
            content = single_line.split()
            if content[2] == 'bl' and [] == re.findall(r'_[a-zA-Z_]+\+', content[4]):
                call_func_addr = content[3]
                call_func_name = content[4].strip('<>')
                elem.append([int(call_func_addr, base=16), call_func_name])
                pre_elem_movw = None
            elif content[2] == 'movw' or content[2] == 'movt':
                if content[2] == 'movw':
                    pre_elem_movw = int(content[4][1:], base=10)
                else:
                    if pre_elem_movw is not None:
                        cur_elem_movt = int(content[4][1:], base=10) << 16
                        address = pre_elem_movw + cur_elem_movt
                        name = '***UnRegName'
                        elem.append([address, name])
                    pre_elem_movw = None
            else:
                pre_elem_movw = None

        self.text_down_flag = True
