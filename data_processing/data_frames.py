import pandas as pd
from data_processing.data_loader import DataLoader


class UniversalDataFrame:

    def __init__(self, xml_file: str):
        self.data_loader = DataLoader(xml_file)
        self.targets = self.data_loader.parse_targets()
        self.drugs = self.data_loader.parse_drugs()
        self.pathways = self.data_loader.parse_pathways()

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

    def create_drugs_basic_informations_df(self) -> pd.DataFrame:
        """Creates a DataFrame with drugs basic information."""

        drug_dicts = [drug.to_dict() for drug in self.drugs]
        selected_columns = [
            "DrugBank ID",
            "Name",
            "Type",
            "Description",
            "Form",
            "Indications",
            "Mechanism_of_action",
            "Food_interactions",
        ]
        basic_df = pd.DataFrame(drug_dicts)
        df = basic_df[selected_columns]

        return df

    # def create_products_data_frame(self) -> pd.DataFrame:
    #     """Creates a DataFrame with products information."""

    #     products_dicts = [product.to_dict() for product in self.products]
    #     df = pd.DataFrame(products_dicts)

    #     return df

    def create_products_data_frame(self, drugs: list) -> pd.DataFrame:
        """Creates a DataFrame with products information."""

        products_data = []

        for drug in drugs:
            for product in drug.products:
                products_data.append(
                    {
                        "DrugBank ID": drug.drug_id,
                        "Product Name": product.name,
                        "Producer": product.producer,
                        "National Drug Code": product.ndc,
                        "Form": product.form,
                        "Method of application": product.application,
                        "Dose information": product.dosage,
                        "Country": product.country,
                        "Agency": product.agency,
                    }
                )

        df = pd.DataFrame(products_data)
        return df

    def create_pathways_data_frame(self) -> pd.DataFrame:
        """Creates a DataFrame with pathways information."""

        pathways_dicts = [pathway.to_dict() for pathway in self.pathways]
        df = pd.DataFrame(pathways_dicts)

        count = len(df)

        p_count = f"Całkowita liczba szkalów wynosi {count}."

        return df

    def create_synonyms_data_frame(self) -> pd.DataFrame:
        """Creates a DataFrame containing DrugBank ID as primary key and its synonyms."""

        data = [
            {
                "DrugBank ID": drug.drug_id,
                "Synonyms": ", ".join(drug.synonyms) if drug.synonyms else "None",
            }
            for drug in self.drugs
        ]

        df = pd.DataFrame(data)

        return df

    # only for drugs in shorter xml_file
    def create_nr_of_pathways_data_frame(self) -> pd.DataFrame:
        """Creates a DataFrame containing each DrugBank ID(from shorter database) and its number of interactive pathways."""

        count = {drug.drug_id: 0 for drug in self.drugs}
        for pathway in self.pathways:
            for drug in pathway.drugs:
                if drug in count:
                    count[drug] += 1

        df = pd.DataFrame(
            {
                "DrugBank_ID": list(count.keys()),
                "Nr_of_pathways": list(count.values()),
            }
        )

        return df

    def create_all_pathways_nr_data_frame(self, df: pd.DataFrame) -> pd.DataFrame:
        """Creates a DataFrame containing each DrugBank ID and its number of interactive pathways."""

        drug_counts = df["Drugs"].value_counts().reset_index()
        drug_counts.columns = ["DrugBank_ID", "Nr_of_pathways"]

        return drug_counts

    def create_groups_data_frame(self) -> pd.DataFrame:
        """Creates a DataFrame containing number of drugs in each drug group eg. investigational, approved."""

        drug_dicts = [drug.to_dict() for drug in self.drugs]
        df_exploded = pd.DataFrame(drug_dicts).explode("Groups")
        df = df_exploded.groupby("Groups").size().reset_index(name="Count")

        approved_not_withdrawn_count = 0
        for drug in self.drugs:
            if "approved" in drug.groups:
                if "withdrawn" not in drug.groups:
                    approved_not_withdrawn_count += 1

        g_count = f"Zatwierdzonych i nie wycofanych leków jest {approved_not_withdrawn_count}."
        # todo gdzie to wyswietlic
        return df

    def create_drug_interactions_data_frame(self) -> pd.DataFrame:
        """Creates a DataFrame with drug names and their drug interactions: drug names and description."""

        data = {
            "DrugBank ID": [],
            "Drug Name": [],
            "Target Name": [],
            "Interaction Description": [],
        }

        for drug in self.drugs:
            for interaction in drug.drug_interactions:
                for target_name, description in interaction.items():
                    data["DrugBank ID"].append(drug.drug_id)
                    data["Drug Name"].append(drug.name)
                    data["Target Name"].append(target_name)
                    data["Interaction Description"].append(description)

        df = pd.DataFrame(data)

        return df

    def create_pathway_interactions_data_frame(self) -> pd.DataFrame:
        """Creates a DataFrame with pathways ids and names with drugs they interact with."""

        pathways_dict = [pathway.to_dict() for pathway in self.pathways]
        dataframe = pd.DataFrame(pathways_dict)
        selected_columns = ["Pathway_ID", "Name", "Drugs"]
        df = dataframe[selected_columns].explode("Drugs").reset_index(drop=True)

        return df
