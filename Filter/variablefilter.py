from Filter import filter
import gvars
import FilePrepare.tagfileprepare as tag


class VariableFilter(filter.FilterObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.out_file = gvars.g_variable_out_file
        self.ctags_tmp_file = gvars.g_ctags_variable_file_tmp
        self.process_obj = self.data_process_obj
        self.tag_file_prepare_obj = tag.VarTagFilePrepareObj(self.parameter_obj)

    def run(self):
        super()._run()
