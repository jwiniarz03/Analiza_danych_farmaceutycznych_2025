from data_processing.data_frames import UniversalDataFrame
from typing import List
from src.drugs import Drug


def show_nr_of_pathways(pathways_df: UniversalDataFrame):
    count = len(pathways_df)

    p_count = f"Całkowita liczba szkalów wynosi {count}."

    print(p_count)


def show_nr_of_approved_not_withdrawn_drugs(drugs: Drug):
    approved_not_withdrawn_count = 0
    for drug in drugs:
        if "approved" in drug.groups:
            if "withdrawn" not in drug.groups:
                approved_not_withdrawn_count += 1

    g_count = (
        f"Zatwierdzonych i nie wycofanych leków jest {approved_not_withdrawn_count}."
    )

    print(g_count)
