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
