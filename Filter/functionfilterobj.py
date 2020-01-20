from Filter import filter
import gvars
import FilePrepare.tagfileprepare as tag
import Process.textprocess as text
import TagProcess.tagprocess as tp
from Cache.cache import FunFilterCache


class FunctionFilterObj(filter.FilterObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.out_file = gvars.g_function_out_file
        self.ctags_tmp_file = gvars.g_ctags_function_file_tmp
        self.process_obj = text.TextProcessObj(parameter_obj)
        self.tag_file_prepare_obj = tag.FunTagFilePrepareObj(parameter_obj)
        self.tag_process_obj = tp.FunTagProcess(parameter_obj)

    def run(self, *cache: FunFilterCache):
        if cache.__len__() != 0:
            for e in cache:
                super()._run(e)
        else:
            super(FunctionFilterObj, self)._run()
