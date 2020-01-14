from ProcessObj.dataprocess import *
from ProcessObj.textprocess import *
from gvars import *


class FilterObj:
    def __init__(self):
        self.__variable_out_file = g_variable_out_file
        self.__function_out_file = g_function_out_file
        self.__ctags_variable_file_tmp = g_ctags_variable_file_tmp
        self.__ctags_function_file_tmp = g_ctags_function_file_tmp
        self.__objdump_data_section_file_tmp = g_objdump_data_section_file_tmp
        self.__objdump_text_section_file_tmp = g_objdump_text_section_file_tmp
        self.__data_process_obj = DataProcessObj(
            data_section_file=self.__objdump_data_section_file_tmp,
            text_section_file=self.__objdump_text_section_file_tmp
        )
        self.__text_process_obj = TextProcessObj(
            data_section_file=self.__objdump_data_section_file_tmp,
            text_section_file=self.__objdump_text_section_file_tmp)
        # {'name' : [dir_level1, 'dir_level2', ...]}
        self.__variable_tag_dict = {}
        self.__function_tag_dict = {}
        # {'dir_level1' : 'name'}
        self.__variable_dir_dict = {}
        self.__function_dir_dict = {}
        self.VAR = (1, 0)
        self.FUN = (0, 1)
        self.ALL = (1, 1)
        self.assert_msg_unrecognized_kind = 'unrecognized kind'

    # filter functions to the directory it belongs to
    def final_trip(self, kind):
        assert kind == self.VAR or kind == self.FUN or \
               kind == self.ALL, self.assert_msg_unrecognized_kind
        if kind[0] == 1:
            for e in self.__variable_tag_dict:
                if self.__variable_tag_dict[e][-1] == 'xxxhit':
                    model_name = self.__variable_tag_dict[e][0]
                    g = self.__variable_dir_dict.get(model_name)
                    if g is None:
                        self.__variable_dir_dict[model_name] = [e]
                    else:
                        # get the first function in the directory
                        self.__variable_dir_dict[model_name].append(e)
        if kind[1] == 1:
            for e in self.__function_tag_dict:
                if self.__function_tag_dict[e][-1] == 'xxxhit':
                    model_name = self.__function_tag_dict[e][0]
                    g = self.__function_dir_dict.get(model_name)
                    if g is None:
                        self.__function_dir_dict[model_name] = [e]
                    else:
                        # get the first function in the directory
                        self.__function_dir_dict[model_name].append(e)

    def init_tag_dict(self, kind):
        assert kind == self.VAR or kind == self.FUN or \
            kind == self.ALL, self.assert_msg_unrecognized_kind
        if kind[0] == 1:
            with open(self.__ctags_variable_file_tmp, 'r') as f:
                ctags_lines = f.readlines()
            for single_line in ctags_lines:
                ctags_list = single_line.split()
                model_name = ctags_list[1]
                self.__variable_tag_dict[ctags_list[0]] = model_name
        if kind[1] == 1:
            with open(self.__ctags_function_file_tmp, 'r') as f:
                ctags_lines = f.readlines()
            for single_line in ctags_lines:
                ctags_list = single_line.split()
                model_name = ctags_list[1]
                self.__function_tag_dict[ctags_list[0]] = model_name

    def start_filter(self, kind):
        assert kind == self.VAR or kind == self.FUN or \
               kind == self.ALL, self.assert_msg_unrecognized_kind
        if kind[0] == 1:
            self.__data_process_obj.start_strip()
            self.__data_process_obj.rough_count()
            unused = self.__data_process_obj.unused
            for e in unused:
                g = self.__variable_tag_dict.get(unused[e][0])
                if g is not None:
                    # mark the function which hit in the directories
                    self.__variable_tag_dict[unused[e][0]].append('xxxhit')
            self.final_trip()
            with open(self.__variable_out_file, 'w') as f:
                for e in self.__variable_dir_dict:
                    f.write('%s:\n' % e)
                    for i in self.__variable_dir_dict[e]:
                        f.write('\t%s\n' % i)
                    f.write('\n\n')
        if kind[1] == 1:
            self.__text_process_obj.start_strip()
            self.__text_process_obj.rough_count()
            unused = self.__text_process_obj.unused
            for e in unused:
                g = self.__function_tag_dict.get(unused[e][0])
                if g is not None:
                    # mark the function which hit in the directories
                    self.__function_tag_dict[unused[e][0]].append('xxxhit')
            self.final_trip()
            with open(self.__function_out_file, 'w') as f:
                for e in self.__function_dir_dict:
                    f.write('%s:\n' % e)
                    for i in self.__function_dir_dict[e]:
                        f.write('\t%s\n' % i)
                    f.write('\n\n')
