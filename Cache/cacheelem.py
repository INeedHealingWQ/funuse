from parameterobj import ParameterObj
from os import path as pt
from Cache import cache


class CacheElem:
    def __init__(self, *, executable, exe_timestamp, directory, dir_timestamp, path):
        self._parameter_obj = None
        self._executable = pt.abspath(pt.expanduser(executable))
        self._exe_timestamp = exe_timestamp
        self._directory = pt.abspath(pt.expanduser(directory))
        self._dir_timestamp = dir_timestamp
        self._path = path
        self.init_para_obj()

    def init_para_obj(self):
        self._parameter_obj = ParameterObj(executable=self._executable, directory=self.directory)

    @property
    def parameter_obj(self):
        return self._parameter_obj

    @property
    def executable(self):
        return self._executable

    @property
    def exe_timestamp(self):
        return self._exe_timestamp

    @property
    def dir_timestamp(self):
        return self._dir_timestamp

    @property
    def directory(self):
        return self._directory

    @property
    def path(self):
        return self._path


class DataUnusedCacheElem(CacheElem):
    def __init__(self, *, executable, exe_timestamp, directory, dir_timestamp, path_data_unused):
        super(DataUnusedCacheElem, self).__init__(executable=executable,
                                                  exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                                  directory=directory, path=path_data_unused)


class TextUnusedCacheElem(CacheElem):
    def __init__(self, *, executable, exe_timestamp, directory, dir_timestamp, path_text_unused):
        super(TextUnusedCacheElem, self).__init__(executable=executable,
                                                  exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                                  directory=directory, path=path_text_unused)


class TagDictCacheElem(CacheElem):
    def __init__(self, *, executable, exe_timestamp, directory, dir_timestamp, path_tag_dict):
        super(TagDictCacheElem, self).__init__(executable=executable,
                                               exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                               directory=directory, path=path_tag_dict)


# class VarTagDictCacheElem(TagDictCacheElem):
#     def __init__(self, *, executable, exe_timestamp, directory, dir_timestamp, path_var_tag_dict):
#         super(VarTagDictCacheElem, self).__init__(executable=executable,
#                                                   exe_timestamp = exe_timestamp, dir_timestamp = dir_timestamp,
#                                                   directory=directory, path_tag_dict=path_var_tag_dict)
#
#
# class FunTagDictCacheElem(TagDictCacheElem):
#     def __init__(self, *, executable, exe_timestamp, directory, dir_timestamp, path_fun_tag_dict):
#         super(FunTagDictCacheElem, self).__init__(executable=executable,
#                                                   exe_timestamp = exe_timestamp, dir_timestamp = dir_timestamp,
#                                                   directory=directory, path_tag_dict=path_fun_tag_dict)


class FilterCacheElem(CacheElem):
    def __init__(self, *, executable, exe_timestamp, directory, dir_timestamp, path_data_unused,
                 path_text_unused, path_tag_dict, path_filter):
        super(FilterCacheElem, self).__init__(executable=executable,
                                              exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                              directory=directory, path=path_filter)
        self.data_unused_cache_elem = DataUnusedCacheElem(executable=executable,
                                                          exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                                          directory=directory, path_data_unused=path_data_unused)
        self.text_unused_cache_elem = TextUnusedCacheElem(executable=executable,
                                                          exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                                          directory=directory, path_text_unused=path_text_unused)
        self.tag_dict_cache_elem = TagDictCacheElem(executable=executable,
                                                    exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                                    directory=directory, path_tag_dict=path_tag_dict)


class VarFilterCacheElem(FilterCacheElem):
    def __init__(self, *, executable, exe_timestamp, directory, dir_timestamp, path_data_unused,
                 path_text_unused, path_var_tag_dict, path_var_filter):
        super(VarFilterCacheElem, self).__init__(executable=executable, directory=directory,
                                                 exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                                 path_data_unused=path_data_unused, path_text_unused=path_text_unused,
                                                 path_tag_dict=path_var_tag_dict, path_filter=path_var_filter)

    @staticmethod
    def construct_index_line(a0: ParameterObj,
                             path_data_unused, path_text_unused, path_var_tag_dict, path_var_filter):
        return ' '.join([cache.VarFilterCache.filter_index_type, *cache.CacheBase.parse_para(a0),
                         path_data_unused, path_text_unused, path_var_tag_dict, path_var_filter]) + '\n'


class FunFilterCacheElem(FilterCacheElem):
    def __init__(self, *, executable, exe_timestamp, directory, dir_timestamp, path_data_unused,
                 path_text_unused, path_fun_tag_dict, path_var_filter):
        super(FunFilterCacheElem, self).__init__(executable=executable, directory=directory,
                                                 exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                                 path_data_unused=path_data_unused, path_text_unused=path_text_unused,
                                                 path_tag_dict=path_fun_tag_dict, path_filter=path_var_filter)

    @staticmethod
    def construct_index_line(a0: ParameterObj,
                             path_data_unused, path_text_unused, path_fun_tag_dict, path_fun_filter):
        return ' '.join([cache.FunFilterCache.filter_index_type, *cache.CacheBase.parse_para(a0),
                         path_data_unused, path_text_unused, path_fun_tag_dict, path_fun_filter]) + '\n'
