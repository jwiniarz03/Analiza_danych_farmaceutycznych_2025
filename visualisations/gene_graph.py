import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt
import textwrap


def wrap_text(text: str, width: int) -> str:
    """
    Wraps the given text into multiple lines with a maximum of `width` characters per line.

    Args:
        text (str): The input text to be wrapped.
        width (int): The maximum number of characters per line.

    Returns:
        str: The wrapped text with newline characters inserted.
    """
    return "\n".join(textwrap.wrap(text, width))


def create_plot(xml, path_to_save, gene_id):
    tree = ET.parse(xml)
    root = tree.getroot()

    # Namespace handling for XML parsing
    ns = {"db": "http://www.drugbank.ca"}

    drugs = []
    results = {}

    for drug in root.findall("db:drug", ns):
        for target in drug.findall("db:targets/db:target/db:polypeptide", ns):
            if target.find("db:gene-name", ns).text == gene_id:
                drug_id = drug.find("db:drugbank-id[@primary='true']", ns).text
                drugs.append(drug_id)

    graph = nx.DiGraph()

    graph.add_node(gene_id, color="skyblue", label=wrap_text(gene_id, 10))
    for drug in drugs:
        graph.add_node(drug, color="lightgreen", label=wrap_text(drug, 10))
        graph.add_edge(gene_id, drug, color="black")

    for drug in root.findall("db:drug", ns):
        drug_id = drug.find("db:drugbank-id[@primary='true']", ns).text
        if drug_id in drugs:
            results[drug_id] = []
            for product in drug.findall("db:products/db:product", ns):
                product_name = product.find("db:name", ns).text
                if product_name not in results[drug_id]:
                    results[drug_id].append(product_name)
                    graph.add_node(
                        product_name, color="pink", label=wrap_text(product_name, 10)
                    )
                    graph.add_edge(drug_id, product_name, color="grey")

    colors = nx.get_node_attributes(graph, "color").values()
    edge_colors = nx.get_edge_attributes(graph, "color").values()
    labels = nx.get_node_attributes(graph, "label")

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph)
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=1200,
        node_color=colors,
        labels=labels,
        font_size=8,
        edge_color=edge_colors,
    )
    if path_to_save:
        plt.savefig(path_to_save)
    else:
        plt.show()
