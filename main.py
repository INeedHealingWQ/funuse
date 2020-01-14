#!/usr/bin/python3

from cmd import *
import threading
from filter import *
from fileprepare import *

if __name__ == '__main__':
    cmd_parse = CmdParse()
    file_prepare = FilePrepare()

    g_dump_tool, g_executable, g_directory = cmd_parse.start_parse(sys.argv)

    file_prepare.init_tool_args(file_prepare.ALLTOOL, file_prepare.ALLSECTION)

    data_section_t = threading.Thread(
        target=file_prepare.split_sections_to_file(file_prepare.DATA), name='DataSectionThread')
    text_section_t = threading.Thread(
        target=file_prepare.split_sections_to_file(file_prepare.TEXT), name='TextSectionThread')
    data_section_t.start()
    text_section_t.start()
    data_section_t.join()
    text_section_t.join()

    future = FilterObj(g_objdump_data_section_file_tmp, g_objdump_text_section_file_tmp)
    future.start()
