import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import textwrap


def generate_synonyms_graph(drug_id: str, synonyms_df: pd.DataFrame) -> nx.Graph:
    """
    Generate a star graph of synonyms for given drug id.

    Args:
        drug_id (str): The DrugBank ID for which to generate the graph.
        synonyms_data (pd.DataFrame): DataFrame containing drug ids and synonyms.

    Returns:
        nx.Graph: The generated star graph of synonyms.

    Raises:
        ValueError: If no synonyms are found for the given DrugBank ID.
    """

    row = synonyms_df[synonyms_df["drug_id"] == drug_id]

    if row.empty:
        raise ValueError(f"No synonyms found for DrugBank ID {drug_id}")

    synonyms = row.iloc[0]["synonyms"].split("\n")

    G = nx.Graph()

    G.add_node(drug_id)

    for synonym in synonyms:
        G.add_node(synonym)
        G.add_edge(drug_id, synonym)

    return G


def plot_synonyms_graph(G: nx.Graph, drug_id: str):
    """
    Generate matplotlib plot of synonyms for the given DrugBank ID.

    Args:
        G (nx.Graph): The graph to plot.
        drug_id (str): The DrugBank ID of which the graph is generated.
    """

    plt.figure(figsize=(8, 6))

    position = nx.spring_layout(G)
    nx.draw_networkx_edges(G, position)
    nx.draw_networkx_nodes(G, position, node_size=3000)

    labels = {}
    for node in G.nodes:
        wrapped_text = "\n".join(textwrap.wrap(node, width=20))
        labels[node] = wrapped_text
    nx.draw_networkx_labels(
        G, position, labels, font_size=6, font_color="white", verticalalignment="center"
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


def create_pie_plot_targets(df: pd.DataFrame) -> plt.pie:
    agregated_data = (
        df.groupby("Cellular location")
        .agg(nr_of_targets=("DrugBank ID", "count"))
        .reset_index()
    )
    total_targets = len(df.index)
    agregated_data["Percentage"] = (
        agregated_data["nr_of_targets"] / total_targets
    ) * 100

    data = agregated_data["Percentage"]
    locations = agregated_data["Cellular location"]
    filtered_data = agregated_data[agregated_data["Percentage"] > 3]
    filtered_labels = filtered_data["Cellular location"]

    plt.figure(figsize=(10, 8))
    plt.pie(
        data,
        labels=[
            label if label in filtered_labels.values else "" for label in locations
        ],
        autopct=lambda p: f"{p:.1f}%" if p > 3 else "",
        startangle=90,
    )
    plt.title("Distribution of Cellular Locations")
    plt.legend(
        locations,
        title="Cellular Locations",
        loc="upper left",
        fontsize="small",
    )
    plt.show()
