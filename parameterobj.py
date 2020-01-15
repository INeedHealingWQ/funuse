

class ParameterObj:
    def __init__(self):
        self.objdump_tool = '/opt/toolchain/iProcLDK_3.4.6/usr/bin/arm-linux-objdump'
        self.ctags_tool = 'ctags'
        self.executable = None
        self.directory = None

        self.output_all = True
        self.output_simple = False
        self.output_jump = False
        self.count_variable = True
        self.count_function = True

    def update(self):
        if None in [self.objdump_tool, self.ctags_tool, self.executable, self.directory]:
            return False
        if [self.output_simple, self.output_all, self.output_jump].count(True) != 1:
            return False
        return True
