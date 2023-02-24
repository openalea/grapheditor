# GraphEditor 

**Authors** : Daniel Barbeau

**Institutes** : INRIA / CIRAD 

**Status** : Python package 

**License** : Cecill-C

**URL** : http://github.com/openalea

## About 

### Description 

The grapheditor package is an attempt to provide a general framework for graph visualisation
and editing. The goal is to generalise as much as can be of the visualisation and interaction
process so the users of this package can more easily define how a tree or a dataflow should be
viewed and interacted with.
To acheive this, we make more heavy use of the observer/observed system from openalea.core and
define contracts that need to be satisfied by both the observers and the observed so that they
collaborate nearly out-of-the-box.
We also create a mapping between graph types and viewing strategies. If the graph is a dataflow
we will choose the dataflow viewing strategy.
  
### Content 

The grapheditor package contains :

  - generic graph observer and interaction classes and interfaces. 
  - a canvas for Qt
  - an implementation of a dataflow viewer.

### Requirements 

- OpenAlea.Core
- qtpy
- Python >= 3.7
- Qt >= 5.12
- QtPy (PyQt >= 5.12)


## Using GraphEditor 

GraphEditor is a framework. It ships with some graph viewing strategies.
The `nx_app.py` in `example` demonstrates how to create views for graphs from the networkx http://networkx.org toolkit. This toolkit provides efficient graph structures. In this example, we want to create a Qt widget that allows one to view/create networkx graphs and edit them.

We need to define:

- observers that manage modification according to events, like key pressed, mouse moves, etc.,
- a node that will represent a vertex on the graph view,
- a graphical view.

### Observers
We define an observer for the vertices.
```
class NxObservedVertex(Observed):

    def __init__(self, graph, identifier):
        Observed.__init__(self)
        self.identifier = identifier
        self.g = weakref.ref(graph)

    def notify_position(self, pos):
        self.notify_listeners(("metadata_changed", "position", pos))

    def notify_update(self, **kwargs):
        for k, v in kwargs.items():
            self.notify_listeners(("metadata_changed", k, v))

        pos = self.g().nodes[self]["position"]
        self.notify_position(pos)

    def __setitem__(self, key, value):
        self.g().nodes[self][key] = value
        self.notify_update()

    def __getitem__(self, key):
        return self.g().nodes[self][key]
```
And one for the graph view:
```
class NXObservedGraph( GraphAdapterBase, Observed ):
    """An adapter to networkx.Graph"""
    def __init__(self):
        GraphAdapterBase.__init__(self)
        Observed.__init__(self)
        self.set_graph(nx.Graph())

    def new_vertex(self, vid=None, **kwargs):
        vtx = NxObservedVertex(self.graph, vid)
        self.add_vertex(vtx, **kwargs)
        return vtx

    def add_vertex(self, vertex, **kwargs):
        if vertex in self.graph:
            return
        else:
            if "position" not in kwargs : 
                kwargs["position"] = [0., 0.]
            else:
                kwargs["position"] = list(map(float, kwargs["position"]))
            if "color" not in kwargs :
                kwargs["color"] = QtGui.QColor(0, 0, 0)

            self.graph.add_node(vertex, **kwargs)
            self.notify_listeners(("vertex_added", ("vertex", vertex)))

    def remove_vertex(self, vertex):
        edges = self.graph.edges([vertex])
        for src, tgt in edges:
            self.remove_edge(src, tgt)
        self.graph.remove_node(vertex)
        self.notify_listeners(("vertex_removed", ("vertex",vertex)))

    def add_edge(self, src_vertex, tgt_vertex, **kwargs):
        edge = [src_vertex, tgt_vertex]
        edge.sort(key=cmp_to_key(cmp))
        edge = tuple(edge)
        if self.graph.has_edge(*edge):
            return
        else:
            self.graph.add_edge(*edge, **kwargs)
            self.notify_listeners(("edge_added", ("default", edge, src_vertex, tgt_vertex)))

    def remove_edge(self, src_vertex, tgt_vertex):
        edge =  [src_vertex, tgt_vertex]
        edge.sort(key=cmp_to_key(cmp))
        edge = tuple(edge)
        self.graph.remove_edge(edge[0], edge[1])
        self.notify_listeners(("edge_removed", ("default",edge)))

    def remove_edges(self, edges):
        GraphAdapterBase.remove_edges(self, (e for e in edges))

    # -- not in the adapter interface (yet): --
    def set_vertex_data(self, vertex, **kwargs):
        if vertex in self.graph:
            for k, v in kwargs.items():
                self.graph.nodes[vertex][k]=v

    def set_edge_data(self, edge_proxy, **kwargs):
        #nothing right now
        pass
```



