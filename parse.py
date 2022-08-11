import os
import time
import multiprocessing

import Utils
import Parser
import Plotter


def main(args):
    result_dir = Utils.create_result_dir(args.dir)
    dir_with_results = args.plot_now
    if not args.plot_now:
        dir_with_results = result_dir
        log_files = Utils.get_files_in_dir(args.dir)
        print(f"Files with logs: {log_files}")

        regex_names, regexs = Utils.get_regular_expressions(args.regex)
        compiled_regexs = Parser.get_compiled_regular_expressions(regexs)

        queue = multiprocessing.SimpleQueue()
        for i, regex in zip(range(len(compiled_regexs)), compiled_regexs):
            queue.put((i+1, regex))
        processes_count = args.processes if args.processes <= len(compiled_regexs) else len(compiled_regexs)
        processes = []
        for i in range(processes_count):
            process = multiprocessing.Process(
                target=Parser.save_matches,
                args=(queue, result_dir, log_files, args.charset, regex_names),
                daemon=True
            )
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

    print(f"Creating graph for found values...")
    graphic_filename = os.path.join(result_dir, f"result.png")
    plotter = Plotter.Plotter(graphic_filename, args.aggregation, args.diff)

    filenames = Utils.get_files_in_dir(dir_with_results)
    i = 1
    index_valuename_filename = []
    for filename in filenames:
        if filename.endswith("csv"):
            with open(filename, encoding=args.charset, errors='ignore') as file:
                value_name = file.readline().split(";")[1]
                index_valuename_filename.append((i, value_name, filename))
            i += 1
    print(f"Files with tables for graph: {filenames}")

    for i, _, filename in index_valuename_filename:
        plotter.plot_graph(filename)
    plotter.set_legend([f"{i}-{description}" for i, description, _ in index_valuename_filename])
    plotter.save_figure()


if __name__ == "__main__":
    stopwatch = time.time()
    args = Utils.get_args()
    main(args)
    print(f"The program ended in {(time.time() - stopwatch):.3f} sec.")
