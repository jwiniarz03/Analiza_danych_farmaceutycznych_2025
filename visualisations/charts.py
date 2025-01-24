import matplotlib.pyplot as plt
import pandas as pd


def plot_pathways_histogram(df: pd.DataFrame):
    """
    Creates a histogram for data from a given DataFrame.

    Args:
        df (pd.DataFrame): DataFrame with drug_id and its number of pathways.
    """

    if df.empty:
        raise ValueError("Given DataFrame is empty. No data to plot.")

    plt.figure(figsize=(18, 8))
    plt.bar(df["Drug"], df["Nr_of_pathways"], color="green")
    plt.xlabel("Drug", fontsize=12, fontweight="bold")
    plt.ylabel("Number of Pathways", fontsize=12, fontweight="bold")
    plt.title("Number of Pathways for each Drug", fontsize=14, fontweight="bold")
    plt.xticks(rotation=90, fontsize=8, fontweight="bold", ha="center")
    plt.xlim(-0.5, len(df["Drug"]) - 0.5)
    plt.tight_layout()
    plt.show()


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
