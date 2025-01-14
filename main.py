from data_processing.data_loader import (
    load_basic_drug_data,
    load_drug_synonyms_data,
    load_products_data,
    load_pathways_data,
)
from data_processing.data_frames import (
    create_data_frame_basic_info,
    create_data_frame_synonyms,
    create_data_frame_products,
    create_data_frame_pathways,
)
from visualisations.graphs import generate_synonyms_graph, plot_synonyms_graph

if __name__ == "__main__":

    file_path = "drugbank_partial.xml"
    drug_id = "DB00006"

    drugs_data = load_basic_drug_data(file_path)

    drug_df = create_data_frame_basic_info(drugs_data)

    synonyms_data = load_drug_synonyms_data(file_path)

    synonyms_df = create_data_frame_synonyms(synonyms_data)

    G = generate_synonyms_graph(drug_id, synonyms_df)

    # plot_synonyms_graph(G, drug_id)

    products_data = load_products_data(file_path)

    products_df = create_data_frame_products(products_data)

    pathways_data = load_pathways_data(file_path)

    pathways_df = create_data_frame_pathways(pathways_data)

    print(pathways_df)
