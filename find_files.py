#!/usr/bin/python3
# -*- encoding: utf-8 -*-

"""
CREATED    :
AUTHOR     :
DESCRIPTION:
"""

import os
import fnmatch

def find_filelist(path=None, pattern='*', walk=False):
    '''Find files matching the pattern in the given folder

    :param path: the path to start searching in (DEFAULT=None)
    :param pattern: the pattern to match on (DEFAULT='*')
    :param walk: look in sub-folders of the src_loc(DEFAULT=False)
    :return: {list} of filenames and path
    '''

    tresult = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, f'{pattern}'):
                if walk is False:
                    if root == path:
                        tresult.append(os.path.join(root, name))
                    else:
                        pass
                elif walk is True:
                    tresult.append(os.path.join(root, name))
                else:
                    pass

    return tresult

