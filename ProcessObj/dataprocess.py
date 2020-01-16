import re
import ProcessObj.processobj as pro


# class for processing .data section
class DataProcessObj(pro.ProcessObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

    def rough_count(self):
        for e in self.text_dict:
            for i in self.text_dict[e][1:]:
                g = self.data_dict.get(i)
                if g is not None:
                    self.data_dict[i].append(self.text_used_it_mark)
        # can not del elem during traversing, so we mark it
        for e in self.data_dict:
            for i in self.data_dict[e][1:]:
                g = self.data_dict.get(i)
                if g is not None:
                    if g[-1] == self.text_used_it_mark:
                        g[-1] = self.all_used_it_mark
                    else:
                        g.append(self.data_used_it_mark)
        for e in self.data_dict:
            elem = self.data_dict[e][-1]
            if elem in [self.all_used_it_mark,
                        self.data_used_it_mark, self.text_used_it_mark]:
                continue
            else:
                self.unused[e] = self.data_dict[e]

    def deep_count(self):
        assert [self.data_down_flag, self.text_down_flag] == [True, True]

    @staticmethod
    def __start_strip(strip_file, strip_dict):
        elem_id = ()
        elem = []
        with open(strip_file) as f:
            lines = f.readlines()

        for single_line in lines:
            if single_line.isspace():
                if elem:
                    strip_dict[elem_id] = elem
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

    def start_strip(self):
        self.__start_strip(self.data_section_file, self.data_dict)
        self.data_down_flag = True
        self.__start_strip(self.text_section_file, self.text_dict)
        self.text_down_flag = True
