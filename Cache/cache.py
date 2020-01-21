import os
import parameterobj
import Cache.cacheelem as cache


class CacheBase:
    """The base cache class for all cache file type"""
    def __init__(self, a0: cache.CacheElem):
        self._parameter_obj = a0.parameter_obj
        self._exe_path = None
        self._exe_timestamp = a0.exe_timestamp
        self._dir_path = None
        self._dir_timestamp = a0.dir_timestamp
        self._match_tuple = None
        if self._parameter_obj is not None:
            self.__init_para()

    def __init_para(self):
        stat_info_exe = os.stat(self._parameter_obj.executable)
        stat_info_dir = os.stat(self._parameter_obj.directory)
        self._exe_path = os.path.abspath(os.path.expanduser(self._parameter_obj.executable))
        self._dir_path = os.path.abspath(os.path.expanduser(self._parameter_obj.directory))
        self._match_tuple = (self._exe_path, self._exe_timestamp, self._dir_path, self._dir_timestamp)

    @staticmethod
    def parse_para(a0: parameterobj.ParameterObj):
        executable = str(a0.executable)
        directory = str(a0.directory)
        stat_info_exe = os.stat(executable)
        stat_info_dir = os.stat(directory)
        exe_path = executable
        dir_path = directory
        exe_timestamp = str(stat_info_exe.st_mtime)
        dir_timestamp = str(stat_info_dir.st_mtime)
        return exe_path, exe_timestamp, dir_path, dir_timestamp

    @property
    def exe_path(self):
        """Get the cached executable path"""
        return self._exe_path

    @exe_path.setter
    def exe_path(self, v):
        self._exe_path = v

    @property
    def exe_timestamp(self):
        """Get the cached executable timestamp"""
        return self._exe_timestamp

    @exe_timestamp.setter
    def exe_timestamp(self, v):
        self._exe_timestamp = v

    @property
    def dir_path(self):
        """Get the cached ctags directory path"""
        return self._dir_path

    @dir_path.setter
    def dir_path(self, v):
        self._dir_path = v

    @property
    def dir_timestamp(self):
        """Get the cached ctags directory timestamp"""
        return self._dir_timestamp

    @dir_timestamp.setter
    def dir_timestamp(self, v):
        self._dir_timestamp = v

    @property
    def match_tuple(self):
        """Get this cache's match tuple"""
        return self._match_tuple

    def match_by_para(self, a0: parameterobj.ParameterObj):
        """Check if match executable or directory using parameter obj"""
        return self.parse_para(a0) == self._match_tuple

    def match_exe_by_para(self, a0: parameterobj.ParameterObj):
        return self.parse_para(a0)[0:2] == self._match_tuple[0:2]

    def match_by_cache(self, cache_base):
        """Check if match executable or directory using cache obj"""
        return self.match_tuple == cache_base.match_tuple

    def match_dir_by_cache(self, cache_base):
        return self.match_tuple[2: 4] == cache_base.match_tuple[2:4]


class DataUnusedCache(CacheBase):
    def __init__(self, a0: cache.DataUnusedCacheElem):
        super().__init__(a0)
        self.unused_path = a0.path


class TextUnusedCache(CacheBase):
    def __init__(self, a0: cache.TextUnusedCacheElem):
        super().__init__(a0)
        self.unused_path = a0.path


class TagDictCache(CacheBase):
    def __init__(self, a0: cache.TagDictCacheElem):
        super().__init__(a0)
        self.dict_path = a0.path


# class VarTagDictCache(TagDictCache):
#     def __init__(self, a0: cache.VarTagDictCacheElem):
#         super().__init__(a0)
#
#
# class FunTagDictCache(TagDictCache):
#     def __init__(self, a0: cache.FunTagDictCacheElem):
#         super().__init__(a0)


class FilterCache(CacheBase):
    def __init__(self, a0: cache.FilterCacheElem):
        super().__init__(a0)
        self.filter_path = a0.path
        self.data_unused_cache = DataUnusedCache(a0.data_unused_cache_elem)
        self.text_unused_cache = TextUnusedCache(a0.text_unused_cache_elem)
        self.tag_dict_cache = TagDictCache(a0.tag_dict_cache_elem)
        self.filter_index_type = None


class VarFilterCache(FilterCache):
    filter_index_type = 'var_filter'

    def __init__(self, a0: cache.VarFilterCacheElem):
        super().__init__(a0)


class FunFilterCache(FilterCache):
    filter_index_type = 'fun_filter'

    def __init__(self, a0: cache.FunFilterCacheElem):
        super().__init__(a0)
