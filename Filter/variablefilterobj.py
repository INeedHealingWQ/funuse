from Filter import filter
import gvars
import FilePrepare.tagfileprepare as tag
import Process.dataprocess as data
import TagProcess.tagprocess as tp


class VariableFilterObj(filter.FilterObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.out_file = gvars.g_variable_out_file
        self.ctags_tmp_file = gvars.g_ctags_variable_file_tmp
        self.process_obj = data.DataProcessObj(parameter_obj)
        self.tag_file_prepare_obj = tag.VarTagFilePrepareObj(parameter_obj)
        self.tag_process_obj = tp.VarTagProcess(parameter_obj)

    def run(self):
        super()._run()
