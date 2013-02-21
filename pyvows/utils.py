# -*- coding: utf-8 -*-
'''This module is the foundation that allows users to write PyVows-style tests.
'''

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import fnmatch
import glob
import os
import time

from pyvows.errors  import _AssertionNotFoundError, VowsAssertionError


elapsed = lambda start_time: float(round(time.time() - start_time, 6))

def locate(pattern, root=os.curdir, recursive=True):
    '''Recursively locates test files when `pyvows` is run from the
    command line.

    '''
    root_path = os.path.abspath(root)

    if recursive:
        return_files = []
        for path, dirs, files in os.walk(root_path):
            for filename in fnmatch.filter(files, pattern):
                return_files.append(os.path.join(path, filename))
        return return_files
    else:
        return glob(os.path.join(root_path, pattern))

def template():
    '''Provides a template containing boilerplate code for new PyVows test
    files. Output is sent to STDOUT, allowing you to redirect it on
    the command line as you wish.

    '''
    from datetime import date
    import sys
    from textwrap import dedent

    from pyvows import version

    TEST_FILE_TEMPLATE = '''\
    # -*- coding: utf-8 -*-
    ##  Generated by PyVows v{version}  ({date})
    ##  http://pyvows.org

    ##  IMPORTS  ##
    ##
    ##  Standard Library
    #
    ##  Third Party
    #
    ##  PyVows Testing
    from pyvows import Vows, expect

    ##  Local Imports
    import


    ##  TESTS  ##
    @Vows.batch
    class PleaseGiveMeAGoodName(Vows.Context):

        def topic(self):
            return # return what you're going to test here

        ##  Now, write some vows for your topic! :)
        def should_do_something(self, topic):
            expect(topic)# <pyvows assertion here>

    '''.format(
        version = version.to_str(),
        date = '{0:%Y/%m/%d}'.format(date.today())
    )

    sys.stdout.write(dedent(TEST_FILE_TEMPLATE))


class VowsAssertion(object):
    '''Used by the `Vows` class for various assertion-related functionality.'''

    AssertionNotFoundError = _AssertionNotFoundError
    '''Raised when a `VowsAssertion` cannot be found.'''

    def __getattr__(self, name):
        if not hasattr(self, name):
            raise VowsAssertion.AssertionNotFoundError(name)
        return super(VowsAssertion, self).__getattr__(name)
