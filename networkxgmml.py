import xml.parsers.expat
import networkx as nx

class XGMMLParserHelper(object):
    """
    """
    
    def __init__(self, graph=nx.DiGraph()):
        """
        
        Arguments:
        - `graph`: Network X graph object
        """
        self._graph = graph
        self._parser = xml.parsers.expat.ParserCreate()
        self._parser.StartElementHandler = self._start_element
        self._parser.EndElementHandler = self._end_element
        self._tagstack = list()

        self._network_attr = dict()
        self._current_attr = dict()
        self._current_obj = dict()

    def _start_element(self, tag, attr):
        """
        
        Arguments:
        - `self`:
        - `tag`:
        - `attr`:
        """

        self._tagstack.append(tag)

        if tag == 'graph':
            self._network_attr = dict()
        
        if tag == 'node' or tag == 'edge':
            self._current_obj = dict(attr)

        if tag == 'att' and (self._tagstack[-2] == 'node' or self._tagstack[-2] == 'edge'):
            if attr['type'] == 'string':
                self._current_attr[attr['name']] = attr['value']
            elif attr['type'] == 'real':
                self._current_attr[attr['name']] = float(attr['value'])
            elif attr['type'] == 'integer':
                self._current_attr[attr['name']] = int(attr['value'])
            elif attr['type'] == 'boolean':
                self._current_attr[attr['name']] = bool(attr['value'])
            else:
                raise NotImplementedError(attr['type'])

        if tag == 'att' and self._tagstack[-2] == 'graph':
            self._network_attr[attr['name']] = attr['value']

    def _end_element(self, tag):
        """
        
        Arguments:
        - `self`:
        - `tag`:
        """

        if tag == 'node':
            self._graph.add_node(self._current_obj['id'], label=self._current_obj['label'], **self._current_attr)
            #print 'add node', self._current_obj
        elif tag == 'edge':
            self._graph.add_edge(self._current_obj['source'], self._current_obj['target'], **self._current_attr)

        self._tagstack.pop()

    def parseFile(self, file):
        """
        
        Arguments:
        - `self`:
        - `file`:
        """

        self._parser.ParseFile(file)

    def graph(self):
        """
        
        Arguments:
        - `self`:
        """

        return self._graph

    def graph_attributes(self):
        """
        
        Arguments:
        - `self`:
        """

        return self._network_attr

def XGMMLReader(file):
    """
    
    Arguments:
    - `file`:
    """

    parser = XGMMLParserHelper()
    parser.parseFile(file)
    return parser.graph()


def XGMMLWriter(file, graph, graph_name):
    """
    
    Arguments:
    - `graph`:
    """

    print >>file, """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<graph directed="1"  xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://www.cs.rpi.edu/XGMML">
<att name="selected" value="1" type="boolean" />
<att name="name" value="{0}" type="string"/>
<att name="shared name" value="{0}" type="string"/>
""".format(graph_name)

    def quote(text):
        """
        
        Arguments:
        - `text`:
        """

        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt')


    for onenode in graph.nodes(data=True):
        id = onenode[0]
        attr = dict(onenode[1])

        if 'label' in attr:
            label = attr['label']
            del attr['label']
        else:
            label = id
        
        print >>file, '<node id="{id}" label="{label}">'.format(id=id, label=label)
        for k, v in attr.iteritems():
            if isinstance(v, int):
                print >>file, '<att name="{}" value="{}" type="integer" />'.format(k, v)
            elif isinstance(v, bool):
                print >>file, '<att name="{}" value="{}" type="boolean" />'.format(k, v)
            elif isinstance(v, float):
                print >>file, '<att name="{}" value="{}" type="real" />'.format(k, v)
            else:
                print >>file, '<att name="{}" value="{}" type="string" />'.format(k, quote(v))

        print >>file, '</node>'
        
    for oneedge in graph.edges(data=True):
        print >>file, '<edge source="{}" target="{}">'.format(oneedge[0], oneedge[1])
        for k, v in oneedge[2].iteritems():
            if isinstance(v, int):
                print >>file, '<att name="{}" value="{}" type="integer" />'.format(k, v)
            elif isinstance(v, bool):
                print >>file, '<att name="{}" value="{}" type="boolean" />'.format(k, v)
            elif isinstance(v, float):
                print >>file, '<att name="{}" value="{}" type="real" />'.format(k, v)
            else:
                print >>file, '<att name="{}" value="{}" type="string" />'.format(k, quote(v))
        print >>file, '</edge>'
    print >>file, '</graph>'
