#!/usr/bin/python3

import sys
import Filter.functionfilterobj as ff
import Filter.variablefilterobj as vf
import funusecmd
from Cache import cache
from Cache import cacheelem
import gvars
from pathlib import Path
from os import mkdir
from os import path


def funuse_init():
    cache_dir = Path(path.abspath(path.expanduser(gvars.g_cache_dir)))
    if cache_dir.exists() is False:
        """Create cache directory if not exists"""
        mkdir(cache_dir)


if __name__ == '__main__':
    funuse_init()
    cmd_parse_obj = funusecmd.CmdParseObj(argv=sys.argv)
    parameter_obj = cmd_parse_obj.start_parse()
    cache_index = path.abspath(path.expanduser(gvars.g_cache_index_file))
#    if parameter_obj.count_variable is True:
#        filter_obj = vf.VariableFilterObj(parameter_obj)
#        filter_obj.run()
    fun_filter_cache = None
    cache_index_path = Path(cache_index)
    if cache_index_path.exists():
        with open(cache_index, 'r') as f:
            lines = f.readlines()
            for single_line in lines:
                elem_list = single_line.split()
                if elem_list[0] == 'fun_filter':
                    fun_filter_cache_elem = cacheelem.FunFilterCacheElem(elem_type=elem_list[0],
                                                                         executable=elem_list[1], exe_timestamp=[2],
                                                                         directory=elem_list[3], dir_timestamp=[4],
                                                                         path_data_unused=elem_list[5], path_text_unused=elem_list[6],
                                                                         path_fun_tag_dict=elem_list[7], path_var_filter=elem_list[8])
                    fun_filter_cache = cache.FunFilterCache(fun_filter_cache_elem)
    if parameter_obj.count_function is True:
        filter_obj = ff.FunctionFilterObj(parameter_obj)
        filter_obj.run(fun_filter_cache)
