import gvars


class TagProcess:
    def __init__(self, parameter_obj):
        self.parameter_obj = parameter_obj
        # {'name' : [dir_level1, 'dir_level2', ...]}
        self.tag_dict = {}
        self.mem_lines = []
        self.tag_tmp_file = None

    def set_mem_lines(self, mem_lines):
        self.mem_lines = mem_lines

    def __init_tag_dict(self, ctags_src):
        if type(ctags_src) is list:
            ctags_lines = ctags_src
        elif type(ctags_src) is str:
            assert self.tag_tmp_file is not None
            with open(self.tag_tmp_file, 'r') as f:
                ctags_lines = f.readlines()
        else:
            assert False, 'Unknown type'

        for single_line in ctags_lines:
            ctags_list = single_line.split()
            name = ctags_list[0]
            model_name = ctags_list[1]
            file_path = ctags_list[2]
            self.tag_dict[name] = [model_name, file_path]

    def _run(self):
        if self.mem_lines:
            tag_src = self.mem_lines
        else:
            tag_src = self.tag_tmp_file
        self.__init_tag_dict(tag_src)


class VarTagProcess(TagProcess):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)
        self.tag_tmp_file = gvars.g_ctags_variable_file_tmp

    def run(self):
        super()._run()


class FunTagProcess(TagProcess):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)
        self.tag_tmp_file = gvars.g_ctags_function_file_tmp

    def run(self):
        super()._run()
