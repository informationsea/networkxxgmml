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

        if tag == 'att' and (self._tagstack[-2] == 'node' or
                             self._tagstack[-2] == 'edge'):
            if 'value' in attr:
                self._current_att_el = self._parse_att_el(self._current_att_el,
                                                          tag, attr)
            elif attr['type'] == 'list':
                self._current_list_name = attr['name']
                self._current_att_el[attr['name']] = list()

        if tag == 'att' and (self._tagstack[-2] == 'att'):
            self._current_list_att_el = dict(attr)
            if 'value' in attr:
                self._current_list_att_el = self._parse_att_el(
                    self._current_list_att_el, tag, attr)
                self._current_att_el[self._current_list_name].append(
                    self._current_list_att_el[attr['name']])

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

                self._graph.add_node(self._current_obj['id'],
                                     label=self._current_obj['label'],
                                     **self._current_att_el)
            else:
                self._graph.add_node(self._current_obj['id'],
                                     **self._current_att_el)
        elif tag == 'edge':
            self._graph.add_edge(self._current_obj['source'],
                                 self._current_obj['target'],
                                 **self._current_att_el)

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


def XGMMLReader(graph_file):
    """

    Arguments:
    - `file`:
    """

    parser = XGMMLParserHelper()
    parser.parseFile(graph_file)
    return parser.graph()


def XGMMLWriter(graph_file, graph, graph_name, directed=True):
    """

    Arguments:
    - `graph_file` output network file (file object)
    - `graph`: NetworkX Graph Object
    - `graph_name`: Name of the graph
    - `directed`: is directed or not
    """

    graph_file.write("""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<graph directed="{directed}"  xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://www.cs.rpi.edu/XGMML">
 <att name="selected" value="1" type="boolean" />
 <att name="name" value="{0}" type="string"/>
 <att name="shared name" value="{0}" type="string"/>\n""".format(graph_name, directed=(1 if directed else 0)))

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
            graph_file.write(
                indentation_string +
                '<att name="{}" value="{}" type="integer" />\n'.format(k, v))
        elif isinstance(v, bool):
            graph_file.write(
                indentation_string +
                '<att name="{}" value="{}" type="boolean" />\n'.format(k, v))
        elif isinstance(v, float):
            graph_file.write(
                indentation_string +
                '<att name="{}" value="{}" type="real" />\n'.format(k, v))
        elif isinstance(v, str):
            graph_file.write(
                indentation_string +
                '<att name="{}" value="{}" type="string" />\n'.format(k, v))
        elif hasattr(v, '__iter__'):
            graph_file.write(
                indentation_string + '<att name="{}" type="list">\n'.format(k))
            for item in v:
                write_att_el(k, item, 3)
            graph_file.write(indentation_string + '</att>\n')
        else:
            graph_file.write(
                indentation_string +
                '<att name="{}" value="{}" type="string" />\n'.format(k,
                                                                    quote(v)))

    for onenode in graph.nodes(data=True):
        id = onenode[0]
        attr = dict(onenode[1])

        if 'label' in attr:
            label = attr['label']
            del attr['label']
        else:
            label = id

        graph_file.write(
            '  <node id="{id}" label="{label}">\n'.format(id=id, label=label))

        # Add color element
        if 'color' in attr:
            color = attr['color']
            del attr['color']
            graph_file.write(
                '  <graphics fill="{color}" />\n'.format(color=color))

        for k, v in iter(attr.items()):
            write_att_el(k, v, 2)

        graph_file.write('  </node>\n')

    for oneedge in graph.edges(data=True):
        #
        # The spec, http://cgi5.cs.rpi.edu/research/groups/pb/punin/public_html/XGMML/draft-xgmml.html#GlobalA,
        # requires an "id", even for edges. This id is supposed to be unique across the entire document, so it
        # can't be equal to one of the node ids. We're making the assumption that whoever created the graph
        # object knew about and respected the "uniqueness" requirement, and passed a suitable id as the attribute
        # "id" to the edge. If the creator of the graph *didn't* pass a unique id, the best I can come up with at
        # this moment is to just ignore the id requirement entirely.
        #
        if 'id' in oneedge[2]:
            edge_id = oneedge[2].pop("id", None)
            graph_file.write('  <edge id="{}" source="{}" target="{}">\n'.format(
                edge_id, oneedge[0], oneedge[1]))
        else:
            graph_file.write('  <edge source="{}" target="{}">\n'.format(
                oneedge[0], oneedge[1]))

        for k, v in iter(oneedge[2].items()):
            write_att_el(k, v, 2)
        graph_file.write('  </edge>\n')
    graph_file.write('</graph>\n')
