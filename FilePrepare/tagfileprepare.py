import gvars
from FilePrepare import fileprepare
from pathlib import Path


class TagFilePrepareObj(fileprepare.FilePrepareObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.tool = parameter_obj.ctags_tool
        self.tool_args = [self.tool, *gvars.g_ctags_all_args, str(self.directory)]
        self.tag_mark_letter = None

    def _prepare(self, file, sub_process):
        with open(file, 'w') as f:
            while True:
                single_line = sub_process.stdout.readline().decode('ascii')
                if single_line is '' and sub_process.poll() is not None:
                    break
                if single_line.isspace() is True:
                    continue
                single_line_list = single_line.split()
                if single_line_list == [] or \
                        single_line_list[-1] != self.tag_mark_letter:
                    continue
                path = Path(single_line_list[1])
                # should be function path match [vf]
                if path.is_file() is False:
                    continue
                # function name
                name = single_line_list[0]
                # file name: xxx.c
                file_path = str(path.relative_to(self.parameter_obj.directory))
                if self.parameter_obj.count_module is True:
                    module_name = self.parameter_obj.directory.name
                else:
                    relative_to_dir_tuple = path.relative_to(self.parameter_obj.directory).parts
                    if len(relative_to_dir_tuple) <= 1:
                        # only a c file, pass
                        continue
                    else:
                        module_name = relative_to_dir_tuple[0]
                write_line = name + ' ' + module_name + ' ' + file_path + '\n'
                f.writelines(write_line)


class VarTagFilePrepareObj(TagFilePrepareObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.tool_args = [self.tool, *gvars.g_ctags_variable_args, str(self.directory)]
        self.prepare_file_name = gvars.g_ctags_variable_file_tmp
        self.tag_mark_letter = 'v'


class FunTagFilePrepareObj(TagFilePrepareObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.tool_args = [self.tool, *gvars.g_ctags_function_args, str(self.directory)]
        self.prepare_file_name = gvars.g_ctags_function_file_tmp
        self.tag_mark_letter = 'f'
