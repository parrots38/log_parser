import os
import re


CHUNK_SIZE = 8192


def get_compiled_regular_expressions(regular_expressions):
    """Return list of compiled regular expressions (Patterns' objects)."""
    compiled_regexs = []
    for regex in regular_expressions:
        pattern = re.compile(regex)
        if pattern.groups != 2:
            print(f"All regular expression must having 2 or more saving groups: "
                  f"1 - for time, other - for error name. Given:\n{pattern.pattern}")
            exit(1)
        compiled_regexs.append(pattern)
    return compiled_regexs


def get_matches_in_files(regex_pattern, files_list, charset):
    """Return matches by regex in all files for files_list.
    :return: list of tuples.
    """
    for file in files_list:
        with open(file, encoding=charset, errors='ignore') as file_object:
            data = ""
            while True:
                line = file_object.readline()
                data += line
                if len(data) > CHUNK_SIZE or not line:
                    matches_list = regex_pattern.findall(data)
                    if matches_list and len(matches_list) > 0:
                        matches = [(m[0], "...".join(m[1:])) for m in matches_list]
                        yield matches
                    data = ""

                    if not line:
                        break


def save_matches_in_file(matches, file):
    """Save matches in file."""
    with open(file, mode="a") as file_object:
        string_list = [";".join(tup) + "\n" for tup in matches]
        file_object.writelines(string_list)


def save_matches(queue, result_dir, log_files, charset, column_names):
    """Save found by pattern in log_files matches into filename, which opened by this charset."""
    while not queue.empty():
        i, pattern = queue.get()
        print(f"Searching matches for regex = [{pattern.pattern}]...")
        filename = os.path.join(result_dir, f"result{i}.csv")
        matches = None
        need_headers = True
        for matches in get_matches_in_files(pattern, log_files, charset):
            if need_headers:
                save_matches_in_file([("time", column_names[i-1])], filename)
                need_headers = False
            save_matches_in_file(matches, filename)
        if matches:
            print(f"Saved all matches for regex = [{pattern.pattern}].")
        else:
            print(f"No matches for regex = [{pattern.pattern}].")
