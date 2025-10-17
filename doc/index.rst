Welcome to OpenAlea GraphEditor's documentation!
################################################

.. figure:: _static/front_image.png

 **networkx application example**

GraphEditor is a set of classes that make it easier to implement editors and views for graph structures than having
to start from scratch. GraphEditor makes no assumption concerning the underlying data structure except that it is made
of vertices and edges. However it expects a way to observe the structure but incorporates the notion of structure wrapper
to easily build a wrapper around an existing structure that doesn't implement [at all|the expected] observer pattern.


In the end the client usually only implements the widgets that represent vertices and edges and how the user interacts with them.


Some keys to the understanding of how GraphEditor works are :

* the Model-View-Controller paradigm
* the Strategy pattern

Documentation
=============

.. toctree::
    :maxdepth: 2

    Tutorial<user/netx.rst>
    Reference Guide<user/autosum.rst>

