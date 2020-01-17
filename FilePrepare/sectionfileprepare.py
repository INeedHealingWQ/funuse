import gvars
from FilePrepare import fileprepare


class SectionFilePrepareObj(fileprepare.FilePrepareObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.tool = parameter_obj.objdump_tool

    def _prepare(self, file, sub_process):
        section_lines = []
        with open(file, 'w') as f:
            while True:
                single_line = sub_process.stdout.readline().decode('ascii')
                if single_line is '' and sub_process.poll() is not None:
                    break
                if single_line.find(gvars.g_objdump_section_prompt_string) != -1:
                    continue
                if self.parameter_obj.quick_mode is True:
                    section_lines.append(single_line)
                else:
                    f.writelines(single_line)
        return section_lines

class DataSectionFilePrepareObj(SectionFilePrepareObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.tool_args = [self.tool, *gvars.g_objdump_data_section_args, str(self.executable)]
        self.prepare_file_name = gvars.g_objdump_data_section_file_tmp


class TextSectionFilePrepareObj(SectionFilePrepareObj):
    def __init__(self, parameter_obj):
        super().__init__(parameter_obj)

        self.tool_args = [self.tool, *gvars.g_objdump_text_section_args, str(self.executable)]
        self.prepare_file_name = gvars.g_objdump_text_section_file_tmp
