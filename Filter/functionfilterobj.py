from Filter import filter
import gvars
import FilePrepare.tagfileprepare as tag
import Process.textprocess as text
import TagProcess.tagprocess as tp
from Cache.cache import FunFilterCache
from Cache import cacheelem, cache
from os import path
from pathlib import Path
import shutil
import datetime
import fcntl


class FunctionFilterObj(filter.FilterObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.out_file = gvars.g_function_out_file
        self.ctags_tmp_file = gvars.g_ctags_function_file_tmp
        self.process_obj = text.TextProcessObj(parameter_obj)
        self.tag_file_prepare_obj = tag.FunTagFilePrepareObj(parameter_obj)
        self.tag_process_obj = tp.FunTagProcess(parameter_obj)

    def __read_cache(self):
        cache_index = path.abspath(path.expanduser(gvars.g_cache_index_file))
        cache_index_path = Path(cache_index)
        if cache_index_path.exists():
            with open(cache_index, 'r') as f:
                fcntl.flock(f, fcntl.LOCK_SH)
                lines = f.readlines()
                fcntl.flock(f, fcntl.LOCK_UN)
                for single_line in lines:
                    elem_list = single_line.split()
                    if elem_list[0] == FunFilterCache.filter_index_type:
                        fun_filter_cache_elem = cacheelem.FunFilterCacheElem(
                            executable=elem_list[1], exe_timestamp=elem_list[2],
                            directory=elem_list[3], dir_timestamp=elem_list[4],
                            path_data_unused=elem_list[5],
                            path_text_unused=elem_list[6],
                            path_fun_tag_dict=elem_list[7],
                            path_var_filter=elem_list[8]
                        )
                        fun_filter_cache = FunFilterCache(fun_filter_cache_elem)
                        if fun_filter_cache.match_by_para(self.parameter_obj) is True:
                            self._filter_cache = fun_filter_cache
                            break

    def __write_cache(self):
        if self._filter_cache is None:
            fun_filter_cache_file = cache.FunFilterCache.filter_index_type + \
                                    str(datetime.datetime.today().timestamp())
            fun_filter_cache_file_path = path.abspath(path.expanduser(gvars.g_cache_dir + fun_filter_cache_file))
            shutil.copyfile(self.out_file, fun_filter_cache_file_path)
            cache_index_file_path = path.abspath(path.expanduser(gvars.g_cache_index_file))
            with open(cache_index_file_path, 'a') as f:
                cache_files = ['None', 'None', 'None', fun_filter_cache_file_path]
                line = cacheelem.FunFilterCacheElem.construct_index_line(self.parameter_obj, *cache_files)
                fcntl.flock(f, fcntl.LOCK_EX)
                f.writelines(line)
                f.flush()
                fcntl.flock(f, fcntl.LOCK_UN)

    def run(self):
        self.__read_cache()
        super(FunctionFilterObj, self)._run()
        self.__write_cache()
