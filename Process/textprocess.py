import re
import Process.process as pro


# class for processing .text section
class TextProcessObj(pro.ProcessObj):
    def __init__(self, parameter_object):
        super().__init__(parameter_object)
        self.__unrecognized_mark = '3'

    def rough_count(self):
        assert self.data_down_flag is True \
               and self.text_down_flag is True
        for e in self.data_dict:
            for i in self.data_dict[e][1:]:
                g = self.text_dict.get(i)
                if g is not None:
                    if g[-1] == self.text_used_it_mark:
                        g[-1] = self.all_used_it_mark
                    elif g[-1] != self.data_used_it_mark and g[-1] != self.all_used_it_mark:
                        g.append(self.data_used_it_mark)
        for e in self.text_dict:
            for i in self.text_dict[e][1:]:
                g = self.text_dict.get(i[0])
                if g is not None:
                    if g[-1] == self.data_used_it_mark:
                        g[-1] = self.all_used_it_mark
                    elif g[-1] != self.text_used_it_mark and g[-1] != self.all_used_it_mark:
                        g.append(self.text_used_it_mark)
        for e in self.text_dict:
            elem = self.text_dict[e][-1]
            if elem in [self.all_used_it_mark,
                        self.data_used_it_mark, self.text_used_it_mark]:
                continue
            else:
                self.unused[e] = self.text_dict[e]

    def deep_count(self):
        assert self.data_down_flag is True and self.text_down_flag is True

    def run(self):
        self.__strip_data()
        self.__strip_text()

    def __strip_data(self):
        elem_id = ()
        elem = []
        if self.data_mem_lines:
            lines = self.data_mem_lines
        else:
            with open(self.data_section_file, 'r') as f:
                lines = f.readlines()
        local_dict = self.data_dict

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
        if self.text_mem_lines:
            lines = self.text_mem_lines
        else:
            with open(self.text_section_file, 'r') as f:
                lines = f.readlines()
        local_dict = self.text_dict
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
                        elem.append([address, self.__unrecognized_mark])
                    pre_elem_movw = None
            else:
                pre_elem_movw = None

        self.text_down_flag = True
