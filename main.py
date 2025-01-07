from data_processing.data_loader import load_basic_drug_data

if __name__ == "__main__":

    file_path = "drugbank_partial.xml"

    # Load and parse data
    drugs_data = load_basic_drug_data(file_path)
