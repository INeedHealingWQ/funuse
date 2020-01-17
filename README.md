# Prepare
    python version need >= 3.5
    Exuberant Ctags >= 5.9
    sudo apt-get install -y python3.x ctags

**You should pull down gcc optimization level to 0 before use funuse**

# Simply use:
    funuse.py -x ./ISS.exe -d ../future

    This will dump both module name and file path in the module.
    Then the file 'unused_functions' or 'unused_variables' would arised in your work directory.
    Note that '../future' is the project path which you want to count.
    Ex:
        funuse.py -x ./ISS.exe -d ../future/vlangarp -m
    Will only dump the unused variables and functions in vlangarp module

    **NOTE**: Do not use funuse multi-times at the same time because of the shared file.

# Only dump unused functions:
    funuse.py -x ./ISS.exe -f -d ../future

# Only dump unused variables:
    funuse.py -x ./ISS.exe -v -d ../future

# Only dump module name:
    funuse.py -x ./ISS.exe -s -d ../future

This tool use '/opt/toolchain/iProcLDK_3.4.6/usr/bin/arm-linux-objdump'
by default, you can use -t to re-assign it:
    funuse.py -x ./ISS.exe -s -d ../future -t arm-linux-objdump

# Show help:
    funuse.py -h


# NOTE:
    Part of the options may not support currently.
