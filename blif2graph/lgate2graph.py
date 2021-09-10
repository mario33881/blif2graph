#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
LGATE2GRAPH: generates logic gate graph from a BLIF file.

> Currently NOT implemented. If you'd like to contribute with a Pull Request, please do!
"""
import argparse
import sys
import os

try:
    from ._version import __version__  # noqa: F401
    import blif2graph.utility as utility

except ImportError:
    from _version import __version__  # noqa: F401
    import utility

boold = False
default_styles = {}


def make_lgate_graph(t_filepath, t_styles, t_outname="lgate", t_format="svg", t_view_graph=False):
    """
    Create a logic gate graph.

    :param str t_filepath: BLIF input file path
    :param str t_styles: ini style path
    :param str t_outname: temporary DOT source file path and output file path
    :param str t_format: output format
    :param bool t_view_graph: view the output graph
    :return bool success: True if the graph was created successfully
    """
    success = False
    try:
        # create the graph here
        success = True
    except Exception as e:
        utility.show_error(e)
    
    return success


def main(raw_args=None):
    """
    Parses command line arguments, checks if the input file exists,
    parses the style file (if the user wants to use a custom style)
    and creates the graph.

    :param list raw_args: list of arguments
    :return int exit_code: exit status code
    """
    global boold
    exit_code = 0
    parsed_styles = default_styles

    print("Sorry, currently logic gates are not supported.")
    print("If you'd like to contribute with a Pull Request, please do!")

    return 1 # remove when something is ready to test

    parser = argparse.ArgumentParser(prog="blif2graph --lgate")

    parser.add_argument("--lgate", action="store_true", default=False, help="Create a logic gate graph (not needed if calling lgate2graph)")
    parser.add_argument("--input", type=str, required=True, help="BLIF input file path")
    parser.add_argument("--style", type=str, help="INI style config file path")
    parser.add_argument("--output", type=str, help="Output file path (no extension)")
    parser.add_argument("--format", type=str, default="svg", help="Set output graph format")
    parser.add_argument("--view_graph", action='store_true', default=False, help="View output graph")
    parser.add_argument("--debug", action='store_true', default=False, help="View debug message")

    args = parser.parse_args(raw_args)
    print("")
    
    if args.debug:
        boold = True
    
    if not os.path.isfile(args.input):
        print("Input file doesn't exist or it is not a file")
        exit_code = 1
        return exit_code
    
    if args.style is not None:
        if not os.path.isfile(args.style):
            print("Style file doesn't exist or it is not a file")
            exit_code = 1
            return exit_code
        
        print("Using custom graph style file")
        parsed_styles = utility.parse_styles_file(args.style)
    else:
        print("Using default graph style")
    
    success = False
    if args.output is None:
        success = make_lgate_graph(
            t_filepath=args.input, 
            t_styles=parsed_styles, 
            t_format=args.format,
            t_view_graph=args.view_graph
        )
    else:
        success = make_lgate_graph(
            t_filepath=args.input, 
            t_styles=parsed_styles, 
            t_outname=args.output,
            t_format=args.format,
            t_view_graph=args.view_graph
        )
    
    if not success:
        print("Something went wrong during graph creation")
        exit_code = 2
        return exit_code

    if args.output is None:
        print("Done. Output file path is:  {}.{}".format("lgate", args.format))
    else:
        print("Done. Output file path is:  {}.{}".format(args.output, args.format))

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
