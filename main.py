from data_processing.data_loader import (
    DataLoader,
)
from data_processing.data_frames import (
    UniversalDataFrame,
)
from visualisations.graphs import (
    generate_draw_synonyms_graph,
    create_pathways_bipartite_graph,
    create_gene_graph,
)

from visualisations.charts import (
    plot_pathways_vertical_histogram,
    plot_pathways_horizontal_histogram,
    create_pie_plot_targets,
    create_groups_pie_plot,
)

from analysis.averages_bar_plot import plot_average_weights, plot_distribution
from analysis.molecular_analysis import compute_average_weights, run_anova
from analysis.pathway_analysis import (
    show_nr_of_pathways,
    show_nr_of_approved_not_withdrawn_drugs,
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

    df_builder = UniversalDataFrame(file_path)

    # Number 1
    df_drugs = df_builder.create_drugs_basic_informations_df()

    # Number 2
    df_synonyms = df_builder.create_synonyms_data_frame()
    # generate_draw_synonyms_graph(drug_id, drugs)

    # Number 3
    df_products = df_builder.create_products_data_frame(drugs)

    # Number 4
    df_pathways = df_builder.create_pathways_data_frame()
    # show_nr_of_pathways(df_pathways)

    # Number 5
    df_pathways_interactions = df_builder.create_pathway_interactions_data_frame()
    # create_pathways_bipartite_graph(df_pathways_interactions)

    # Number 6
    df_nr_pathways = df_builder.create_nr_of_pathways_data_frame()
    df_all_pathways_nr = df_builder.create_all_pathways_nr_data_frame(
        df_pathways_interactions
    )
    # plot_pathways_horizontal_histogram(df_nr_pathways)
    # plot_pathways_vertical_histogram(df_all_pathways_nr)

    # Number 7
    protein_df = df_builder.create_targets_interactions_dataframe()

    # Number 8
    # create_pie_plot_targets(protein_df)

    # Number 9
    df_groups_number = df_builder.create_groups_data_frame()
    # show_nr_of_approved_not_withdrawn_drugs(drugs)
    # create_groups_pie_plot(df_groups_number, df_drugs)

    # Number 10
    df_drug_interactions = df_builder.create_drug_interactions_data_frame()

    # Number 11
    # create_gene_graph("FCGR3B", drugs, targets)

    # Number 12
    df_molecular_weight = compute_average_weights(targets)
    # plot_average_weights(targets)
    # plot_distribution(targets)
    # run_anova(targets)

    # print(df_drug_interactions)
    # pd.DataFrame.to_csv(df_synonyms, path_or_buf="data.csv")
    # pd.DataFrame.to_excel(df_synonyms, "data.xlsx")
    # pd.DataFrame.to_json(df_synonyms, path_or_buf="data.json", indent=4)


if __name__ == "__main__":
    main()
