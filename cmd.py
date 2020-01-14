import sys
import getopt
from gvars import *

class CmdParse:
    def __init__(self):
        self.help_message = r'''
        Usage: funuse <option(s)> <path>
        All the following switches must be given:
        -t, --dumptool=<path>    Gnu binutil objdump tool path, this should be a system-wide path.   
        -x, --executable=<path>  The executable file path, this should be a system-wide path.
        -d, --directory=<path>   Count definitions under the directory.
            
        The following switches are optional:
        -a, --all       Print full information, this is the default argument.
        -s, --simple    Brief output, only the top-level directories
        -v, --variable  Count the global variables which are not used.
        -f, --function  Count the function definition which are not used.
        -j, --jump      Use common ctags format for easy jumping
        '''

    def start_parse(self, argv):
        options_args, left_arguments = self.parse_opt(argv[1:])
        dump_tool = None
        executable = None
        directory = None
        for o, a in options_args:
            if o in ['-t', '--dumptool']:
                dump_tool = a
            elif o in ['-x', ['-executable']]:
                executable = a
            elif o in ['-d', ['--directory']]:
                directory = a
            else:
                assert False, 'unrecognized option: %s\n' % o

        if dump_tool is None or executable is None or directory is None:
            self.usage()
            sys.exit()

        return dump_tool, executable, directory

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
