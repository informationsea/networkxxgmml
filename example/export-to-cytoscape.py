#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import networkx as nx
import networkxgmml

def _main():
    parser = argparse.ArgumentParser(description="Write XGMML for Cytoscape")
    parser.add_argument('export', default='output/exported.xgmml', type=argparse.FileType('w'), help='default: %(default)s', nargs='?')
    options = parser.parse_args()

    g = nx.Graph()

    # add cliques
    clique_nodes1 = [1, 2, 3, 4, 5]
    clique_nodes2 = [6, 7, 8, 9, 10]

    for i1, n1 in enumerate(clique_nodes1):
        for i2, n2 in enumerate(clique_nodes1[i1+1:]):
            g.add_edge(n1, n2)

    for i1, n1 in enumerate(clique_nodes2):
        for i2, n2 in enumerate(clique_nodes2[i1+1:]):
            g.add_edge(n1, n2)

    # add edges between cliques

    g.add_edge(1, 7)
    g.add_edge(3, 9)


    # export network with new name
    networkxgmml.XGMMLWriter(options.export, g, "New Graph")
    print 'XGMML is exported to {0}'.format(options.export.name)

if __name__ == '__main__':
    _main()
