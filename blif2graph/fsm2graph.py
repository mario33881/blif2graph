#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
FSM2GRAPH: generates an FSM graph from a BLIF file.

This script was inspired by generate-stg, a tool created by Mattia Corradi and Dalla Chiara Michele: 
https://github.com/bohzio/sis-tools/blob/master/generate-stg
"""
import argparse
import os
import sys

import graphviz
import blifparser.blifparser as blifparser

try:
    from ._version import __version__  # noqa: F401
    import blif2graph.utility as utility

except ImportError:
    from _version import __version__  # noqa: F401
    import utility

boold = False
default_styles = {
    'graph': {
        'fontsize': '16',
        'fontcolor': 'black',
        'fontname': 'Times-Roman',
        'rankdir': 'TB',           # TB: top to bottom (inverse: BT), LR: left to right (inverse: RL)
        'splines': 'true',
        'overlap': 'false',
        'size': '8,5',
        'bgcolor': 'transparent',  
        'center': 'true',
        'charset': 'UTF-8',
        'colorscheme': '',
        'concentrate': 'false',   # true: concentrate arrows together in one line until a certain point
        'dpi': '96.0'
    },
    'edges': {
        'fontsize': '16',
        'arrowsize': '.5',
        'arrowhead': 'normal',
        'arrowtail': 'normal',
        'color': 'gray34',
        'fillcolor': 'gray34',
        'fontcolor': 'gray34',
        'fontname': 'Times-Roman',
        'colorscheme': '',
        'constraint': 'true',
        'decorate': 'false',
        'dir': 'forward'
    },
    'nodes': {
        'fontsize': '16',
        'color': 'black',
        'fillcolor': 'black',
        'fontcolor': 'black',
        'fontname': 'Times-Roman',
        'colorscheme': '',
        'penwidth': '2.0'
    }
}


def apply_styles(t_graph, t_styles):
    """
    Applies the <t_styles> styles to the graph, 
    nodes and edges of the <t_graph> graph.

    Example:
    >>> g = graphviz.Digraph('fsm')
    >>> # add nodes to g
    >>> styles = {"graph": {"fontsize": "18"}, "nodes": {"fonsize": "12"}}
    >>> g = apply_styles(g, styles)

    :param t_graph: graphviz graph
    :param dict t_styles: dictionary with custom styles
    :return t_graph: graphviz graph with custom styles
    """
    if 'graph' in t_styles and t_styles['graph']:
        t_graph.graph_attr.update(t_styles['graph'])

    if 'nodes' in t_styles and t_styles['nodes']:
        t_graph.node_attr.update(t_styles['nodes'])

    if 'edges' in t_styles and t_styles['edges']:
        t_graph.edge_attr.update(t_styles['edges'])

    return t_graph


def get_reset_state_name(t_fsm):
    """
    Returns the name of the reset state.

    If an .r keyword is specified, that is the name of the reset state.
    If the .r keyword is not present, the first state defined 
    in the transition table is the reset state.

    :param t_fsm: blifparser.BlifParser().blif.fsm object
    :return str reset_state: name of the reset state
    """
    reset_state = None
    if t_fsm.r is None:
        if len(t_fsm.transtable) > 0:
            reset_state = t_fsm.transtable[0][1]
    else:
        reset_state = t_fsm.r.name
    
    return reset_state


def make_fsm_graph(t_filepath, t_styles, t_outname="fsm", t_format="svg", t_view_graph=False):
    """
    Create an FSM graph.

    :param str t_filepath: BLIF input file path
    :param str t_styles: ini style path
    :param str t_outname: temporary DOT source file path and output file path
    :param str t_format: output format
    :param bool t_view_graph: view the output graph
    :return bool success: True if the graph was created successfully
    """
    success = False

    try:
        blif_data = blifparser.BlifParser(t_filepath)
        blif = blif_data.blif

        if len(blif.problems) > 0:
            print("PROBLEMS:")
            for problem in blif.problems:
                print(problem)

            print("-----------")    
            raise Exception("BLIF file is not valid. Please, fix the problems above")
        
        g = graphviz.Digraph('fsm')

        reset_state = get_reset_state_name(blif.fsm)

        if reset_state is not None:
            if boold:
                print("[DEBUG-FSM2GRAPH] reset state name:", reset_state)
            g.attr('node', shape='doublecircle')
            g.node(reset_state)

            g.attr('node', shape='circle')
            for row in blif.fsm.transtable:
                if boold:
                    print("[DEBUG-FSM2GRAPH] ", row)
                g.edge(row[1], row[2], label=" "+row[0]+"/"+row[3])

            g = apply_styles(g, t_styles)
            g.render(filename=t_outname, format=t_format, view=t_view_graph)

            try:
                os.remove(t_outname)
            except OSError:
                print("Couldn't remove temporary file '{}', please remove it manually".format(t_outname))

            success = True
        else:
            print("Couldn't find the reset state: this probably means that the .r keyword is missing and the transition table is empty")
    
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
   
    parser = argparse.ArgumentParser(prog="blif2graph --fsm")
    parser.add_argument("--fsm", action="store_true", default=False, help="Create an FSM graph (not needed if calling fsm2graph)")
    parser.add_argument("--input", type=str, required=True, help="Input path")
    parser.add_argument("--style", type=str, help="Style config file path")
    parser.add_argument("--output", type=str, help="Output file path (no extension)")
    parser.add_argument("--format", type=str, default="svg", help="Set output graph format")
    parser.add_argument("--view_graph", action='store_true', default=False, help="View output graph")
    parser.add_argument("--debug", action='store_true', default=False, help="View debug message")

    args = parser.parse_args(raw_args)
    print("")

    print(
        "This script was inspired by generate-stg, a tool created by Mattia Corradi and Dalla Chiara Michele:\n"
        "https://github.com/bohzio/sis-tools/blob/master/generate-stg\n\n"
    )

    if args.debug:
        boold = True
        print("[DEBUG-FSM2GRAPH] Arguments: ", args)
    
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
        success = make_fsm_graph(
            t_filepath=args.input, 
            t_styles=parsed_styles, 
            t_format=args.format,
            t_view_graph=args.view_graph
        )
    else:
        success = make_fsm_graph(
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
        print("Done. Output file path is:  {}.{}".format("fsm", args.format))
    else:
        print("Done. Output file path is:  {}.{}".format(args.output, args.format))

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
