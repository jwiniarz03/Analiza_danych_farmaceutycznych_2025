from src.targets import Target
from typing import List
import pandas as pd
import numpy as np
from collections import defaultdict
from statistics import mean


def compute_average_weights(targets: List[Target]) -> pd.DataFrame:
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
        location: (mean(weights), np.std(weights) if weights else None)
        for location, weights in weight_dict.items()
    }

    return pd.DataFrame(
        list(avg_weights.items()),
        columns=["Cellular Location", "Average Molecular Weight", "Standard Deviation"],
    )
