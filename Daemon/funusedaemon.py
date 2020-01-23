from time import sleep
from Daemon.daemon import Daemon
import gvars
import fcntl
from os import path
from os import remove


class FunuseDaemon(Daemon):
    def __init__(self, *args, **kwargs):
        super(FunuseDaemon, self).__init__(*args, **kwargs)
        self.index_monitor_sleep_time = 5

    def __check_index_lines(self, lines: list):
        cache_type_dict = {}
        updated_lines = []
        for single_line in lines:
            single_line_split_list = single_line.split()
            if len(single_line_split_list) != 9:
                continue
            cache_type = single_line_split_list[0]
            if cache_type_dict.get(cache_type) is None:
                cache_type_dict[cache_type] = [single_line_split_list]
            else:
                cache_type_dict[cache_type].append(single_line_split_list)
        for e in cache_type_dict:
            max_cache = cache_type_dict[e][0]
            max_stamp = float(max_cache[2])
            for i in cache_type_dict[e][1:]:
                stamp = float(i[2])
                if stamp > max_stamp:
                    need_del_name = max_cache[-1]
                    max_cache = i
                    max_stamp = stamp
                else:
                    need_del_name = i[-1]
                try:
                    remove(need_del_name)
                except OSError:
                    pass
            newest = ' '.join(max_cache) + '\n'
            updated_lines.append(newest)
        if updated_lines.__len__() < lines.__len__():
            return updated_lines
        else:
            return True

    def __index_monitor(self):
        """monitor cache index file"""
        cache_index_file = path.abspath(path.expanduser(gvars.g_cache_index_file))
        with open(cache_index_file, 'r+') as f:
            while True:
                try:
                    fcntl.flock(f, fcntl.LOCK_SH | fcntl.LOCK_NB)
                    f.seek(0, 0)
                    lines = f.readlines()
                    fcntl.flock(f, fcntl.LOCK_UN)
                except OSError:
                    pass
                if lines:
                    updated_lines = self.__check_index_lines(lines)
                    if updated_lines is not True:
                        fcntl.flock(f, fcntl.LOCK_EX)
                        f.truncate(0)
                        f.seek(0, 0)
                        f.writelines(updated_lines)
                        f.flush()
                        fcntl.flock(f, fcntl.LOCK_UN)
                        self.log('Aged several old cache lines\n')
                sleep(self.index_monitor_sleep_time)

    def run(self):
        self.__index_monitor()
