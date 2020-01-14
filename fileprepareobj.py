from gvars import *
import subprocess


# Prepare some temporary files for coming processing
class FilePrepareObj:
    def __init__(self, objdump_tool=None, ctags_tool='ctags', executable=None, directory=None):
        self.dump_tool = objdump_tool
        self.ctags_tool = ctags_tool
        self.executable = executable
        self.directory = directory
        self.DATA = 1
        self.TEXT = 2
        self.ALLSECTION = 3
        self.OBJDUMP = 1
        self.CTAGS = 2
        self.ALLTOOL = 3
        self.objdump_data_section_final_args = None
        self.objdump_text_section_final_args = None
        self.ctags_variable_final_args = None
        self.ctags_function_final_args = None
        self.assert_msg_global_args = 'global arguments need initialization first'
        self.assert_msg_unrecognized_tool = 'unrecognized tool type'
        self.assert_msg_unrecognized_type = 'unrecognized section type'
        self.assert_msg_objdump_data_args = \
            'data section arguments for objdump need initialization first to create sub process'
        self.assert_msg_objdump_text_args = \
            'text section arguments for objdump need initialization first to create sub process'
        self.assert_msg_ctags_variable_args = \
            'variable arguments for ctags need initialization first to create sub process'
        self.assert_msg_ctags_function_args = \
            'function arguments for ctags need initialization first to create sub process'

    def init_tool_args(self, tool_type, section_type):
        if tool_type == self.OBJDUMP:
            if section_type == self.DATA:
                self.objdump_data_section_final_args = \
                    [self.dump_tool, *g_objdump_data_section_args, self.executable]
            elif section_type == self.TEXT:
                self.objdump_text_section_final_args = \
                    [self.dump_tool, *g_objdump_text_section_args, self.executable]
            elif section_type == self.ALLSECTION:
                self.objdump_data_section_final_args = \
                    [self.dump_tool, *g_objdump_data_section_args, self.executable]
                self.objdump_text_section_final_args = \
                    [self.dump_tool, *g_objdump_text_section_args, self.executable]
            else:
                assert False, self.assert_msg_unrecognized_type
        elif tool_type == self.CTAGS:
            if section_type == self.DATA:
                self.ctags_variable_final_args = \
                    [self.ctags_tool, *g_ctags_variable_args, self.directory]
            elif section_type == self.TEXT:
                self.ctags_function_final_args = \
                    [self.ctags_tool, *g_ctags_function_args, self.directory]
            elif section_type == self.ALLSECTION:
                self.ctags_variable_final_args = \
                    [self.ctags_tool, *g_ctags_variable_args, self.directory]
                self.ctags_function_final_args = \
                    [self.ctags_tool, *g_ctags_function_args, self.directory]
            else:
                assert False, self.assert_msg_unrecognized_type
        elif tool_type == self.ALLTOOL:
            if section_type == self.DATA:
                self.objdump_data_section_final_args = \
                    [self.dump_tool, *g_objdump_data_section_args, self.executable]
                self.ctags_variable_final_args = \
                    [self.ctags_tool, *g_ctags_variable_args, self.executable]
            elif section_type == self.TEXT:
                self.objdump_text_section_final_args = \
                    [self.dump_tool, *g_objdump_text_section_args, self.executable]
                self.ctags_function_final_args = \
                    [self.ctags_tool, *g_ctags_function_args, self.directory]
            elif section_type == self.ALLSECTION:
                self.objdump_data_section_final_args = \
                    [self.dump_tool, *g_objdump_data_section_args, self.executable]
                self.objdump_text_section_final_args = \
                    [self.dump_tool, *g_objdump_text_section_args, self.executable]
                self.ctags_variable_final_args = \
                    [self.ctags_tool, *g_ctags_variable_args, self.directory]
                self.ctags_function_final_args = \
                    [self.ctags_tool, *g_ctags_function_args, self.directory]
        else:
            assert False, self.assert_msg_unrecognized_tool

    def init_tag_file(self, section_type):
        if section_type == self.DATA:
            assert self.ctags_variable_final_args is not None, self.assert_msg_ctags_variable_args
            var_sub_process = subprocess.Popen(
                self.ctags_variable_final_args, stdout=subprocess.PIPE
            )
            var_file_tmp = g_ctags_variable_file_tmp
        elif section_type == self.TEXT:
            assert self.ctags_function_final_args is not None, self.assert_msg_ctags_function_args
            var_sub_process = subprocess.Popen(
                self.ctags_function_final_args, stdout=subprocess.PIPE
            )
            var_file_tmp = g_ctags_function_file_tmp
        else:
            assert False, self.assert_msg_unrecognized_type

        with open(var_file_tmp, 'w') as f:
            while var_sub_process.poll() is None:
                single_line = var_sub_process.stdout.readline().decode('ascii')
                if single_line.isspace() is True:
                    continue
                print(single_line)
                single_line_list = single_line.split()
                model_dir_list = single_line_list[1].partition(self.directory)[2]
                model_dir_list = model_dir_list.split('/')
                if model_dir_list[0] == '':
                    model_dir = model_dir_list[1]
                else:
                    model_dir = model_dir_list[0]
                var_name = single_line_list[0]
                write_line = var_name + ' ' + model_dir
                f.writelines(write_line)

    # /tmp/outfile_data, /tmp/outfile_text
    def split_sections_to_file(self, section_type):
        if section_type == self.DATA:
            assert self.objdump_data_section_final_args is not None, self.assert_msg_objdump_data_args
            section_sub_process = subprocess.Popen(
                self.objdump_data_section_final_args, stdout=subprocess.PIPE
            )
            section_file_tmp = g_objdump_data_section_file_tmp
        elif section_type == self.TEXT:
            assert self.objdump_text_section_final_args is not None, self.assert_msg_objdump_text_args
            section_sub_process = subprocess.Popen(
                self.objdump_text_section_final_args, stdout=subprocess.PIPE
            )
            section_file_tmp = g_objdump_text_section_file_tmp
        else:
            assert False, self.assert_msg_unrecognized_type

        with open(section_file_tmp, 'w') as f:
            while section_sub_process.poll() is None:
                single_line = section_sub_process.stdout.readline().decode('ascii')
                res = single_line.find(g_objdump_section_prompt_string)
                if res != -1:
                    break
            while section_sub_process.poll() is None:
                f.writelines(section_sub_process.stdout.readline().decode('ascii'))
