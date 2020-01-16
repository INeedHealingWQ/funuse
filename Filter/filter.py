import Process.dataprocess as data
import Process.textprocess as text
import FilePrepare.sectionfileprepare as sec
import parameterobj as para
import copy


class FilterObj:
    def __init__(self, parameter_obj):
        assert type(parameter_obj) is para.ParameterObj, 'parameter error'
        self.parameter_obj = copy.deepcopy(parameter_obj)
        self.data_process_obj = data.DataProcessObj(self.parameter_obj)
        self.text_process_obj = text.TextProcessObj(self.parameter_obj)
        self.data_section_file_prepare_obj = sec.DataSectionFilePrepareObj(self.parameter_obj)
        self.text_section_file_prepare_obj = sec.TextSectionFilePrepareObj(self.parameter_obj)
        self.process_obj = None
        self.tag_file_prepare_obj = None
        self.out_file = None
        self.ctags_tmp_file = None
        # {'name' : [dir_level1, 'dir_level2', ...]}
        self.tag_dict = {}
        # {'dir_level1' : 'name'}
        self.module_dict = {}
        # {'file_path' : 'name'}
        self.file_dict = {}
        self.assert_msg_dict_need_init = 'dictionary needs initialization first'

    def __init_tag_dict(self):
        assert self.ctags_tmp_file is not None
        with open(self.ctags_tmp_file, 'r') as f:
            ctags_lines = f.readlines()
        for single_line in ctags_lines:
            ctags_list = single_line.split()
            model_name = ctags_list[1]
            file_path = ctags_list[2]
            self.tag_dict[ctags_list[0]] = [model_name, file_path]

    def __to_file(self):
        with open(self.out_file, 'w') as f:
            if self.parameter_obj.output_all is True:
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

    def run(self):
        assert None not in [self.process_obj, self.tag_file_prepare_obj]
        self.data_section_file_prepare_obj.run()
        self.text_section_file_prepare_obj.run()
        self.tag_file_prepare_obj.run()
        self.process_obj.run()
        self.process_obj.rough_count()
        self.__init_tag_dict()
        unused = self.data_process_obj.unused
        for e in unused:
            g = self.tag_dict.get(unused[e][0])
            if g is not None:
                # mark the function which hit in the directories
                self.tag_dict[unused[e][0]].append('xxxhit')
        self.__final_trip()
        self.__to_file()

    # filter functions to the directory it belongs to
    def __final_trip(self):
        for e in self.tag_dict:
            if self.tag_dict[e][-1] == 'xxxhit':
                if self.parameter_obj.output_simple is True:
                    model_name = self.tag_dict[e][0]
                    g = self.module_dict.get(model_name)
                    if g is None:
                        # got the first function in the directory
                        self.module_dict[model_name] = [e]
                    else:
                        self.module_dict[model_name].append(e)
                elif self.parameter_obj.output_all is True:
                    # get the file path which the variable belongs to in the module
                    model_name = self.tag_dict[e][0]
                    file_name = self.tag_dict[e][1]
                    m = self.module_dict.get(model_name)
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