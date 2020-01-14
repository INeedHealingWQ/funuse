from gvars import *
import subprocess


# Prepare some temporary files for coming processing
class FilePrepare:
    def __init__(self):
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
            assert g_dump_tool is not None and g_executable is not None \
                   and g_directory is not None, self.assert_msg_global_args
            if section_type == self.DATA:
                self.objdump_data_section_final_args = \
                    [g_dump_tool, *g_objdump_data_section_args, g_executable]
            elif section_type == self.TEXT:
                self.objdump_text_section_final_args = \
                    [g_dump_tool, *g_objdump_text_section_args, g_executable]
            elif section_type == self.ALLSECTION:
                self.objdump_data_section_final_args = \
                    [g_dump_tool, *g_objdump_data_section_args, g_executable]
                self.objdump_text_section_final_args = \
                    [g_dump_tool, *g_objdump_text_section_args, g_executable]
            else:
                assert False, self.assert_msg_unrecognized_type
        elif tool_type == self.CTAGS:
            if section_type == self.DATA:
                self.ctags_variable_final_args = g_ctags_variable_args
            elif section_type == self.TEXT:
                self.ctags_function_final_args = g_ctags_function_args
            elif section_type == self.ALLSECTION:
                self.ctags_variable_final_args = g_ctags_variable_args
                self.ctags_function_final_args = g_ctags_function_args
            else:
                assert False, self.assert_msg_unrecognized_type
        elif tool_type == self.ALLTOOL:
            if section_type == self.DATA:
                self.objdump_data_section_final_args = \
                    [g_dump_tool, *g_objdump_data_section_args, g_executable]
                self.ctags_variable_final_args = g_ctags_variable_args
            elif section_type == self.TEXT:
                self.objdump_text_section_final_args = \
                    [g_dump_tool, *g_objdump_text_section_args, g_executable]
                self.ctags_function_final_args = g_ctags_function_args
            elif section_type == self.ALLSECTION:
                self.objdump_data_section_final_args = \
                    [g_dump_tool, *g_objdump_data_section_args, g_executable]
                self.ctags_variable_final_args = g_ctags_variable_args
                self.objdump_text_section_final_args = \
                    [g_dump_tool, *g_objdump_text_section_args, g_executable]
                self.ctags_function_final_args = g_ctags_function_args
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
                tag_list = single_line.split()
                up_dir = str(g_directory).split('/')
                if up_dir[-1] == '':
                    up_dir = up_dir[0:-1]
                dir_list = tag_list[1].split('/')
                dir_list = dir_list[dir_list.index(up_dir[-1]):]

                pass

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
