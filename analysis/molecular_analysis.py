from data_processing.data_loader import DataLoader
import pandas as pd
from collections import defaultdict
from statistics import mean


class MolecularWeightAnalysis:
    def __init__(self, xml_file: str):
        self.data_loader = DataLoader(xml_file)
        self.targets = self.data_loader.parse_targets()

    def compute_average_weights(self) -> pd.DataFrame:
        weight_dict = defaultdict(list)

        for target in self.targets:
            polypeptide = target.polypeptide
            if polypeptide.cellular_location and polypeptide.molecular_weight:
                try:
                    weight = float(polypeptide.molecular_weight)
                    weight_dict[polypeptide.cellular_location].append(weight)
                except ValueError:
                    continue

        avg_weights = {
            location: mean(weights) if weights else None
            for location, weights in weight_dict.items()
        }

        return pd.DataFrame(
            list(avg_weights.items()),
            columns=["Cellular Location", "Average Molecular Weight"],
        )


data_loader = DataLoader("path/to/drugbank.xml")  # Update with actual XML path
analysis = MolecularWeightAnalysis(data_loader)
df = analysis.compute_average_weights()
print(df)
