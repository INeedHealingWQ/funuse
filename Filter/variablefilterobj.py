from Filter import filter
import gvars
import FilePrepare.tagfileprepare as tag
import Process.dataprocess as data
import TagProcess.tagprocess as tp
from Cache.cache import VarFilterCache
from Cache import cacheelem, cache
from os import path
from pathlib import Path
import shutil
import datetime


class VariableFilterObj(filter.FilterObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.out_file = gvars.g_variable_out_file
        self.ctags_tmp_file = gvars.g_ctags_variable_file_tmp
        self.process_obj = data.DataProcessObj(parameter_obj)
        self.tag_file_prepare_obj = tag.VarTagFilePrepareObj(parameter_obj)
        self.tag_process_obj = tp.VarTagProcess(parameter_obj)

    def __read_cache(self):
        cache_index = path.abspath(path.expanduser(gvars.g_cache_index_file))
        cache_index_path = Path(cache_index)
        if cache_index_path.exists():
            with open(cache_index, 'r') as f:
                lines = f.readlines()
                for single_line in lines:
                    elem_list = single_line.split()
                    if elem_list[0] == VarFilterCache.filter_index_type:
                        var_filter_cache_elem = cacheelem.VarFilterCacheElem(executable=elem_list[1], exe_timestamp=elem_list[2],
                                                                             directory=elem_list[3], dir_timestamp=elem_list[4],
                                                                             path_data_unused=elem_list[5],
                                                                             path_text_unused=elem_list[6],
                                                                             path_var_tag_dict=elem_list[7],
                                                                             path_var_filter=elem_list[8])
                        var_filter_cache = VarFilterCache(var_filter_cache_elem)
                        if var_filter_cache.match_by_para(self.parameter_obj) is True:
                            self._filter_cache = var_filter_cache
                            break

    def __write_cache(self):
        if self._filter_cache is None:
            var_filter_cache_file = cache.VarFilterCache.filter_index_type + \
                                    str(datetime.datetime.today().timestamp())
            var_filter_cache_file_path = path.abspath(path.expanduser(gvars.g_cache_dir + var_filter_cache_file))
            shutil.copyfile(self.out_file, var_filter_cache_file_path)
            cache_index_file_path = path.abspath(path.expanduser(gvars.g_cache_index_file))
            with open(cache_index_file_path, 'a') as f:
                cache_files = ['None', 'None', 'None', var_filter_cache_file_path]
                line = cacheelem.VarFilterCacheElem.construct_index_line(self.parameter_obj, *cache_files)
                f.writelines(line)

    def run(self):
        self.__read_cache()
        super(VariableFilterObj, self)._run()
        self.__write_cache()
