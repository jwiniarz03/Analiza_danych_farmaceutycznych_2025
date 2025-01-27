import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import textwrap
from src.drugs import Drug
from typing import List


def generate_draw_synonyms_graph(drug_id: str, drugs: List[Drug]) -> None:
    """
    Generate and draw a star graph of synonyms for a given DrugBank ID.

    Args:
        drug_id (str): The DrugBank ID of a given drug.
        drugs (List[Drug]): List of Drug objects with drug data.
    """

    drug = None
    for d in drugs:
        if d.drug_id == drug_id:
            drug = d
            break

    if not drug:
        raise ValueError(f"DrugBank ID {drug_id} not found.")

    if not drug.synonyms:
        raise ValueError(f"Drug with ID {drug_id} has no synonyms.")

    G = nx.Graph()
    G.add_node(drug_id, label="DrugBank ID")

    for synonym in drug.synonyms:
        G.add_node(synonym, label="Synonym")
        G.add_edge(drug_id, synonym)

    plt.figure(figsize=(10, 8))

    position = nx.spring_layout(G, seed=0)
    nx.draw_networkx_nodes(
        G, position, node_size=5000, node_color="lightblue", edgecolors="black"
    )
    nx.draw_networkx_edges(G, position)
    # nx.draw_networkx_labels(
    #     G, position, font_size=10, font_color="black", font_weight="bold"
    # )
    labels = {}
    for node in G.nodes:
        wrapped_text = "\n".join(textwrap.wrap(node, width=10))
        labels[node] = wrapped_text
    nx.draw_networkx_labels(
        G,
        position,
        labels,
        font_size=10,
        font_color="black",
        verticalalignment="center",
    )
    plt.title(f"Star Graph for DrugBank ID: {drug_id}")

    plt.show()


class BipartiteGraph:
    def __init__(self):
        """
        Initialize the bipartite graph with two sets of vertices and an adjacency list.
        """
        self.P = set()  # First set of vertices --> Pathways
        self.D = set()  # Second set of vertices --> Drugs
        self.adj_list = {}  # Adjacency list to store edges

    def add_vertex(self, vertex, set_type):

        if set_type == "P":
            self.P.add(vertex)
        elif set_type == "D":
            self.D.add(vertex)
        else:
            raise ValueError("set_type must be either 'U' or 'V'")
        # Initialize the adjacency list for the new vertex
        self.adj_list[vertex] = []

    def add_edge(self, p, d):
        if (p in self.P and d in self.D) or (p in self.D and d in self.P):
            self.adj_list[p].append(d)
            self.adj_list[d].append(p)
        else:
            raise ValueError("Edge must connect vertices from different sets")

    def is_bipartite(self):
        color = {}
        for vertex in list(self.U) + list(self.V):
            if vertex not in color:
                if not self._bfs_check(vertex, color):
                    return False
        return True

    def _bfs_check(self, start, color):
        from collections import deque

        queue = deque([start])
        color[start] = 0  # Start coloring with color 0

        while queue:
            vertex = queue.popleft()
            current_color = color[vertex]

            for neighbor in self.adj_list[vertex]:
                if neighbor not in color:
                    color[neighbor] = 1 - current_color  # Alternate color
                    queue.append(neighbor)
                elif color[neighbor] == current_color:
                    return False

        return True

    def display(self):
        print("Set P:", self.P)
        print("Set D:", self.D)
        print("Adjacency List:")
        for vertex, neighbors in self.adj_list.items():
            print(f"{vertex}: {neighbors}")
