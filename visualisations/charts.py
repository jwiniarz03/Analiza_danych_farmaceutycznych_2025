import matplotlib.pyplot as plt
import pandas as pd
from analysis.molecular_analysis import compute_average_weights, get_weights
from typing import List
import seaborn as sns
from src.targets import Target


def plot_pathways_vertical_histogram(df: pd.DataFrame, path_to_save: str = None):
    """
    Creates a vertical histogram for data from a given DataFrame.

    Args:
        df (pd.DataFrame): DataFrame with drug_id and its number of pathways.
        path_to_save (str, optional): Path to save the generated plot. If None, the plot is displayed.
    """

    if df.empty:
        raise ValueError("Given DataFrame is empty. No data to plot.")

    plt.figure(figsize=(18, 8))
    plt.bar(df["DrugBank_ID"], df["Nr_of_pathways"], color="pink")
    plt.xlabel("DrugBank ID", fontsize=12, fontweight="bold")
    plt.ylabel("Number of Pathways", fontsize=12, fontweight="bold")
    plt.title("Number of Pathways for each Drug", fontsize=14, fontweight="bold")
    plt.xticks(rotation=0, fontsize=8, fontweight="bold", ha="center")
    plt.xlim(-0.5, len(df["DrugBank_ID"]) - 0.5)
    plt.tight_layout()
    if path_to_save:
        plt.savefig(path_to_save)
    else:
        plt.show()


def plot_pathways_horizontal_histogram(df: pd.DataFrame, path_to_save: str = None):
    """
    Creates a horizontal histogram for data from a given DataFrame.

    Args:
        df (pd.DataFrame): DataFrame with drug_id and its number of pathways.
        path_to_save (str, optional): Path to save the generated plot. If None, the plot is displayed.
    """

    if df.empty:
        raise ValueError("Given DataFrame is empty. No data to plot.")

    plt.figure(figsize=(8, 8))
    plt.barh(df["DrugBank_ID"], df["Nr_of_pathways"], color="pink")
    plt.ylabel("DrugBank ID", fontsize=12, fontweight="bold")
    plt.xlabel("Number of Pathways", fontsize=12, fontweight="bold")
    plt.title("Number of Pathways for each Drug", fontsize=14, fontweight="bold")
    plt.yticks(fontsize=5, fontweight="bold")
    plt.ylim(-0.5, len(df["DrugBank_ID"]) - 0.5)
    plt.tight_layout()
    if path_to_save:
        plt.savefig(path_to_save)
    else:
        plt.show()


def create_pie_plot_targets(df: pd.DataFrame, path_to_save: str = None):
    """
    Creates a pie chart representing the distribution of cellular locations for targets.

    Args:
        df (pd.DataFrame): DataFrame containing target cellular locations and DrugBank IDs.
        path_to_save (str, optional): Path to save the generated plot. If None, the plot is displayed.
    """
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

    plt.figure(figsize=(14, 8))
    plt.pie(
        data,
        labels=[
            label if label in filtered_labels.values else "" for label in locations
        ],
        autopct=lambda p: f"{p:.1f}%" if p > 3 else "",
        startangle=90,
    )
    plt.title("Distribution of Cellular Locations", fontsize=12, fontweight="bold")
    plt.legend(
        locations,
        title="Cellular Locations",
        loc="upper left",
        fontsize="small",
        bbox_to_anchor=(1.0, 1.15),
        handlelength=2.0,
    )
    plt.tight_layout()
    if path_to_save:
        plt.savefig(path_to_save)
    else:
        plt.show()


def create_groups_pie_plot(
    df: pd.DataFrame, df_drugs: pd.DataFrame, path_to_save: str = None
):
    """
    Creates separate pie charts for each drug group, showing its proportion of the total unique drugs.

    Args:
        df (pd.DataFrame): DataFrame with drug groups and the count of drugs in each group.
        df_drugs (pd.DataFrame): DataFrame containing unique drugs.
        path_to_save (str, optional): Path to save the generated plot. If None, the plot is displayed.
    """

    total_unique_drugs = len(df_drugs)

    num_plots = len(df)
    ncols = 3
    nrows = (num_plots + ncols - 1) // ncols

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(5 * ncols, 4 * nrows))
    if num_plots == 1:
        axes = [axes]

    for ax, (group, count) in zip(axes.flat, zip(df["Groups"], df["Count"])):
        sizes = [count, total_unique_drugs - count]
        labels = [group, "others"]

        ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            textprops={"fontsize": 8},
            startangle=180,
        )
        ax.set_title(f"Proportion of {group} drugs", fontsize=10)

    for ax in axes.flat[num_plots:]:
        ax.axis("off")

    plt.tight_layout()
    if path_to_save:
        plt.savefig(path_to_save)
    else:
        plt.show()


def plot_average_weights(targets: List[Target], path_to_save: str = None):
    """
    Creates a bar chart showing the average molecular weight for each cellular location.

    Args:
        targets (List[Target]): List of target objects.
        path_to_save (str, optional): Path to save the generated plot. If None, the plot is displayed.
    """
    df = compute_average_weights(targets).sort_values(
        by="Average Molecular Weight", ascending=False
    )

    plt.figure(figsize=(12, 6))
    sns.barplot(
        x="Cellular Location", y="Average Molecular Weight", data=df, color="pink"
    )
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.yticks(fontsize=8)
    plt.xlabel("Cellular Location", fontsize=10, fontweight="bold")
    plt.ylabel("Average Molecular Weight", fontsize=10, fontweight="bold")
    plt.title(
        "Average Molecular Weight by Cellular Location", fontsize=16, fontweight="bold"
    )
    plt.tight_layout()
    if path_to_save:
        plt.savefig(path_to_save)
    else:
        plt.show()


def plot_distribution(targets: List[Target], path_to_save: str):
    df = get_weights(targets)

    plt.figure(figsize=(12, 6))
    sns.stripplot(
        x="Cellular Location",
        y="Molecular Weight",
        data=df,
        jitter=True,
        alpha=0.7,
        color="darkblue",
    )
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.yticks(fontsize=8)
    plt.title("Molecular Weight Distribution")
    plt.tight_layout()
    if path_to_save:
        plt.savefig(path_to_save)
    else:
        plt.show()
