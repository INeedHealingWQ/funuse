from Filter import filter
import gvars
import FilePrepare.tagfileprepare as tag


class FunctionFilter(filter.FilterObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.out_file = gvars.g_function_out_file
        self.ctags_tmp_file = gvars.g_ctags_function_file_tmp
        self.process_obj = self.text_process_obj
        self.tag_file_prepare_obj = tag.FunTagFilePrepareObj(self.parameter_obj)
