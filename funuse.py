#!/usr/bin/python3

import sys
import Filter.functionfilterobj as ff
import Filter.variablefilterobj as vf
import funusecmd
import gvars
from pathlib import Path
from os import path, fork
from Daemon.funusedaemon import FunuseDaemon as Dm


def init_check_cache():
    cache_dir = Path(path.abspath(path.expanduser(gvars.g_cache_dir)))
    cache_index_file = Path(path.abspath(path.expanduser(gvars.g_cache_index_file)))
    if cache_dir.exists() is False:
        """Create cache directory if not exists"""
        try:
            cache_dir.mkdir(parents=True)
            if cache_index_file.exists() is False:
                """Create cache index file if not exists"""
                cache_index_file.touch()
        except PermissionError:
            'Create cache directory failed, may be you should use super-user privilege'


def init_check_daemon():
    full_daemon_path = path.abspath(path.expanduser(gvars.g_daemon_dir))
    p = Path(full_daemon_path)
    p.mkdir(parents=True, exist_ok=True)
    full_daemon_pid_file = path.abspath(path.expanduser(gvars.g_daemon_pid_file))
    full_daemon_log_file = path.abspath(path.expanduser(gvars.g_daemon_log_file))
    full_daemon_state_file = path.abspath(path.expanduser(gvars.g_daemon_state_file))
    pid = fork()
    '''For a process to try to be a daemon'''
    if pid == 0:
        '''In child'''
        daemon = Dm(pidfile=full_daemon_pid_file, logfile=full_daemon_log_file,
                    statefile=full_daemon_state_file, verbose=0)
        daemon.start()
        exit(0)


def funuse_init():
    init_check_cache()
    init_check_daemon()


if __name__ == '__main__':
    funuse_init()
    cmd_parse_obj = funusecmd.CmdParseObj(argv=sys.argv)
    parameter_obj = cmd_parse_obj.start_parse()
    cache_index = path.abspath(path.expanduser(gvars.g_cache_index_file))
    if parameter_obj.count_variable is True:
        filter_obj = vf.VariableFilterObj(parameter_obj)
        print('Start filtering unused variables ...')
        filter_obj.run()
        print('Filtering unused variables done')
    if parameter_obj.count_function is True:
        print('Start filtering unused functions ...')
        filter_obj = ff.FunctionFilterObj(parameter_obj)
        filter_obj.run()
        print('Filtering unused functions done')
