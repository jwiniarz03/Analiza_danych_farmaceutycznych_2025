import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from analysis.molecular_analysis import compute_average_weights, get_weights
from typing import List
from src.targets import Target


def plot_average_weights(targets: List[Target]):
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
    plt.show()


def plot_distribution(targets: List[Target]):
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
    plt.show()
