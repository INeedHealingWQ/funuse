#!/usr/bin/python3

import sys
import subprocess
import re


tmpfile = '/tmp/testfile'
outfile = '/tmp/out'
#word = 'hello'


if __name__ == '__main__':
    tmp = open(tmpfile, 'r')
    lines = tmp.readlines()
    out = open(outfile, 'w')
    for i in lines:
        sp = re.split(r' ', i)
        for words in sp:
            b = re.findall(r'^nmh', words)
            if b != []:
                out.write(str(words))
                out.write('\n')

