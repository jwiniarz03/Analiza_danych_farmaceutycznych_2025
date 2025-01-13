from data_processing.data_loader import load_basic_drug_data, load_drug_synonyms_data
from data_processing.data_frames import (
    create_data_frame_basic_info,
    create_data_frame_synonyms,
)

if __name__ == "__main__":

    file_path = "drugbank_partial.xml"

    # Load and parse data
    drugs_data = load_basic_drug_data(file_path)

    drug_df = create_data_frame_basic_info(drugs_data)

    synonyms_data = load_drug_synonyms_data(file_path)

    synonyms_df = create_data_frame_synonyms(synonyms_data)
