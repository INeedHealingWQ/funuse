

class ParameterObj:
    def __init__(self, *, executable = None, directory = None):
        self.objdump_tool = '/opt/toolchain/iProcLDK_3.4.6/usr/bin/arm-linux-objdump'
        self.ctags_tool = 'ctags'
        self.executable = executable
        self.directory = directory

        self.output_simple = False
        self.count_variable = True
        self.count_function = True
        self.count_module = False

        self.quick_mode = False

    def update(self):
        if None in [self.objdump_tool, self.ctags_tool, self.executable, self.directory]:
            return False
        return True
