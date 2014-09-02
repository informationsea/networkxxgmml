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

XGMMLReader(file)
-----------------

Argument: file: a file-like object contains XGMML

Return: a networkx.DiGraph object

    
XGMMLWriter(file, graph, graph_name)
------------------------------------

* file: a file-like object to write XGMML
* graph: a networkx.Graph object
* graph_name: a name of a network

-------
License
-------

Distributed with a MIT license

---------
Copyright
---------

Copyright (C) 2014 Yasunobu OKAMURA
