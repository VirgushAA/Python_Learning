import unittest
import shortest_path
import networkx as nx


class TestingShortestPath(unittest.TestCase):

    def test_search_shorted_path(self):
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
        g = nx.Graph()
        g.add_node(node['id'] for node in data['nodes'])
        for edge in data['edges']:
            g.add_edge(edge['source'], edge['target'])
        p = shortest_path.search_shorted_path(g, "Python (programming language)", "Computer science")
        self.assertIsInstance(p, list)


if __name__ == '__main__':
    unittest.main()
