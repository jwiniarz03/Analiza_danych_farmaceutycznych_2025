from data_processing.data_frames import UniversalDataFrame
from typing import List
from src.drugs import Drug


def show_nr_of_pathways(pathways_df: UniversalDataFrame):
    """
    Displays the total number of pathways present in the provided DataFrame.

    Args:
        pathways_df (UniversalDataFrame): A DataFrame containing pathway data.

    Prints:
        The total number of pathways as a message to the console.
    """
    count = len(pathways_df)

    p_count = f"Całkowita liczba szkalów wynosi {count}."

    print(p_count)


def show_nr_of_approved_not_withdrawn_drugs(drugs: Drug):
    """
    Displays the number of drugs that are approved but not withdrawn.

    Args:
        drugs (List[Drug]): A list of Drug objects.

    Prints:
        The number of approved and not withdrawn drugs as a message to the console.
    """
    approved_not_withdrawn_count = 0
    for drug in drugs:
        if "approved" in drug.groups:
            if "withdrawn" not in drug.groups:
                approved_not_withdrawn_count += 1

    g_count = (
        f"Zatwierdzonych i nie wycofanych leków jest {approved_not_withdrawn_count}."
    )

    print(g_count)
