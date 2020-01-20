import FilePrepare.sectionfileprepare as sec
import parameterobj as para
import copy
from Cache import cache
from os import path
import shutil
import gvars
import datetime


class FilterObj:
    def __init__(self, parameter_obj):
        assert type(parameter_obj) is para.ParameterObj, 'parameter error'
        self.parameter_obj = copy.deepcopy(parameter_obj)
        self.data_section_file_prepare_obj = sec.DataSectionFilePrepareObj(self.parameter_obj)
        self.text_section_file_prepare_obj = sec.TextSectionFilePrepareObj(self.parameter_obj)
        self.tag_file_prepare_obj = None
        self.process_obj = None
        self.tag_process_obj = None
        self.out_file = None
        # {'dir_level1' : 'name'}
        self.module_dict = {}
        # {'file_path' : 'name'}
        self.file_dict = {}
        self.hit_mark = '0'
        self._filter_cache = None
        self.assert_msg_dict_need_init = 'dictionary needs initialization first'

    @property
    def filter_cache(self):
        return self._filter_cache

    @filter_cache.setter
    def filter_cache(self, v: cache.FilterCache):
        if v.match_by_para(self.parameter_obj) is True:
            self._filter_cache = copy.deepcopy(v)

    @filter_cache.deleter
    def filter_cache(self):
        self.__filter_cache = None

    def __to_file(self):
        with open(self.out_file, 'w') as f:
            if self.parameter_obj.output_simple is False:
                for m in self.file_dict:
                    f.write('%s:\n' % m)
                    for p in self.file_dict[m]:
                        f.write('\t%s:\n' % p)
                        for i in self.file_dict[m][p]:
                            f.write('\t\t%s\n' % i)
                    f.write('\n\n')
            else:
                for e in self.module_dict:
                    f.write('%s:\n' % e)
                    for i in self.module_dict[e]:
                        f.write('\t%s\n' % i)
                    f.write('\n\n')
        if self._filter_cache is None:
            pass
#            cache_file = gvars.g_cache_fun_filtered_prefix + str(datetime.datetime.today().timestamp())
#            cache_file_path = path.abspath(path.expanduser(cache_file))
#            shutil.copyfile(self.out_file, cache_file_path)
#            cache_index_file_path = path.abspath(path.expanduser(gvars.g_cache_index_file))
#            with open(cache_index_file_path, 'w+') as f:
#                line = 'fun_filter ' + str(self.parameter_obj.executable) + ' ' + str(self.parameter_obj.directory) \
#                + ' None' + ' None' + ' None ' + cache_file
#                f.writelines(line)

    def _run(self):
        assert None not in [self.process_obj, self.tag_file_prepare_obj]
        if self._filter_cache is not None:
            p_str = path.abspath(path.expanduser(self._filter_cache.filter_path))
            shutil.copyfile(p_str, self.out_file)
            return
        data_section_mem_lines = self.data_section_file_prepare_obj.run()
        text_section_mem_lines = self.text_section_file_prepare_obj.run()
        if [data_section_mem_lines, text_section_mem_lines] != [[], []]:
            self.process_obj.set_mem_lines(data_section_mem_lines, text_section_mem_lines)
        tag_mem_lines = self.tag_file_prepare_obj.run()
        self.process_obj.run()
        self.process_obj.rough_count()
        if tag_mem_lines != []:
            self.tag_process_obj.set_mem_lines(tag_mem_lines)
        unused = self.process_obj.unused
        self.tag_process_obj.run()
        tag_dict = self.tag_process_obj.tag_dict
        for e in unused:
            g = tag_dict.get(unused[e][0])
            if g is not None:
                # mark the function which hit in the directories
                tag_dict[unused[e][0]].append(self.hit_mark)
        self.__final_trip()
        self.__to_file()

    # filter functions to the directory it belongs to
    def __final_trip(self):
        tag_dict = self.tag_process_obj.tag_dict
        for e in tag_dict:
            if tag_dict[e][-1] == self.hit_mark:
                if self.parameter_obj.output_simple is True:
                    model_name = tag_dict[e][0]
                    g = self.module_dict.get(model_name)
                    if g is None:
                        # got the first function in the directory
                        self.module_dict[model_name] = [e]
                    else:
                        self.module_dict[model_name].append(e)
                else:
                    # get the file path which the variable belongs to in the module
                    model_name = tag_dict[e][0]
                    file_name = tag_dict[e][1]
                    m = self.file_dict.get(model_name)
                    if m is None:
                        # Got the first file in the module
                        self.file_dict[model_name] = {file_name: [e]}
                    else:
                        g = self.file_dict[model_name].get(file_name)
                        if g is None:
                            # Got the first function in the file
                            self.file_dict[model_name][file_name] = [e]
                        else:
                            # Otherwise append to the variables list of the file
                            self.file_dict[model_name][file_name].append(e)
