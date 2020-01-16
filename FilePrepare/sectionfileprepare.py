import gvars
from FilePrepare import fileprepare


class SectionFilePrepareObj(fileprepare.FilePrepareObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.tool = parameter_obj.objdump_tool

    def _prepare(self, file, sub_process):
        with open(file, 'w') as f:
            while sub_process.poll() is None:
                single_line = sub_process.stdout.readline().decode('ascii')
                res = single_line.find(gvars.g_objdump_section_prompt_string)
                if res != -1:
                    break
            while sub_process.poll() is None:
                f.writelines(sub_process.stdout.readline().decode('ascii'))


class DataSectionFilePrepareObj(SectionFilePrepareObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.tool_args = [self.tool, *gvars.g_objdump_data_section_args, self.executable]
        self.prepare_file_name = gvars.g_objdump_data_section_file_tmp


class TextSectionFilePrepareObj(SectionFilePrepareObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.tool_args = [self.tool, *gvars.g_objdump_text_section_args, self.executable]
        self.prepare_file_name = gvars.g_objdump_text_section_file_tmp
