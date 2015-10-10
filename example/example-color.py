# @brief    This file is just a test script for the features of networkxgmml

import networkx as nx
import networkxgmml as nml

g1 = nx.Graph()
g1.add_node('a', color='#00FF00', magnitude=3)
g1.add_node('b', color='#00FF00', magnitude=7)
g1.add_node('c', color='#FF0000', magnitude=5)
g1.add_node('d', color='#00FF00', magnitude=1)
g1.add_node('e', magnitude=2)
g1.add_node('f', magnitude=0)
g1.add_node('g', magnitude=9)

g1.add_edge('a', 'e', weight=2.5)
g1.add_edge('a', 'c', weight=1.5)
g1.add_edge('d', 'e', weight=2.0)
g1.add_edge('a', 'e', weight=2.5)
g1.add_edge('c', 'b', weight=0.5)
g1.add_edge('e', 'f', weight=0.5)
g1.add_edge('g', '1', weight=4.5)


with open('output/example_mynml.xgmml', 'w+') as f:
    nml.XGMMLWriter(f, g1, 'Test nml1')

with open('output/example_mynml_undir.xgmml', 'w+') as f:
    nml.XGMMLWriter(f, g1, 'Test nml2', directed=False)

# An assertion error example
# f = open('example_mynml_fail.xgmml', 'w+')
# nml.XGMMLWriter(f, g1, 'Test nml2', directed=2)
# f.close()
