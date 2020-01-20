from parameterobj import ParameterObj
from os import path as pt


class CacheElem:
    def __init__(self, *, elem_type, executable, exe_timestamp, directory, dir_timestamp, path):
        self._type = elem_type
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
    def type(self):
        return self._type

    @property
    def executable(self):
        return self._executable

    @property
    def directory(self):
        return self._directory

    @property
    def path(self):
        return self._path

    @property
    def parameter_obj(self):
        return self._parameter_obj


class DataUnusedCacheElem(CacheElem):
    def __init__(self, *, elem_type, executable, exe_timestamp, directory, dir_timestamp, path_data_unused):
        super(DataUnusedCacheElem, self).__init__(elem_type=elem_type, executable=executable,
                                                  exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                                  directory=directory, path=path_data_unused)


class TextUnusedCacheElem(CacheElem):
    def __init__(self, *, elem_type, executable, exe_timestamp, directory, dir_timestamp, path_text_unused):
        super(TextUnusedCacheElem, self).__init__(elem_type=elem_type, executable=executable,
                                                  exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                                  directory=directory, path=path_text_unused)


class TagDictCacheElem(CacheElem):
    def __init__(self, *, elem_type, executable, exe_timestamp, directory, dir_timestamp, path_tag_dict):
        super(TagDictCacheElem, self).__init__(elem_type=elem_type, executable=executable,
                                               exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                               directory=directory, path=path_tag_dict)


# class VarTagDictCacheElem(TagDictCacheElem):
#     def __init__(self, *, elem_type, executable, exe_timestamp, directory, dir_timestamp, path_var_tag_dict):
#         super(VarTagDictCacheElem, self).__init__(elem_type=elem_type, executable=executable,
#                                                   exe_timestamp = exe_timestamp, dir_timestamp = dir_timestamp,
#                                                   directory=directory, path_tag_dict=path_var_tag_dict)
#
#
# class FunTagDictCacheElem(TagDictCacheElem):
#     def __init__(self, *, elem_type, executable, exe_timestamp, directory, dir_timestamp, path_fun_tag_dict):
#         super(FunTagDictCacheElem, self).__init__(elem_type=elem_type, executable=executable,
#                                                   exe_timestamp = exe_timestamp, dir_timestamp = dir_timestamp,
#                                                   directory=directory, path_tag_dict=path_fun_tag_dict)


class FilterCacheElem(CacheElem):
    def __init__(self, *, elem_type, executable, exe_timestamp, directory, dir_timestamp, path_data_unused,
                 path_text_unused, path_tag_dict, path_filter):
        super(FilterCacheElem, self).__init__(elem_type=elem_type, executable=executable,
                                              exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                              directory=directory, path=path_filter)
        self.data_unused_cache_elem = DataUnusedCacheElem(elem_type=elem_type, executable=executable,
                                                          exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                                          directory=directory, path_data_unused=path_data_unused)
        self.text_unused_cache_elem = TextUnusedCacheElem(elem_type=elem_type, executable=executable,
                                                          exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                                          directory=directory, path_text_unused=path_text_unused)
        self.tag_dict_cache_elem = TagDictCacheElem(elem_type=elem_type, executable=executable,
                                                    exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                                    directory=directory, path_tag_dict=path_tag_dict)


class VarFilterCacheElem(FilterCacheElem):
    def __init__(self, *, elem_type, executable, exe_timestamp, directory, dir_timestamp, path_data_unused,
                 path_text_unused, path_var_tag_dict, path_var_filter):
        super(VarFilterCacheElem, self).__init__(elem_type=elem_type, executable=executable, directory=directory,
                                                 exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                                 path_data_unused=path_data_unused, path_text_unused=path_text_unused,
                                                 path_tag_dict=path_var_tag_dict, path_filter=path_var_filter)


class FunFilterCacheElem(FilterCacheElem):
    def __init__(self, *, elem_type, executable, exe_timestamp, directory, dir_timestamp, path_data_unused,
                 path_text_unused, path_fun_tag_dict, path_var_filter):
        super(FunFilterCacheElem, self).__init__(elem_type=elem_type, executable=executable, directory=directory,
                                                 exe_timestamp=exe_timestamp, dir_timestamp=dir_timestamp,
                                                 path_data_unused=path_data_unused, path_text_unused=path_text_unused,
                                                 path_tag_dict=path_fun_tag_dict, path_filter=path_var_filter)
