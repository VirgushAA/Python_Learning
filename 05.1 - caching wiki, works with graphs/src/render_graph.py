import json
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pseudo_db as db


def count_nodes_edges(data):
    node_edge_count = {}

    for edge in data['edges']:
        source = edge['source']
        target = edge['target']

        if source not in node_edge_count:
            node_edge_count[source] = 0
        node_edge_count[source] += 1

        if target not in node_edge_count:
            node_edge_count[target] = 0
        node_edge_count[target] += 1
    return node_edge_count


def create_net(data, node_edge_count):
    net = Network(notebook=True)

    for node, count in node_edge_count.items():
        size = count * 2 + 100
        net.add_node(node, label=node, size=size)

    for edge in data['edges']:
        net.add_edge(edge['source'], edge['target'])

    return net


def create_network_graph(data, node_edge_count):
    graph = nx.Graph()
    for node, count in node_edge_count.items():
        size = (count + 1) * 2
        graph.add_node(node, label=node, size=size)

    for edge in data['edges']:
        graph.add_edge(edge['source'], edge['target'])

    return graph


def process_figure(graph, node_edge_count) -> None:
    plt.figure(figsize=(16, 12), dpi=1000)
    pos = nx.spring_layout(graph)
    sizes = [(node_edge_count[node] + 1) * 10 for node in graph.nodes()]
    nx.draw(graph, pos, with_labels=True, node_size=sizes, node_color='lightblue', font_size=1, font_weight='bold',
            width=0.2, arrows=True)
    plt.title(f"Representation of wikipedia")

    plt.savefig('wiki_graph.png', format='png', bbox_inches='tight')
    plt.close()


def main():
    try:
        with open(db.getenv()) as file:
            data = json.load(file)
    except FileNotFoundError:
        print('database not found')
        return None

    node_edge_count = count_nodes_edges(data)
    net = create_net(data, node_edge_count)

    graph = create_network_graph(data, node_edge_count)
    process_figure(graph, node_edge_count)
    net.show('wiki_graph.html')


if __name__ == '__main__':
    main()
