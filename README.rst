=============
networkxxgmml
=============

XGMML parser for networkx

-------
Install
-------

    pip install networkxgmml

That's all!


----
APIs
----

XGMMLReader(graph_file)
-----------------

Argument: graph_file: a file-like object contains XGMML

Return: a networkx.DiGraph object

    
XGMMLWriter(graph_file, graph, graph_name, directed=True)
------------------------------------

* file: a file-like object to write XGMML
* graph: a networkx.Graph object
* graph_name: a name of a network
* directed: is directed graph or not

-------
License
-------

Distributed with a MIT license

------------
Contributors
------------

* Yasunobu OKAMURA
* Anders Riutta
* Jeff Yunes
* Gustavo Pereira

