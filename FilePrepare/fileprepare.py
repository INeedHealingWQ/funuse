import subprocess
import parameterobj as para
import copy
from abc import ABCMeta, abstractmethod


# Prepare some temporary files for coming processing
class FilePrepareObj:
    def __init__(self, parameter_obj):
        __metaclass__ = ABCMeta
        assert type(parameter_obj) is para.ParameterObj, 'parameter error'
        self.parameter_obj = copy.deepcopy(parameter_obj)

        self.tool = None
        self.tool_args = None
        self.prepare_file_name = None

        self.directory = parameter_obj.directory
        self.executable = parameter_obj.executable
        self.__assert_msg_tool_args = 'Tool args need initialization first'

    # Need override in derived class
    @abstractmethod
    def _prepare(self, file, sub_process):
        pass

    def run(self):
        assert self.tool_args is not None, self.__assert_msg_tool_args
        var_sub_process = subprocess.Popen(
            self.tool_args, stdout=subprocess.PIPE
        )
        self._prepare(self.prepare_file_name, var_sub_process)
