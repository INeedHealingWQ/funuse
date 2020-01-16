import gvars
from FilePrepare import fileprepare


class TagFilePrepareObj(fileprepare.FilePrepareObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.tool = parameter_obj.ctags_tool
        self.tool_args = [self.tool, *gvars.g_ctags_all_args, self.directory]

    def _prepare(self, file, sub_process):
        with open(file, 'w') as f:
            while sub_process.poll() is None:
                single_line = sub_process.stdout.readline().decode('ascii')
                if single_line.isspace() is True:
                    continue
                single_line_list = single_line.split()
                if len(single_line_list) < 2:
                    continue
                module_dir_str = single_line_list[1].partition(self.directory)[2]
                module_dir_str = module_dir_str.strip('/')
                module_dir_list = module_dir_str.split('/')
                module_dir = module_dir_list[0]
                c_file_path_in_module = '/'.join(module_dir_list[1:])
                var_name = single_line_list[0]
                write_line = var_name + ' ' + module_dir + ' ' + c_file_path_in_module + '\n'
                f.writelines(write_line)


class VarTagFilePrepareObj(TagFilePrepareObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.tool_args = [self.tool, *gvars.g_ctags_variable_args, self.directory]
        self.prepare_file_name = gvars.g_ctags_variable_file_tmp


class FunTagFilePrepareObj(TagFilePrepareObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.tool_args = [self.tool, *gvars.g_ctags_function_args, self.directory]
        self.prepare_file_name = gvars.g_ctags_function_file_tmp
