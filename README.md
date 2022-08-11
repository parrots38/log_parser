## Help
```
usage: python LogParser/parse.py [-d logs_dir] [-r config_for_regex.txt] [-c charset_for_logs] [-a value_for_aggregation] [-p processes_count]
       python LogParser/parse.py -f [-d logs_dir] [-r config_for_regex.txt] [-c charset_for_logs] [-a value_for_aggregation] [-p processes_count]
       python LogParser/parse.py [-n tables_dir] [-a value_for_aggregation]

Parse logs and building graphics. Needs matplotlib and pandas.

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Directory with log files [default = logs].
  -r REGEX, --regex REGEX
                        Path to config file with regular expressions. This
                        file has to contain names and regular expressions with
                        delimiter ';' each one in new line [default =
                        config.txt]. All regular expression must having 2 or
                        more saving groups: 1 - for time, other - for error
                        name or another identifier.
  -c CHARSET, --charset CHARSET
                        Charset which will be use for open log files [default
                        = utf8].
  -n PLOT_NOW, --plot_now PLOT_NOW
                        If True, need to specify path to directory with tables
                        for plotting graphs [default = ].
  -a AGGREGATION, --aggregation AGGREGATION
                        Int value for aggregation matches' count [default = 1]
  -p PROCESSES, --processes PROCESSES
                        Int value for processes' count [default = 4]
  -f, --diff            If this argument is specified all matches will be
                        grouped by 2nd saving group and for all unique matches
                        in 2nd saving group will be found time's difference,
                        that specify services' response time. The 2nd saving
                        group has to contain request's hash or something
                        unique value to identify request.
```
