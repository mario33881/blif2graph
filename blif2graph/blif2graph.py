#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
BLIF2GRAPH: Generates a graph from a BLIF file.
"""
import os
import sys
import argparse

try:
    from ._version import __version__  # noqa: F401
    import blif2graph.fsm2graph as fsm2graph
    import blif2graph.lgate2graph as lgate2graph

except ImportError:
    from _version import __version__  # noqa: F401
    import fsm2graph
    import lgate2graph


def read_line_by_line(t_file):
    """
    Reads a file and yields one line per iteration.

    :param str t_file: input file path
    """
    with open(t_file, "r") as f:
        line = f.readline()
        while line != "":
            yield line
            line = f.readline()


def manage_legal(t_legal_arg):
    """
    Manages licenses: if t_legal_arg is an empty string,
    this function shows this repository's license.
    If t_legal_arg is not an empty string then that string is used
    to look for the file of a third party dependency.
    If that file exists that file's content gets shown.

    :param str t_legal_arg: if not empty, shows the dependency's license specified by this argument
    """
    legal_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'legal'))

    if t_legal_arg == "":
        print("\nThe following is the blif2graph license:\n")
        for line in read_line_by_line(os.path.join(legal_folder, "LICENSE.txt")):
            print(" " + line, end="")

        print("\n\nType --legal <library> where <library> is one of the following license files to view the dependency license:")
        
        for index, license in enumerate(os.listdir(os.path.join(legal_folder, "third-party"))):
            if index % 3 == 0:
                print("")  # go to newline every 3 libraries to improve readability
            
            print(" ", license, " |", sep="", end="")
    else:
        license_path = os.path.join(legal_folder, "third-party", t_legal_arg)
        if not os.path.isfile(license_path):
            print("License file '{}' not found: please type the full file name --legal <package>-<version>_license.txt".format(args.legal))
            return 1
        
        for line in read_line_by_line(license_path):
            print(" " + line, end="")
        print("")
    
    return 0


def main(raw_args=None):
    """
    Parses command line arguments, checks if the input file exists,
    parses the style file (if the user wants to use a custom style)
    and creates the graph.

    :param list raw_args: list of arguments
    :return int exit_code: exit status code
    """
    exit_code = 0

    parser = argparse.ArgumentParser(prog="blif2graph")
    parser.add_argument("--fsm", action="store_true", default=False, help="Create an FSM graph")
    parser.add_argument("--lgate", action="store_true", default=False, help="Create a logic gate graph")
    parser.add_argument("--input", type=str, default=None, help="BLIF input file path")
    parser.add_argument("--style", type=str, help="INI style config file path")
    parser.add_argument("--output", type=str, help="Output file path (no extension)")
    parser.add_argument("--format", type=str, default="svg", help="Set output graph format")
    parser.add_argument("--view_graph", action='store_true', default=False, help="View output graph")
    parser.add_argument("--debug", action='store_true', default=False, help="View debug message")
    parser.add_argument("--graphviz_dlls", type=str, help="Path to Graphviz's DLLs. Useful when the 'DLL load failed' error is thrown")

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        parser.add_argument(
            "--legal", 
            nargs='?',     # allow the user to type --legal without arguments
            default=None,  # if the user doesn't type --legal, args.legal is None
            const="",      # if the user types --legal without arguments, args.legal == ""
            type=str, 
            help="View blif2graph license and licenses of its dependencies"
        )

    args = parser.parse_args(raw_args)
    
    print("")

    if args.debug:
        print("[DEBUG-BLIF2GRAPH] Arguments:", args)

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS') and args.legal is not None:
        return manage_legal(args.legal)

    if args.input is None:
        parser.print_help(sys.stderr)
        print("\nblif2graph: error: the following arguments are required: --fsm --input <input_file> OR --lgate --input <input_file>")
        return 1

    if args.fsm == args.lgate:
        parser.print_help()
        print("\nPlease, specify '--fsm' OR '--lgate' as an argument")
        exit_code = 1
        return exit_code
    
    if args.fsm:
        if args.debug:
            print("[DEBUG-BLIF2GRAPH] User wants to create an fsm graph")

        fsm2graph.main(raw_args)
    else:
        if args.debug:
            print("[DEBUG-BLIF2GRAPH] User wants to create a logic gate graph")

        lgate2graph.main(raw_args)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
