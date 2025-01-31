from src.targets import Target
from typing import List
import pandas as pd
import numpy as np
from collections import defaultdict
from statistics import mean
from scipy.stats import f_oneway


def compute_average_weights(targets: List[Target]) -> pd.DataFrame:
    """
    Computes the average molecular weight and standard deviation for each cellular location
    based on the provided list of Target objects.

    Args:
        targets (List[Target]): A list of Target objects that contain Polypeptide objects
                                 with molecular weight and cellular location data.

    Returns:
        pd.DataFrame: A DataFrame containing the average molecular weight and standard deviation
                      for each cellular location.
    """
    weight_dict = defaultdict(list)

    for target in targets:
        polypeptide = target.polypeptide
        if polypeptide.cellular_location and polypeptide.molecular_weight:
            try:
                weight = float(polypeptide.molecular_weight)
                weight_dict[polypeptide.cellular_location].append(weight)
            except ValueError:
                continue

    avg_weights = {
        location: {
            "Average Molecular Weight": mean(weights),
            "Standard Deviation": np.std(weights),
        }
        for location, weights in weight_dict.items()
    }

    df = pd.DataFrame.from_dict(avg_weights, orient="index").reset_index()
    df.rename(columns={"index": "Cellular Location"}, inplace=True)

    return df


def get_weights(targets: List[Target]) -> pd.DataFrame:
    """
    Extracts the molecular weight and cellular location for each target, returning
    a DataFrame.

    Args:
        targets (List[Target]): A list of Target objects containing Polypeptide objects
                                 with molecular weight and cellular location data.

    Returns:
        pd.DataFrame: A DataFrame with two columns: "Cellular Location" and "Molecular Weight".
    """
    list = []

    for target in targets:
        polypeptide = target.polypeptide
        if polypeptide.cellular_location and polypeptide.molecular_weight:
            try:
                weight = float(polypeptide.molecular_weight)
                list.append((polypeptide.cellular_location, weight))
            except ValueError:
                continue

    return pd.DataFrame(list, columns=["Cellular Location", "Molecular Weight"])


def run_anova(targets: List[Target]):
    """
    Runs an ANOVA test to determine if there are significant differences in molecular weights
    between different cellular locations based on the provided list of Target objects.

    Args:
        targets (List[Target]): A list of Target objects containing Polypeptide objects
                                 with molecular weight and cellular location data.

    Prints:
        The F-statistic and p-value of the ANOVA test.
    """
    df = get_weights(targets)

    groups = [
        df[df["Cellular Location"] == loc]["Molecular Weight"].values
        for loc in df["Cellular Location"].unique()
    ]

    stat, p_value = f_oneway(*groups)

    print(f"ANOVA test: F-statistic = {stat:.3f}, p-value = {p_value:.3e}")

    if p_value < 0.05:
        print("Wniosek: Istnieje istotna statystycznie różnica między grupami!")
    else:
        print("Wniosek: Brak istotnych różnic między grupami.")
