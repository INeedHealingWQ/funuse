import re


# class for processing .data section
class DataProcessObj:
    def __init__(self, data_section_file, text_section_file):
        self.__DATA = 0
        self.__TEXT = 1
        self.__data_section_file = data_section_file
        self.__text_section_file = text_section_file
        self.__data_dict = {}
        # self.__data_dict = {0 : ['', 0, 0, ...]}
        self.__text_dict = {}
        # self.__textDict = {0 : ['', [0, ''], [0, ''], ...]}
        self.data_down_flag = False
        self.text_down_flag = False
        self.unused = {}

    def rough_count(self):
        assert self.data_down_flag is True \
               and self.text_down_flag is True
        for e in self.__text_dict:
            for i in self.__text_dict[e][1:]:
                g = self.__data_dict.get(i)
                if g is not None:
                    self.__data_dict[i].append("***TextUsedIt")
        # can not del elem during traversing, so we mark it
        for e in self.__data_dict:
            for i in self.__data_dict[e][1:]:
                g = self.__data_dict.get(i)
                if g is not None:
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

    def start_strip(self):
        self.__strip_data()
        self.__strip_text()

    def __strip_data(self):
        self.__strip(self.__DATA)

    def __strip_text(self):
        self.__strip(self.__TEXT)

    def __strip(self, section_type):
        elem_id = ()
        elem = []
        lines = None
        local_dict = {}

        assert section_type == self.__DATA or section_type == self.__TEXT
        if section_type == self.__DATA:
            f = open(self.__data_section_file, 'r')
            lines = f.readlines()
            f.close()
            local_dict = self.__data_dict
        elif section_type == self.__TEXT:
            f = open(self.__text_section_file, 'r')
            lines = f.readlines()
            f.close()
            local_dict = self.__text_dict

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

        if section_type == self.__DATA:
            self.data_down_flag = True
        elif section_type == self.__TEXT:
            self.text_down_flag = True

    def dump_data(self):
        print(self.__data_dict)
        print(self.__text_dict)
