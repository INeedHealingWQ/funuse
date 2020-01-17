#!/usr/bin/python3

import sys
import Filter.functionfilter as ff
import Filter.variablefilter as vf
import funusecmd

if __name__ == '__main__':
    cmd_parse_obj = funusecmd.CmdParseObj(argv=sys.argv)
    parameter_obj = cmd_parse_obj.start_parse()
    if parameter_obj.count_variable is True:
        filter_obj = vf.VariableFilter(parameter_obj)
        filter_obj.run()
    if parameter_obj.count_function is True:
        filter_obj = ff.FunctionFilter(parameter_obj)
        filter_obj.run()
