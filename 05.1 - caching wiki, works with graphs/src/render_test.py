import unittest
import render_graph as rg
import networkx as nx
from pyvis.network import Network


class TestingRender(unittest.TestCase):

    data = {
              "nodes": [
                {
                  "id": "Python (programming language)",
                  "label": "Python"
                }
              ],
              "edges": [
                {
                  "source": "Python (programming language)",
                  "target": "Computer science"
                }
              ]
            }

    def test_count_nodes_edges(self):
        c = rg.count_nodes_edges(self.data)
        self.assertIsInstance(c, dict)

    def test_create_net(self):
        c = rg.count_nodes_edges(self.data)
        n = rg.create_net(self.data, c)
        self.assertIsInstance(n, Network)

    def test_create_graph(self):
        c = rg.count_nodes_edges(self.data)
        g = rg.create_network_graph(self.data, c)
        self.assertIsInstance(g, nx.Graph)


if __name__ == '__main__':
    unittest.main()
