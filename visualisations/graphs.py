import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


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
