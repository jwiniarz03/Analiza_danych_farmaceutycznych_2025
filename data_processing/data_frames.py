import pandas as pd
from data_processing.data_loader import DataLoader
from src.targets import Target, Polypeptide


def create_data_frame_basic_info(drugs_data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from the drug data dictionary.

    Args:
        drugs_data (dict): Dictionary with drug id as keys and drug information as values.

    Returns:
        pd.DataFrame: DataFrame with drug data.
    """

    df = (
        pd.DataFrame.from_dict(drugs_data, orient="index")
        .reset_index()
        .rename(columns={"index": "id"})
    )

    return df


def create_data_frame_synonyms(synonyms_data: list[dict[str:str]]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from the synonyms data dictionary.

    Args:
        synonyms_data (dict): Dictionary with id as keys and a single string of synonyms separated by newlines as values.

    Returns:
        pd.DataFrame: DataFrame with drug id and a single string of all synonyms.
    """

    df = pd.DataFrame.from_dict(
        synonyms_data, orient="index", columns=["synonyms"]
    ).reset_index()
    df.rename(columns={"index": "drug_id"}, inplace=True)

    return df


def create_data_frame_products(products_data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from the products data dictionary.

    Args:
        products_data (list[dict[str:str]]): List of products containing specified drug.

    Returns:
        pd.DataFrame: DataFrame with products data.
    """

    df = pd.DataFrame(products_data)

    return df


def create_data_frame_pathways(pathways_data: dict) -> pd.DataFrame:
    """ """
    df = pd.DataFrame(pathways_data)

    count = df.count()

    p_count = f"Całkowita liczba szkalów wynosi {count}"

    return df[["Pathway", "Category"]], p_count


def create_data_frame_path_drug(path_drug_data):

    df = pd.DataFrame(path_drug_data)

    return df[["Pathway", "Drug Name"]]


class UniversalDataFrame:

    def __init__(self, xml_file: str):
        self.data_loader = DataLoader(xml_file)
        self.targets = self.data_loader.parse_targets()

    def create_targets_interactions_dataframe(self) -> pd.DataFrame:
        """Creates a DataFrame with targets interaction information."""
        data = {
            "DrugBank ID": [],
            "Source": [],
            "External ID": [],
            "Polypeptide name": [],
            "Gene name": [],
            "GenAtlas ID": [],
            "Chromosome number": [],
            "Cellular location": [],
        }

        for target in self.targets:
            polypeptide = target.polypeptide
            data["DrugBank ID"].append(target.id)
            data["Source"].append(polypeptide.source)
            data["External ID"].append(polypeptide.id)
            data["Polypeptide name"].append(polypeptide.name)
            data["Gene name"].append(polypeptide.gene_name)
            data["GenAtlas ID"].append(polypeptide.genatlas_id)
            data["Chromosome number"].append(polypeptide.chromosome_location)
            data["Cellular location"].append(polypeptide.cellular_location)

        return pd.DataFrame(data)
