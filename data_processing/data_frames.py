import pandas as pd


def create_data_frame_basic_info(drugs_data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from thedrug data dictionary.

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
