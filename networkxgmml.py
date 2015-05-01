import xml.parsers.expat
import networkx as nx

class XGMMLParserHelper(object):
    """
    """
    
    def __init__(self):
        """
        
        Arguments:
        - `graph`: Network X graph object
        """
        self._graph = nx.DiGraph()
        self._parser = xml.parsers.expat.ParserCreate()
        self._parser.StartElementHandler = self._start_element
        self._parser.EndElementHandler = self._end_element
        self._tagstack = list()

        self._network_att_el = dict()
        self._current_att_el = dict()
        self._current_list_att_el = list()
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
            self._network_att_el = dict()
        
        if tag == 'node' or tag == 'edge':
            self._current_obj = dict(attr)

        if tag == 'att' and (self._tagstack[-2] == 'node' or self._tagstack[-2] == 'edge'):
            if 'value' in attr:
                self._current_att_el = self._parse_att_el(self._current_att_el, tag, attr)
            elif attr['type'] == 'list':
                self._current_list_name = attr['name']
                self._current_att_el[attr['name']] = list()

        if tag == 'att' and (self._tagstack[-2] == 'att'):
            self._current_list_att_el = dict(attr)
            if 'value' in attr:
                self._current_list_att_el = self._parse_att_el(self._current_list_att_el, tag, attr)
                self._current_att_el[self._current_list_name].append(self._current_list_att_el[attr['name']])

        if tag == 'att' and self._tagstack[-2] == 'graph':
            if 'value' in attr:
                self._network_att_el[attr['name']] = attr['value']

    def _parse_att_el(self, att_el, tag, attr):
        """
        
        Arguments:
        - `self`:
        - `att_el`: att element. Can be child of node, edge or another att.
        - `tag`:
        - `attr`:
        """

        if 'value' in attr:
            if attr['type'] == 'string':
                att_el[attr['name']] = attr['value']
            elif attr['type'] == 'real':
                att_el[attr['name']] = float(attr['value'])
            elif attr['type'] == 'integer':
                att_el[attr['name']] = int(attr['value'])
            elif attr['type'] == 'boolean':
                att_el[attr['name']] = bool(attr['value'])
            else:
                raise NotImplementedError(attr['type'])

            return att_el

    def _end_element(self, tag):
        """
        
        Arguments:
        - `self`:
        - `tag`:
        """

        if tag == 'node':
            if 'label' in self._current_obj:
                if 'label' in self._current_att_el:
                    self._current_att_el['@label'] = self._current_att_el['label']
                    del self._current_att_el['label']
                self._graph.add_node(self._current_obj['id'], label=self._current_obj['label'], **self._current_att_el)
            else:
                self._graph.add_node(self._current_obj['id'], **self._current_att_el)
        elif tag == 'edge':
            self._graph.add_edge(self._current_obj['source'], self._current_obj['target'], **self._current_att_el)

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

        return self._network_att_el

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
  <att name="shared name" value="{0}" type="string"/>""".format(graph_name)

    def quote(text):
        """
        
        Arguments:
        - `text`:
        """

        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def write_att_el(k, v, indent_count):
        indentation_string = ''
        for i in range(0, indent_count):
            indentation_string += '  '
        if isinstance(v, int):
            print >>file, indentation_string + '<att name="{}" value="{}" type="integer" />'.format(k, v)
        elif isinstance(v, bool):
            print >>file, indentation_string + '<att name="{}" value="{}" type="boolean" />'.format(k, v)
        elif isinstance(v, float):
            print >>file, indentation_string + '<att name="{}" value="{}" type="real" />'.format(k, v)
        elif hasattr(v, '__iter__'):
            print >>file, indentation_string + '<att name="{}" type="list">'.format(k)
            for item in v:
                write_att_el(k, item, 3)
            print >>file, indentation_string + '</att>'
        else:
            print >>file, indentation_string + '<att name="{}" value="{}" type="string" />'.format(k, quote(v))

    for onenode in graph.nodes(data=True):
        id = onenode[0]
        attr = dict(onenode[1])

        if 'label' in attr:
            label = attr['label']
            del attr['label']
        else:
            label = id
        
        print >>file, '  <node id="{id}" label="{label}">'.format(id=id, label=label)
        for k, v in attr.iteritems():
            write_att_el(k, v, 2)

        print >>file, '  </node>'
        
    for oneedge in graph.edges(data=True):
        print >>file, '  <edge source="{}" target="{}">'.format(oneedge[0], oneedge[1])
        for k, v in oneedge[2].iteritems():
            write_att_el(k, v, 2)
        print >>file, '  </edge>'
    print >>file, '</graph>'
