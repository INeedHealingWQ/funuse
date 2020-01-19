#!/usr/bin/python3

import sys
import Filter.functionfilterobj as ff
import Filter.variablefilterobj as vf
import funusecmd

if __name__ == '__main__':
    cmd_parse_obj = funusecmd.CmdParseObj(argv=sys.argv)
    parameter_obj = cmd_parse_obj.start_parse()
    if parameter_obj.count_variable is True:
        filter_obj = vf.VariableFilterObj(parameter_obj)
        filter_obj.run()
    if parameter_obj.count_function is True:
        filter_obj = ff.FunctionFilterObj(parameter_obj)
        filter_obj.run()
