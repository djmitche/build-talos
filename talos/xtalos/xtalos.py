# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import optparse
import sys
import yaml

DEBUG_CRITICAL =0
DEBUG_ERROR =   1
DEBUG_WARNING = 2
DEBUG_INFO =    3
DEBUG_VERBOSE = 4

class xtalosError(Exception):
    """error related to xtalos invocation"""

def options_from_config(options, config_file):
    """override options from a YAML config file; returns the dictionary
    - options: a dictionary with default options
    - config_file: path to a YAML config file
    """

    config = open(config_file, 'r')
    yaml_config = yaml.load(config)
    config.close()
    for obj in options.keys():
        options[obj] = yaml_config.get(obj, options[obj])
    return options

class XtalosOptions(optparse.OptionParser):

    def __init__(self, **kwargs):
        optparse.OptionParser.__init__(self, **kwargs)
        defaults = {}

        self.add_option("--pid", dest="processID",
                        help="process ID of the process we launch")
        defaults["processID"] = None

        self.add_option("-x", "--xperf", dest="xperf_path",
                        help="location of xperf tool, defaults to 'xperf.exe'")
        defaults["xperf_path"] = "xperf.exe"

        self.add_option("-e", "--etl_filename", dest="etl_filename",
                        help = "Name of the .etl file to work with. Defaults to 'output.etl'")
        defaults["etl_filename"] = "output.etl"

        self.add_option("-d", "--debug",
                        type="int", dest="debug_level",
                        help="debug level for output from tool (0-5, 5 being everything), defaults to 1")
        defaults["debug_level"] = 1

        self.add_option("-o", "--output-file", dest="outputFile",
                        help="Filename to write all output to, default is stdout")
        defaults["outputFile"] = None

        self.add_option("-r", "--providers", dest="xperf_providers",
                        action="append",
                        help="xperf providers to collect data from")
        defaults["xperf_providers"] = []

        self.add_option("--user-providers", dest="xperf_user_providers",
                        action="append",
                        help="user mode xperf providers to collect data from")
        defaults["xperf_user_providers"] = []

        self.add_option("-s", "--stackwalk", dest="xperf_stackwalk",
                        action="append",
                        help="xperf stackwalk options to collect")
        defaults["xperf_stackwalk"] = []

        self.add_option("-c", "--config-file", dest="configFile",
                        help="Name of the yaml config file with test run and browser information")
        defaults["configFile"] = None

        self.add_option("-w", "--whitelist-file", dest="whitelist_file",
                        help="Name of whitelist file")
        defaults["whitelist_file"] = None

        self.add_option("-i", "--all-stages", dest="all_stages", action="store_true",
                        help="Include all stages in file I/O output, not just startup")
        defaults["all_stages"] = False

        self.add_option("-t", "--all-threads", dest="all_threads", action="store_true",
                        help="Include all threads in file I/O output, not just main")
        defaults["all_threads"] = False

        self.add_option("-a", "--approot", dest="approot",
                        help="Provide the root directory of the application we are testing to find related files (i.e. dependentlibs.list)")
        defaults["approot"] = None

        self.add_option("-a", "--error-filename", dest="error_filename",
                        help="Filename to store the failures detected while runnning the test")
        defaults["error_filename"] = None

        self.set_defaults(**defaults)

        self.set_usage('')

    def verifyOptions(self, options):

        # override options from config file
        if options.configFile:
            options_from_config(options.__dict__, options.configFile)

        # ensure xperf path exists
        options.xperf_path = os.path.abspath(options.xperf_path)
        if not os.path.exists(options.xperf_path):
            print "ERROR: xperf_path '%s' does not exist" % options.xperf_path
            return None

        return options
