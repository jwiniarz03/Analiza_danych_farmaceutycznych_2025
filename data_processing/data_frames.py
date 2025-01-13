import pandas as pd


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


def create_data_frame_find_synonyms(synonyms_data: dict) -> pd.DataFrame:
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
