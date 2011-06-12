======================================================
graphcanvas: interactive graph (network) visualization
======================================================

graphcanvas is an library for interacting with visualizations of complex
graphs. The aim is to allow the developer to declare the graph by the
simplest means and be able to visualize the graph immediately.

For example::

    from graphcanvas.api import GraphView, graph_from_dict
    g = {'a':['b'], 'b':['c', 'd'], 'c':[], 'd':[]}
    GraphView(graph=graph_from_dict(g)).configure_traits()


Prerequisites
-------------

* `NetworkX <http:://networkx.lanl.gov>`_
* `distribute <http://pypi.python.org/pypi/distribute>`_
* enable
