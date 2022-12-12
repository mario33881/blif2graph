# BLIF2GRAPH

Generates a graph from a BLIF (SIS) file.

## Description

This library uses argparse to parse arguments:

If the ```--fsm``` flag is passed to the program the [blifparser library](https://github.com/mario33881/blifparser) 
parses the input file and blif2graph uses fsm2graph to generate an FSM graph using pygraphviz.

You can also pass other arguments together with the ```--fsm``` flag:
* ```--input```: BLIF input file path (required)
* ```--style```: INI style config file path (you can use [graphviz styles](http://www.graphviz.org/doc/info/attrs.html))
* ```--output```: Output file path (no extension)
* ```--format```: Set output graph format (default: svg)
* ```--view_graph```: View output graph (default: False)
* ```--debug```: View debug messages (default: False)
* ```--graphviz_dlls```: Path to Graphviz's DLLs.
    > Useful when the 'DLL load failed' error is thrown (tipically thrown on Windows on non-default installations).

> The fsm2graph script was inspired by [generate-stg](https://github.com/bohzio/sis-tools/blob/master/generate-stg), a tool created by Mattia Corradi and Dalla Chiara Michele

Output example:

<img src="assets/fsm.svg" height="1000px">

> [Click here to see the input file](https://github.com/arc6-202021/lib_componenti_sis/blob/f831de9f16dacf4db13f9d9eebb335ee596c5e92/fsm/controllore.blif)

If the ```--lgate``` flag is passed to the program the [blifparser library](https://github.com/mario33881/blifparser) 
parses the input file and blif2graph uses lgate2graph to generate a graph using pygraphviz.

You can also pass other arguments together with the ```--lgate``` flag:
* ```--input```: BLIF input file path (required)
* ```--style```: INI style config file path
    > Currently not used
* ```--output```: Output file path (no extension)
* ```--format```: Set output graph format (default: svg)
* ```--view_graph```: View output graph (default: False)
* ```--debug```: View debug messages (default: False)
* ```--graphviz_dlls```: Path to Graphviz's DLLs.
    > Useful when the 'DLL load failed' error is thrown (tipically thrown on Windows on non-default installations).

Output example:

<img src="assets/lgate.svg">

> Where:
> * red = input
> * blue = output
> * black = internal connection

> [Click here to see the input file](https://github.com/arc6-202021/lib_componenti_sis/blob/f831de9f16dacf4db13f9d9eebb335ee596c5e92/comparatori/comparatore4.blif)

## Requirements 
* [python 3](https://www.python.org/)
* [graphviz](https://graphviz.org/): creates the graphs
* [pygraphviz python library](https://pygraphviz.github.io/): "connects" python to graphviz
* [blifparser python library](https://pypi.org/project/blifparser/): parses BLIF files

## Installation

Install using pip:
```
pip install blif2graph
```

## Usage

You can use it from the command line:
```bash
# generates an FSM graph, fsm.blif input, fsmgraph.pdf output, view result using the default PDF viewer software at the end
python3 blif2graph.py --fsm --input fsm.blif --output fsmgraph --format pdf --view_graph
```

```bash
# generates a logic gate graph, lgate.blif input, lgategraph.pdf output, view result using the default PDF viewer software at the end
python3 blif2graph.py --lgate --input lgate.blif --output lgategraph --format pdf --view_graph
```

```bash
# generates an FSM graph, myfsm.blif input, default fsm.svg output, custom graphviz style, view result using the default SVG viewer software at the end
python3 blif2graph.py --fsm --input myfsm.blif --style mystyles.ini --view_graph
```

Example of an FSM custom style file:

```ini
[graph]
fontsize = 16
fontcolor = black
fontname = Times-Roman
rankdir = TB             # TB: top to bottom (inverse: BT), LR: left to right (inverse: RL)
splines = true
overlap = false
size = 8,5
bgcolor = transparent  
center = true
charset = UTF-8
colorscheme = 
concentrate = false   # true: concentrate arrows together in one line until a certain point
dpi = 96.0

[edges]
fontsize = 16
arrowsize = .5
arrowhead = normal
arrowtail = normal
color = gray31
fillcolor = black
fontcolor = black
fontname = Times-Roman
colorscheme = 
constraint = true
decorate = true
dir = forward
penwidth = 1.0

[nodes]
fontsize = 16
colorscheme = 
color = black
fillcolor = black
fontcolor = black
fontname = Times-Roman
penwidth = 2.0
```

You can also import the script and call the main() function passing a list of arguments:

```py
import blif2graph
params = "   --fsm  --input    ..\\myfsm.blif --format  pdf  --view_graph   "
params = [param for param in params.split(" ") if param.strip() != ""]
blif2graph.main(params)
```

## Changelog 

**WIP 2.0.0:** <br>

## Features

* Added lgate2graph logic: generates a graph from logic gates.

## Fixes
* Better fsm default styles
    > Example: the background color is white instead of transparent. This is preferable when the background of a viewer application is dark (the background allows you to see the lines and text).
* Ignore DPI setting when the output format is "svg"
    > Before this fix the svg got cut off

**2021-09-10 1.0.0:** <br>
First commit

## Author
[Stefano Zenaro (mario33881)](https://github.com/mario33881)
