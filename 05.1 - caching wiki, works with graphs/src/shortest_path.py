import argparse
import json
from collections import deque
import networkx as nx
import pseudo_db as db


def search_shorted_path(graph, start, dest):
    queue = deque([[start]])
    visited = set()
    while queue:
        path = queue.popleft()
        node = path[-1]

        if node in visited:
            continue

        visited.add(node)

        if node == dest:
            return path

        for neighbor in graph[node]:
            new_path = list(path)
            new_path.append(neighbor)
            queue.append(new_path)

    return None


def create_graph_from_file(data, args):
    if args.__dict__['non_directed']:
        graph = nx.Graph()
    else:
        graph = nx.DiGraph()
    for node in data['nodes']:
        graph.add_node(node['id'], label=node['id'])
    for edge in data['edges']:
        graph.add_edge(edge['source'], edge['target'])
    return graph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--from', help='Starting point')
    parser.add_argument('--to', help='destination point')
    parser.add_argument('--non-directed', action='store_true', help='allows using any direction')
    parser.add_argument('-v', action='store_true', help='verbose i suppose')
    args = parser.parse_args()
    source = args.__dict__['from']
    target = args.__dict__['to']

    try:
        with open(db.getenv()) as file:
            data = json.load(file)
    except FileNotFoundError:
        print('database not found')
        return None

    graph = create_graph_from_file(data, args)
    path = []

    try:
        path = search_shorted_path(graph, source, target)
    except KeyError:
        pass

    if not path:
        print("No path found from", source, "to", target)
    else:
        if args.__dict__['v']:
            output = ''
            for o in (f'{i} -> ' for i in path):
                output += o
            print(output.strip(' -> ') + '\n' + str(len(path) - 1))
        else:
            print(len(path) - 1)


if __name__ == '__main__':
    main()
