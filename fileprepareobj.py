from gvars import *
import subprocess
from parameterobj import *
import copy


# Prepare some temporary files for coming processing
class FilePrepareObj:
    def __init__(self, parameter_obj):
        assert type(parameter_obj) is ParameterObj, 'parameter error'
        self.__parameter_obj = copy.deepcopy(parameter_obj)

        self.__dump_tool = parameter_obj.objdump_tool
        self.__ctags_tool = parameter_obj.ctags_tool
        self.__executable = parameter_obj.executable
        self.__directory = parameter_obj.directory
        self.__objdump_data_section_final_args = None
        self.__objdump_text_section_final_args = None
        self.__ctags_variable_final_args = None
        self.__ctags_function_final_args = None
        self.__assert_msg_objdump_data_args = \
            'data section arguments for objdump need initialization first to create sub process'
        self.__assert_msg_objdump_text_args = \
            'text section arguments for objdump need initialization first to create sub process'
        self.__assert_msg_ctags_variable_args = \
            'variable arguments for ctags need initialization first to create sub process'
        self.__assert_msg_ctags_function_args = \
            'function arguments for ctags need initialization first to create sub process'

    def init_tool_args(self):
        if self.__parameter_obj.count_variable is True:
            self.__objdump_data_section_final_args = \
                [self.__dump_tool, *g_objdump_data_section_args, self.__executable]
            self.__ctags_variable_final_args = \
                [self.__ctags_tool, *g_ctags_variable_args, self.__directory]
        if self.__parameter_obj.count_function is True:
            self.__objdump_text_section_final_args = \
                [self.__dump_tool, *g_objdump_text_section_args, self.__executable]
            self.__ctags_function_final_args = \
                [self.__ctags_tool, *g_ctags_function_args, self.__directory]

    def __prepare_tag_file(self, file, sub_process):
        assert file in [g_ctags_variable_file_tmp, g_ctags_function_file_tmp] \
            and type(sub_process) is subprocess.Popen
        with open(file, 'w') as f:
            while sub_process.poll() is None:
                single_line = sub_process.stdout.readline().decode('ascii')
                if single_line.isspace() is True:
                    continue
                single_line_list = single_line.split()
                module_dir_str = single_line_list[1].partition(self.__directory)[2]
                module_dir_str = module_dir_str.strip('/')
                module_dir_list = module_dir_str.split('/')
                module_dir = module_dir_list[0]
                c_file_path_in_module = '/'.join(module_dir_list[1:])
                var_name = single_line_list[0]
                write_line = var_name + ' ' + module_dir + ' ' + c_file_path_in_module + '\n'
                f.writelines(write_line)

    def prepare_tag_file(self):
        if self.__parameter_obj.count_variable is True:
            assert self.__ctags_variable_final_args is not None, self.__assert_msg_ctags_variable_args
            var_sub_process = subprocess.Popen(
                self.__ctags_variable_final_args, stdout=subprocess.PIPE
            )
            var_file_tmp = g_ctags_variable_file_tmp
            self.__prepare_tag_file(var_file_tmp, var_sub_process)
        if self.__parameter_obj.count_function is True:
            assert self.__ctags_function_final_args is not None, self.__assert_msg_ctags_function_args
            var_sub_process = subprocess.Popen(
                self.__ctags_function_final_args, stdout=subprocess.PIPE
            )
            var_file_tmp = g_ctags_function_file_tmp
            self.__prepare_tag_file(var_file_tmp, var_sub_process)

    @staticmethod
    def __prepare_sections_file(file, sub_process):
        assert file in [g_objdump_data_section_file_tmp, g_objdump_text_section_file_tmp] \
               and type(sub_process) is subprocess.Popen
        with open(file, 'w') as f:
            while sub_process.poll() is None:
                single_line = sub_process.stdout.readline().decode('ascii')
                res = single_line.find(g_objdump_section_prompt_string)
                if res != -1:
                    break
            while sub_process.poll() is None:
                f.writelines(sub_process.stdout.readline().decode('ascii'))

    # /tmp/outfile_data, /tmp/outfile_text
    def prepare_sections_file(self):
        if self.__parameter_obj.count_variable is True:
            assert self.__objdump_data_section_final_args is not None, self.__assert_msg_objdump_data_args
            section_sub_process = subprocess.Popen(
                self.__objdump_data_section_final_args, stdout=subprocess.PIPE
            )
            section_file_tmp = g_objdump_data_section_file_tmp
            self.__prepare_sections_file(section_file_tmp, section_sub_process)
        if self.__parameter_obj.count_function is True:
            assert self.__objdump_text_section_final_args is not None, self.__assert_msg_objdump_text_args
            section_sub_process = subprocess.Popen(
                self.__objdump_text_section_final_args, stdout=subprocess.PIPE
            )
            section_file_tmp = g_objdump_text_section_file_tmp
            self.__prepare_sections_file(section_file_tmp, section_sub_process)
