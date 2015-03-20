#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import networkx as nx
import networkxgmml
import json

def _main():
    parser = argparse.ArgumentParser(description="Read network from Cytoscape")
    parser.add_argument('XGMML', default=file('./yeast-ppi.xgmml'), help='XGMML file exported from Cytoscape  default: %(default)s', nargs='?', type=argparse.FileType('r'))
    parser.add_argument('edgelist', default='./output/yeast-ppi-edgelist.txt', nargs='?', help='edge list output path  [default: %(default)s]')
    parser.add_argument('nodelist', default='./output/yeast-ppi-nodelist.txt', nargs='?', help='node list output path  [default: %(default)s]')
    options = parser.parse_args()

    g = networkxgmml.XGMMLReader(options.XGMML)

    print '# of edges', len(g.edges())
    with file(options.edgelist, 'w') as f:
        for n1, n2 in g.edges():
            print >>f, '\t'.join([n1, n2, json.dumps(g.edge[n1][n2])])

    print 'edge list is exported to {0}'.format(options.edgelist)

    print '# of nodes', len(g.nodes())
    with file(options.nodelist, 'w') as f:
        for onenode in g.nodes():
            print >>f, '\t'.join([onenode, json.dumps(g.node[onenode])])

    print 'node list is exported to {0}'.format(options.nodelist)
    

if __name__ == '__main__':
    _main()
