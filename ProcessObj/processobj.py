import parameterobj
import gvars
import copy


class ProcessObj:
    def __init__(self, parameter_obj):
        assert type(parameter_obj) is parameterobj.ParameterObj
        self.parameter_obj = copy.deepcopy(parameter_obj)
        self.data_section_file = gvars.g_objdump_data_section_file_tmp
        self.text_section_file = gvars.g_objdump_text_section_file_tmp
        self.data_dict = {}
        # self.__data_dict = {0 : ['', 0, 0, ...]}
        self.text_dict = {}
        # self.__textDict = {0 : ['', [0, ''], [0, ''], ...]}
        self.data_down_flag = False
        self.text_down_flag = False
        self.data_used_it_mark = '0'
        self.text_used_it_mark = '1'
        self.all_used_it_mark = '2'

        self.unused = {}

    def rough_count(self):
        pass

    def deep_count(self):
        pass
