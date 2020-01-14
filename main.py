#!/usr/bin/python3

from cmd import *
import threading
from filter import *
from fileprepareobj import *

if __name__ == '__main__':
    cmd_parse_obj = CmdParseObj()

    dump_tool, executable, directory = cmd_parse_obj.start_parse(sys.argv)

    file_prepare_obj = FilePrepareObj(objdump_tool=dump_tool, executable=executable, directory=dump_tool)
    file_prepare_obj.init_tool_args(file_prepare_obj.ALLTOOL, file_prepare_obj.ALLSECTION)

    data_section_t = threading.Thread(
        target=file_prepare_obj.split_sections_to_file(file_prepare_obj.DATA), name='DataSectionThread')
    text_section_t = threading.Thread(
        target=file_prepare_obj.split_sections_to_file(file_prepare_obj.TEXT), name='TextSectionThread')
#    function_t = threading.Thread(
#        target=filter_obj.start_filter(kind=filter_obj.FUN), name='FunctionThread')
#    data_section_t.start()
#    text_section_t.start()
#    data_section_t.join()
#    text_section_t.join()

    file_prepare_obj.init_tag_file(file_prepare_obj.TEXT)
    filter_obj = FilterObj()
    filter_obj.init_tag_dict(kind=filter_obj.FUN)
    filter_obj.start_filter(kind=filter_obj.FUN)
