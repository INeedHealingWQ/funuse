import sys, os
from pathlib import Path
import getopt
from gvars import *
from parameterobj import *

class CmdParseObj:
    def __init__(self, argv):
        self.__argv = argv[1:]
        self.__parameter_obj = ParameterObj()
        self.help_message = r'''
        Usage: funuse <option(s)> <path>
        All the following switches must be given:
        -t, --dumptool=<path>    Gnu binutil objdump tool path, this should be a system-wide path.   
        -x, --executable=<path>  The executable file path, this should be a system-wide path.
        -d, --directory=<path>   Count definitions under the directory.
            
        The following switches are optional:
        -m, --module    Count only a single module, then the -d option should followed by module path.
        -s, --simple    Brief output, only the top-level directories.
        -q, --quick     Quick mode, not write data to disk, this will use more memory.
        -v, --variable  Count the global variables which are not used.
        -f, --function  Count the function definition which are not used.
        -h, --help      Show help
        '''

    def elf_check(self):
        pass

    def start_parse(self):
        options_args, left_arguments = self.parse_opt(self.__argv)
        for o, a in options_args:
            if o in ['-t', '--dumptool']:
                self.__parameter_obj.objdump_tool = a
            elif o in ['-x', ['-executable']]:
                exe_str = os.path.expanduser(a)
                exe = Path(exe_str)
                if exe.is_file() is False or exe.suffix != '.exe':
                    print('%s should be an ELF-executable')
                    self.usage()
                    sys.exit()
                self.__parameter_obj.executable = exe
            elif o in ['-d', ['--directory']]:
                path_str = os.path.expanduser(a)
                path = Path(path_str)
                if path.is_dir() is False:
                    print('%s is not a directory.' % a)
                    self.usage()
                    sys.exit(0)
                # Transfer to absolute directory for further processing.
                self.__parameter_obj.directory = path
            elif o in ['-s', ['--simple']]:
                self.__parameter_obj.output_simple = True
            elif o in ['-v', '--variable']:
                self.__parameter_obj.count_variable = True
                self.__parameter_obj.count_function = False
            elif o in ['-f', '--function']:
                self.__parameter_obj.count_function = True
                self.__parameter_obj.count_variable = False
            elif o in ['-m', '--module']:
                self.__parameter_obj.count_module = True
            elif o in ['-h', '--help']:
                self.usage()
                sys.exit(0)
            elif o in ['-q', '--quick']:
                self.__parameter_obj.quick_mode = True
            else:
                assert False, 'unrecognized option\n'

        if self.__parameter_obj.update() is False:
            self.usage()
            sys.exit()

        return self.__parameter_obj

    def usage(self):
        print(self.help_message)

    def parse_opt(self, arg_list):
        try:
            opts_args, left_args = getopt.getopt(arg_list, g_short_options, g_long_options)
        except getopt.GetoptError as err:
            print(err)
            self.usage()
            sys.exit(2)
        return opts_args, left_args
