import parameterobj
import gvars
import copy


class ProcessObj:
    def __init__(self, parameter_obj):
        assert type(parameter_obj) is parameterobj.ParameterObj
        self.__parameter_obj = copy.deepcopy(parameter_obj)
        self.__data_section_file = gvars.g_objdump_data_section_file_tmp
        self.__text_section_file = gvars.g_objdump_text_section_file_tmp
        self.__data_dict = {}
        # self.__data_dict = {0 : ['', 0, 0, ...]}
        self.__text_dict = {}
        # self.__textDict = {0 : ['', [0, ''], [0, ''], ...]}
        self.data_down_flag = False
        self.text_down_flag = False
        self.__data_used_it_mark = '1'
        self.__text_used_it_mark = '0'
        self.__all_used_it_mark = '2'

        self.unused = {}

    def rough_count(self):
        pass