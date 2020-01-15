import sys
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
        -a, --all       Print full information.
        -s, --simple    Brief output, only the top-level directories, this is the default argument.
        -v, --variable  Count the global variables which are not used.
        -f, --function  Count the function definition which are not used.
        -j, --jump      Use common ctags format for easy jumping
        -h, --help      Show help
        '''

    def start_parse(self):
        options_args, left_arguments = self.parse_opt(self.__argv)
        for o, a in options_args:
            if o in ['-t', '--dumptool']:
                self.__parameter_obj.objdump_tool = a
            elif o in ['-x', ['-executable']]:
                self.__parameter_obj.executable = a
            elif o in ['-d', ['--directory']]:
                self.__parameter_obj.directory = a
            elif o in ['-a', ['--all']]:
                self.__parameter_obj.output_all = True
                self.__parameter_obj.output_simple = False
                self.__parameter_obj.output_jump = False
            elif o in ['-s', ['--simple']]:
                self.__parameter_obj.output_simple = True
                self.__parameter_obj.output_all = False
                self.__parameter_obj.output_jump = False
            elif o in ['-v', '--variable']:
                self.__parameter_obj.count_variable = True
            elif o in ['-f', '--function']:
                self.__parameter_obj.count_function = True
            elif o in ['-j', '--jump']:
                self.__parameter_obj.output_jump = True
                self.__parameter_obj.output_all =  False
                self.__parameter_obj.output_simple = False
            elif o in ['-h', '--help']:
                self.usage()
                sys.exit(0)
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
