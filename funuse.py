#!/usr/bin/python3

from cmd import *
import threading
from filter import *
from fileprepareobj import *

if __name__ == '__main__':
    cmd_parse_obj = CmdParseObj(argv=sys.argv)
    parameter_obj = cmd_parse_obj.start_parse()
    filter_obj = FilterObj(parameter_obj)

    file_prepare_obj = FilePrepareObj(parameter_obj)
    file_prepare_obj.init_tool_args()
    file_prepare_obj.prepare_tag_file()

    data_section_t = threading.Thread(
        target=file_prepare_obj.prepare_sections_file(), name='DataSectionThread')
    text_section_t = threading.Thread(
        target=file_prepare_obj.prepare_sections_file(), name='TextSectionThread')
    data_section_t.start()
    text_section_t.start()
    data_section_t.join()
    text_section_t.join()

    filter_obj.init_tag_dict()
    filter_obj.start_filter()
