#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
BLIF2GRAPH: Generates a graph from a BLIF file.
"""
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
    parser.add_argument("--input", type=str, required=True, help="BLIF input file path")
    parser.add_argument("--style", type=str, help="INI style config file path")
    parser.add_argument("--output", type=str, help="Output file path (no extension)")
    parser.add_argument("--format", type=str, default="svg", help="Set output graph format")
    parser.add_argument("--view_graph", action='store_true', default=False, help="View output graph")
    parser.add_argument("--debug", action='store_true', default=False, help="View debug message")

    args = parser.parse_args(raw_args)
    
    print("")

    if args.debug:
        print("[DEBUG-BLIF2GRAPH] Arguments:", args)

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
