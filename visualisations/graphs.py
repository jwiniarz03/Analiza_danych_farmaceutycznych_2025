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
    """

    G = nx.Graph()

    synonyms = []
