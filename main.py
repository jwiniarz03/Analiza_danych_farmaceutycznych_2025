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
    create_pathways_bipartite_graph,
    create_gene_graph,
)

from visualisations.charts import (
    plot_pathways_histogram,
    create_pie_plot_targets,
    create_groups_pie_plot,
)

import argparse
import pandas as pd


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=True)
    parser.add_argument("--id", type=str, required=True)
    args = parser.parse_args()
    return args


def main():

    args = parse_arguments()
    file_path = args.path
    drug_id = args.id  # DB00047

    data_loader = DataLoader(file_path)
    targets = data_loader.parse_targets()
    drugs = data_loader.parse_drugs()
    # products = data_loader.parse_products()
    pathways = data_loader.parse_pathways()

    df_builder = UniversalDataFrame(file_path)
    protein_df = df_builder.create_targets_interactions_dataframe()
    df_drugs = df_builder.create_drugs_basic_informations_df()
    df_products = df_builder.create_products_data_frame(drugs)
    df_pathways = df_builder.create_pathways_data_frame()
    df_synonyms = df_builder.create_synonyms_data_frame()
    df_nr_pathways = df_builder.create_nr_of_pathways_data_frame()
    df_groups_number = df_builder.create_groups_data_frame()
    df_drug_interactions = df_builder.create_drug_interactions_data_frame()
    df_pathways_interactions = df_builder.create_pathway_interactions_data_frame()
    df_all_pathways_nr = df_builder.create_all_pathways_nr_data_frame(
        df_pathways_interactions
    )

    # pie = create_pie_plot_targets(protein_df)  # --> to do

    # generate_draw_synonyms_graph(drug_id, drugs)  # --> mayby ok

    # plot_pathways_histogram(df_nr_pathways)  # --> i think ok
    # plot_pathways_histogram(df_all_pathways_nr)

    # create_groups_pie_plot( df_groups_number, df_drugs)  #  --> can be better

    create_pathways_bipartite_graph(
        df_pathways_interactions
    )  # --> i think it cant be better xd

    # create_gene_graph("FCGR3B", drugs, targets)
    # pd.DataFrame.to_csv(df_synonyms, path_or_buf="data.csv")
    # pd.DataFrame.to_excel(df_synonyms, "data.xlsx")
    # pd.DataFrame.to_json(df_synonyms, path_or_buf="data.json", indent=4)

    # print(df_synonyms)


if __name__ == "__main__":
    main()
