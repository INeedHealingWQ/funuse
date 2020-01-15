from ProcessObj.dataprocess import *
from ProcessObj.textprocess import *
from gvars import *
from parameterobj import *
import copy


class FilterObj:
    def __init__(self, parameter_obj):
        assert type(parameter_obj) is ParameterObj, 'parameter error'
        self.__parameter_obj = copy.deepcopy(parameter_obj)
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
        # {'file_path' : 'name'}
        self.__variable_file_dict = {}
        self.__function_file_dict = {}
        self.assert_msg_variable_dict_need_init = 'variable dictionary need initialization first'
        self.assert_msg_function_dict_need_init = 'function dictionary need initialization first'

    # filter functions to the directory it belongs to
    def __final_trip(self):
        if self.__parameter_obj.count_variable is True:
            for e in self.__variable_tag_dict:
                if self.__variable_tag_dict[e][-1] == 'xxxhit':
                    if self.__parameter_obj.output_simple is True:
                        model_name = self.__variable_tag_dict[e][0]
                        g = self.__variable_dir_dict.get(model_name)
                        if g is None:
                            # got the first function in the directory
                            self.__variable_dir_dict[model_name] = [e]
                        else:
                            self.__variable_dir_dict[model_name].append(e)
                    elif self.__parameter_obj.output_all is True:
                        # get the file path which the variable belongs to in the module
                        model_name = self.__variable_tag_dict[e][0]
                        file_name = self.__variable_tag_dict[e][1]
                        m = self.__variable_file_dict.get(model_name)
                        if m is None:
                            # Got the first file in the module
                            self.__variable_file_dict[model_name] = {file_name: [e]}
                        else:
                            g = self.__variable_file_dict[model_name].get(file_name)
                            if g is None:
                                # Got the first function in the file
                                self.__variable_file_dict[model_name][file_name] = [e]
                            else:
                                # Otherwise append to the variables list of the file
                                self.__variable_file_dict[model_name][file_name].append(e)
        if self.__parameter_obj.count_function is True:
            for e in self.__function_tag_dict:
                if self.__function_tag_dict[e][-1] == 'xxxhit':
                    if self.__parameter_obj.output_simple is True:
                        model_name = self.__function_tag_dict[e][0]
                        g = self.__function_dir_dict.get(model_name)
                        if g is None:
                            self.__function_dir_dict[model_name] = [e]
                        else:
                            # get the first function in the directory
                            self.__function_dir_dict[model_name].append(e)
                    if self.__parameter_obj.output_all is True:
                        model_name = self.__function_tag_dict[e][0]
                        file_name = self.__function_tag_dict[e][1]
                        m = self.__function_file_dict.get(model_name)
                        if m is None:
                            self.__function_file_dict[model_name] = {file_name: [e]}
                        else:
                            g = self.__function_file_dict[model_name].get(file_name)
                            if g is None:
                                self.__function_file_dict[model_name][file_name] = [e]
                            else:
                                self.__function_file_dict[model_name][file_name].append(e)

    # This must be called before start_filter
    def init_tag_dict(self):
        if self.__parameter_obj.count_variable is True:
            with open(self.__ctags_variable_file_tmp, 'r') as f:
                ctags_lines = f.readlines()
            for single_line in ctags_lines:
                ctags_list = single_line.split()
                model_name = ctags_list[1]
                file_path = ctags_list[2]
                self.__variable_tag_dict[ctags_list[0]] = [model_name, file_path]
        if self.__parameter_obj.count_function is True:
            with open(self.__ctags_function_file_tmp, 'r') as f:
                ctags_lines = f.readlines()
            for single_line in ctags_lines:
                ctags_list = single_line.split()
                model_name = ctags_list[1]
                file_path = ctags_list[2]
                self.__function_tag_dict[ctags_list[0]] = [model_name, file_path]

    def __to_file(self):
        if self.__parameter_obj.count_variable is True:
            with open(self.__variable_out_file, 'w') as f:
                if self.__parameter_obj.output_all is True:
                    for m in self.__variable_file_dict:
                        f.write('%s:\n' % m)
                        for p in self.__variable_file_dict[m]:
                            f.write('\t%s:\n' % p)
                            for i in self.__variable_file_dict[m][p]:
                                f.write('\t\t%s\n' % i)
                        f.write('\n\n')
                else:
                    for e in self.__variable_dir_dict:
                        f.write('%s:\n' % e)
                        for i in self.__variable_dir_dict[e]:
                            f.write('\t%s\n' % i)
                        f.write('\n\n')
        if self.__parameter_obj.count_function is True:
            with open(self.__function_out_file, 'w') as f:
                if self.__parameter_obj.output_all is True:
                    for m in self.__function_file_dict:
                        f.write('%s:\n' % m)
                        for p in self.__function_file_dict[m]:
                            f.write('\t%s:\n' % p)
                            for i in self.__function_file_dict[m][p]:
                                f.write('\t\t%s\n' % i)
                        f.write('\n\n')
                else:
                    for e in self.__function_dir_dict:
                        f.write('%s:\n' % e)
                        for i in self.__function_dir_dict[e]:
                            f.write('\t%s\n' % i)
                        f.write('\n\n')

    # This must be called after init_tag_list
    def start_filter(self):
        if self.__parameter_obj.count_variable is True:
            assert self.__variable_tag_dict, self.assert_msg_variable_dict_need_init
            self.__data_process_obj.start_strip()
            self.__data_process_obj.rough_count()
            unused = self.__data_process_obj.unused
            for e in unused:
                g = self.__variable_tag_dict.get(unused[e][0])
                if g is not None:
                    # mark the function which hit in the directories
                    self.__variable_tag_dict[unused[e][0]].append('xxxhit')
        if self.__parameter_obj.count_function is True:
            assert self.__function_tag_dict, self.assert_msg_function_dict_need_init
            self.__text_process_obj.start_strip()
            self.__text_process_obj.rough_count()
            unused = self.__text_process_obj.unused
            for e in unused:
                g = self.__function_tag_dict.get(unused[e][0])
                if g is not None:
                    # mark the function which hit in the directories
                    self.__function_tag_dict[unused[e][0]].append('xxxhit')
        self.__final_trip()
        self.__to_file()
