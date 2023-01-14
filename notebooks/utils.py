from pyvis.network import Network



def pyvis_network(edges):
    net = Network(notebook=True)
    nodes = dict()
    for edge in edges:
        src = edge.src.split("/")[-1]
        dst = edge.dst.split("/")[-1]
        if src not in nodes:
            nodes[src] = len(nodes)
        if dst not in nodes:
            nodes[dst] = len(nodes)
        net.add_node(nodes[src], label=src)
        net.add_node(nodes[dst], label=dst)
        net.add_edge(nodes[src], nodes[dst])

    return net
