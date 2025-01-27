from data_processing.data_loader import (
    load_basic_drug_data,
    load_drug_synonyms_data,
    load_products_data,
    load_pathways_drugs_data,
    DataLoader,
)
from data_processing.data_frames import (
    create_data_frame_basic_info,
    create_data_frame_synonyms,
    create_data_frame_products,
    create_data_frame_pathways,
    create_data_frame_path_drug,
    UniversalDataFrame,
)
from visualisations.graphs import (
    generate_draw_synonyms_graph,
)

from visualisations.charts import plot_pathways_histogram, create_pie_plot_targets

if __name__ == "__main__":

    file_path = "drugbank_partial.xml"
    drug_id = "DB00003"

    synonyms_data = load_drug_synonyms_data(file_path)

    synonyms_df = create_data_frame_synonyms(synonyms_data)

    path_drug_data = load_pathways_drugs_data(file_path)

    pathways_df = create_data_frame_pathways(path_drug_data)

    path_drug_df = create_data_frame_path_drug(path_drug_data)

    data_loader = DataLoader(file_path)
    targets = data_loader.parse_targets()
    drugs = data_loader.parse_drugs()
    products = data_loader.parse_products()
    pathways = data_loader.parse_pathways()

    df_builder = UniversalDataFrame(file_path)
    protein_df = df_builder.create_targets_interactions_dataframe()
    df_drugs = df_builder.create_drugs_basic_informations_df()
    df_products = df_builder.create_products_data_frame()
    df_pathways = df_builder.create_pathways_data_frame()
    df_synonyms = df_builder.create_synonyms_data_frame()
    df_nr_pathways = df_builder.create_nr_of_pathways_data_frame()
    df_groups_number = df_builder.create_groups_data_frame()

    # pie = create_pie_plot_targets(protein_df) --> to do

    # nx_graph = generate_draw_synonyms_graph(drug_id, drugs) --> mayby ok

    # histogram = plot_pathways_histogram(df_nr_pathways) --> i think ok

    print(df_groups_number)
