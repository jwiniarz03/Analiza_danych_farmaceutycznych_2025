from data_processing.data_loader import load_basic_drug_data
from data_processing.data_frames import create_data_frame_basic_info

if __name__ == "__main__":

    file_path = "drugbank_partial.xml"

    # Load and parse data
    drugs_data = load_basic_drug_data(file_path)

    drug_df = create_data_frame_basic_info(drugs_data)
