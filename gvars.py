# some common arguments of objdump and temporary files for storing tmp data '''
g_objdump_data_section_args = ['-D', '-j.data']
g_objdump_text_section_args = ['-D', '-j.text']
g_objdump_data_section_file_tmp = '/tmp/outfile_data'
g_objdump_text_section_file_tmp = '/tmp/outfile_text'
g_objdump_section_prompt_string = 'Disassembly of section'

# command line options
g_short_options = "vft:x:d:shm"
g_long_options = ["variable", "function", "module", "help", "dumptool=", "executable=", "directory="]
g_necessary_opts_s = ['-t', '-x', '-d']
g_necessary_opts_l = ['--dumptool', '--executable', '--directory']
g_necessary_opts = [['-t', '--dumptool'], ['-x', '--executable'], ['-d', '--directory']]

# ctags arguments
g_ctags_tool = 'ctags'
g_ctags_function_args = ['--languages=c', '--c-kinds=+f-vdceglmnpstu', '--fields=+k-afiKlmnsSzt', '-f -', '-R']
g_ctags_variable_args = ['--languages=c', '--c-kinds=+v-fdceglmnpstu', '--fields=+k-afiKlmnsSzt', '-f -', '-R']
g_ctags_all_args = ['--languages=c', '--c-kinds=+vf-dceglmnpstu', '-f -', '-R']
g_ctags_variable_file_tmp = '/tmp/tagfile_variable'
g_ctags_function_file_tmp = '/tmp/tagfile_function'

# output file
g_variable_out_file = 'unused_variables'
g_function_out_file = 'unused_functions'
