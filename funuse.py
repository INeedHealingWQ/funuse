#!/usr/bin/python3

import sys
import Filter.functionfilterobj as ff
import Filter.variablefilterobj as vf
import funusecmd
import gvars
from pathlib import Path
from os import path


def funuse_init():
    cache_dir = Path(path.abspath(path.expanduser(gvars.g_cache_dir)))
    cache_index_file = Path(path.abspath(path.expanduser(gvars.g_cache_index_file)))
    if cache_dir.exists() is False:
        """Create cache directory if not exists"""
        try:
            cache_dir.mkdir(parents=True)
            if cache_index_file.exists() is False:
                """Create cache index file if not exists"""
                cache_index_file.touch()
        except PermissionError:
            'Create cache directory failed, may be you should use super-user privilege'


if __name__ == '__main__':
    funuse_init()
    cmd_parse_obj = funusecmd.CmdParseObj(argv=sys.argv)
    parameter_obj = cmd_parse_obj.start_parse()
    cache_index = path.abspath(path.expanduser(gvars.g_cache_index_file))
    if parameter_obj.count_variable is True:
        filter_obj = vf.VariableFilterObj(parameter_obj)
        filter_obj.run()
    if parameter_obj.count_function is True:
        filter_obj = ff.FunctionFilterObj(parameter_obj)
        filter_obj.run()
