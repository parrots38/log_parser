import argparse
import time
from os import walk, listdir, mkdir, cpu_count
from os.path import abspath, isfile, join, dirname, isdir
from shutil import rmtree


RESULT_DIR = "result"


def get_args():
    """Return parsed command line args."""
    parser = argparse.ArgumentParser(
        description="Parse logs and building graphics. Needs matplotlib and pandas.",
        usage="python LogParser/parse.py [-d logs_dir] [-r config_for_regex.txt] [-c charset_for_logs] [-a value_for_aggregation] [-p processes_count]\n"
              "       python LogParser/parse.py -f [-d logs_dir] [-r config_for_regex.txt] [-c charset_for_logs] [-a value_for_aggregation] [-p processes_count]\n"
              "       python LogParser/parse.py [-n tables_dir] [-a value_for_aggregation]"
    )
    parser.add_argument('-d', '--dir', action="store", type=str, default="logs",
                        help="Directory with log files [default = %(default)s].")
    parser.add_argument('-r', '--regex', action="store", type=str, default="config.txt",
                        help="Path to config file with regular expressions.\n"
                             "This file has to contain names and regular expressions with delimiter ';' "
                             "each one in new line [default = %(default)s]. "
                             "All regular expression must having 2 or more saving groups: "
                             "1 - for time, other - for error name or another identifier."
                        )
    parser.add_argument('-c', '--charset', action="store", type=str, default="utf8",
                        help="Charset which will be use for open log files [default = %(default)s].")
    parser.add_argument('-n', '--plot_now', action="store", type=str, default="",
                        help="If True, need to specify path to directory with tables for plotting graphs "
                             "[default = %(default)s].")
    parser.add_argument('-a', '--aggregation', action="store", type=int, default=1,
                        help="Int value for aggregation matches' count [default = %(default)i]")
    parser.add_argument('-p', '--processes', action="store", type=int, default=cpu_count(),
                        help="Int value for processes' count [default = %(default)i]")
    parser.add_argument('-f', '--diff', action="store_true",
                        help="If this argument is specified all matches will be grouped by 2nd saving group "
                             "and for all unique matches in 2nd saving group will be found time's difference, "
                             "that specify services' response time. The 2nd saving group has to contain "
                             "request's hash or something unique value to identify request.")
    return parser.parse_args()


def get_files_in_dir(path):
    """Return only files in dir."""
    absolute_path = abspath(path)
    result = []
    for root, sub, files in walk(absolute_path):
        for file in files:
            absolute_filename = join(root, file)
            result.append(absolute_filename)
    return sorted(result)


def create_result_dir(dir_for_log_files):
    """Create dir for result files and return path."""
    current_path = abspath(dir_for_log_files)
    working_directory = dirname(current_path)
    result_dir_abspath = join(working_directory, RESULT_DIR + time.strftime("_%y-%m-%dT%H-%M-%S"))

    mkdir(result_dir_abspath)
    return result_dir_abspath


def get_regular_expressions(path_to_config_file):
    """Return regular expressions from config file."""
    with open(path_to_config_file) as file:
        lines = [l.rstrip() for l in file.readlines()]
        names = []
        regexs = []
        for line in lines:
            name, regex = line.split(";", 1)
            names.append(name)
            regexs.append(regex)
        return names, regexs
