#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import xtalos
import subprocess

def start(xperf_path, xperf_providers, xperf_stackwalk, xperf_user_providers, etl_filename, debug=False):

    xperf_cmd = [xperf_path,
                 '-on', '+'.join(xperf_providers),
                 '-stackwalk', '+'.join(xperf_stackwalk),
                 '-MaxBuffers', '1024',
                 '-BufferSize', '1024',
                 '-f', '%s.kernel' % etl_filename,
                 '-start', 'talos_ses',
                 '-on', '+'.join(xperf_user_providers),
                 '-MaxBuffers', '1024',
                 '-BufferSize', '1024',
                 '-f', '%s.user' % etl_filename
                 ]
    if debug:
        print "executing '%s'" % subprocess.list2cmdline(xperf_cmd)
    subprocess.call(xperf_cmd)

def start_from_config(config_file=None, debug=False, **kwargs):
    """start from a YAML config file"""

    # required options and associated error messages
    required = {'xperf_path': "xperf_path not given",
                'xperf_providers': "No xperf providers given",
                'xperf_user_providers': "No xperf user providers given",
                'xperf_stackwalk': "No xperf stackwalk options given",
                "etl_filename": "No etl_filename given"}
    for key in required:
        if key not in kwargs:
            kwargs[key] = None

    if config_file:
        # override options from YAML config file
        kwargs = xtalos.options_from_config(kwargs, config_file)

    # ensure the required options are given
    for key, msg in required.items():
        if not kwargs.get(key):
            raise xtalos.xtalosError(msg)

    # ensure path to xperf actually exists
    if not os.path.exists(kwargs['xperf_path']):
        raise xtalos.xtalosError("ERROR: xperf_path '%s' does not exist" % kwargs['xperf_path'])

    # make calling arguments
    args = dict([(key, kwargs[key]) for key in required.keys()])
    args['debug'] = debug

    # call start
    start(**args)

def main(args=sys.argv[1:]):

    # parse command line options
    parser = xtalos.XtalosOptions()
    options, args = parser.parse_args(args)
    options = parser.verifyOptions(options)
    if options is None:
        parser.error("Unable to verify options")

    # start xperf
    try:
        start_from_config(config_file=None,
                          debug=options.debug_level >= xtalos.DEBUG_INFO,
                          **options.__dict__)
    except xtalos.xtalosError, e:
        parser.error(str(e))

if __name__ == "__main__":
    main()
