import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import textwrap
from src.drugs import Drug
from typing import List
from src.targets import Polypeptide


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


def create_pathways_bipartite_graph(df: pd.DataFrame):
    B = nx.Graph()

    pathways = df["Pathway_ID"].unique()
    drugs = df["Drugs"].unique()

    B.add_nodes_from(pathways, bipartite=0, color="skyblue")
    B.add_nodes_from(drugs, bipartite=1, color="pink")

    edges = [(row["Pathway_ID"], row["Drugs"]) for _, row in df.iterrows()]
    B.add_edges_from(edges)

    pos = nx.bipartite_layout(B, pathways)

    labels = {}
    for node in B.nodes:
        wrapped_text = "\n".join(textwrap.wrap(node, width=13))
        labels[node] = wrapped_text

    plt.figure(figsize=(12, 10))
    node_colors = [B.nodes[node]["color"] for node in B.nodes]

    nx.draw_networkx(
        B,
        pos,
        labels=labels,
        with_labels=True,
        node_size=1200,
        node_color=node_colors,
        font_size=5,
        edge_color="gray",
        font_weight="bold",
        node_shape="o",
    )
    pathway_x = [pos[node][0] for node in pathways]
    drug_x = [pos[node][0] for node in drugs]
    y_max = max(pos[node][1] for node in B.nodes) + 0.1

    plt.text(
        min(pathway_x),
        y_max,
        "Pathway_ID",
        fontsize=10,
        ha="center",
        color="black",
    )
    plt.text(
        max(drug_x),
        y_max,
        "DrugBank_ID",
        fontsize=10,
        ha="center",
        color="black",
    )
    plt.title("Pathways and Drug Interactions Bipartite Graph")
    plt.axis("off")
    plt.tight_layout()
    plt.show()
