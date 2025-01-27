import xml.etree.ElementTree as ET
from typing import List
from src.targets import Target, Polypeptide
from src.drugs import Drug
from src.products import Product
from src.pathways import Pathway


def load_basic_drug_data(xml_file: str) -> dict[str : dict[str:str]]:
    """
    Load the DrugBank partial XML file and parse its data for basic informations.

    Args:
        xml_file (str): Path to the DrugBank XML file.

    Returns:
        dict: Dictionary with drug id as keys and drug information as values.
    """

    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Namespace handling for XML parsing
    namespaces = {"db": "http://www.drugbank.ca"}

    basic_drugs_data = {}
    for drug in root.findall("db:drug", namespaces):
        id = drug.find("db:drugbank-id[@primary='true']", namespaces).text
        food_interactions = "\n".join(
            [
                food.text
                for food in drug.findall(
                    "db:food-interactions/db:food-interaction", namespaces
                )
            ]
        )
        if not food_interactions:
            food_interactions = "None"
        basic_drug_info = {
            "name": drug.find("db:name", namespaces).text,
            "type": drug.get("type"),
            "description": drug.find("db:description", namespaces).text,
            "form": drug.find("db:state", namespaces).text,
            "indications": drug.find("db:indication", namespaces).text,
            "mechanism_of_action": drug.find("db:mechanism-of-action", namespaces).text,
            "food_interactions": food_interactions,
        }
        basic_drugs_data[id] = basic_drug_info

    return basic_drugs_data


def load_drug_synonyms_data(xml_file: str) -> dict[str:str]:
    """
    Load the DrugBank partial XML file and parse its data for synonyms informations.

    Args:
        xml_file (str): Path to the DrugBank XML file.

    Returns:
        dict: Dictionary with drug id as keys and a single string of synonyms separated by newlines as values.
    """

    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Namespace handling for XML parsing
    namespaces = {"db": "http://www.drugbank.ca"}

    synonyms_drugs_data = {}
    for drug in root.findall("db:drug", namespaces):
        id = drug.find("db:drugbank-id[@primary='true']", namespaces).text
        synonyms = "\n".join(
            synonym.text
            for synonym in drug.findall("db:synonyms/db:synonym", namespaces)
        )

        synonyms_drugs_data[id] = synonyms

    return synonyms_drugs_data


def load_products_data(xml_file) -> list[dict[str:str]]:
    """
    Load the DrugBank partial xml file and parse its data for informations about products.

    Args:
        xml_file (str): Path to the DrugBank XML file.

    Returns:
        list of dicts: List of products containing specified drug.
    """

    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Namespace handling for XML parsing
    ns = {"db": "http://www.drugbank.ca"}

    basic_products_data = []

    for drug in root.findall("db:drug", ns):
        id = drug.find("db:drugbank-id[@primary='true']", ns).text
        for product in drug.findall("db:products/db:product", ns):
            product_data = {
                "Drug ID": id,
                "Product name": (product.find("db:name", ns).text),
                "Producer": (product.find("db:labeller", ns).text),
                "National Drug Code": (product.find("db:ndc-product-code", ns).text),
                "Form": (product.find("db:dosage-form", ns).text),
                "Method of application": (product.find("db:route", ns).text),
                "Dose information": (product.find("db:strength", ns).text),
                "Country": (product.find("db:country", ns).text),
                "Agency": (product.find("db:source", ns).text),
            }
        basic_products_data.append(product_data)

    return basic_products_data


def load_pathways_drugs_data(xml_file) -> list[dict[str:str]]:

    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Namespace handling for XML parsing
    ns = {"db": "http://www.drugbank.ca"}

    drugs_data = []

    for drug in root.findall("db:drug", ns):
        for pathway in drug.findall("db:pathways/db:pathway", ns):
            pathway_name = pathway.find("db:name", ns).text
            category = pathway.find("db:category", ns).text
            drugs_list = []
            for drug in pathway.findall("db:drugs/db:drug", ns):
                drug_name = drug.find("db:name", ns).text
                drugs_list.append(drug_name)
            drugs = ", ".join(drugs_list)
            pathway_data = {
                "Pathway": pathway_name,
                "Category": category,
                "Drug Name": drugs,
            }
            drugs_data.append(pathway_data)

    return drugs_data


class DataLoader:

    def __init__(self, xml_data: str):
        self.xml_data = xml_data

    def parse_targets(self) -> List[Target]:
        """Parse XML data and return a list of Target objects."""
        tree = ET.parse(self.xml_data)
        root = tree.getroot()

        # Namespace handling for XML parsing
        ns = {"db": "http://www.drugbank.ca"}

        targets = []

        for drug in root.findall("db:drug", ns):
            for target in drug.findall("db:targets/db:target", ns):
                id = target.find("db:id", ns).text
                name = target.find("db:name", ns).text
                polypeptide_general = target.find("db:polypeptide", ns)

                if polypeptide_general is None:
                    continue

                genatlas_id = None

                for ext_id in polypeptide_general.findall(
                    "db:external-identifiers/db:external-identifier", ns
                ):
                    resource = ext_id.find("db:resource", ns).text
                    identifier = ext_id.find("db:identifier", ns).text
                    if resource == "GenAtlas":
                        genatlas_id = identifier

                polypeptide = Polypeptide(
                    id=polypeptide_general.attrib["id"],
                    source=polypeptide_general.attrib["source"],
                    name=polypeptide_general.find("db:name", ns).text,
                    gene_name=polypeptide_general.find("db:gene-name", ns).text,
                    genatlas_id=genatlas_id,
                    chromosome_location=polypeptide_general.find(
                        "db:chromosome-location", ns
                    ).text,
                    cellular_location=polypeptide_general.find(
                        "db:cellular-location", ns
                    ).text,
                )

                new_Target = Target(id, name, polypeptide)
                targets.append(new_Target)

        return targets

    def parse_drugs(self) -> List[Drug]:
        """Parse XML data and return a list of Drug objects."""

        tree = ET.parse(self.xml_data)
        root = tree.getroot()

        # Namespace handling for XML parsing
        ns = {"db": "http://www.drugbank.ca"}

        drugs = []
        drug_interactions = []

        for drug in root.findall("db:drug", ns):
            id = drug.find("db:drugbank-id[@primary='true']", ns).text
            name = drug.find("db:name", ns).text
            type = drug.get("type")
            description = drug.find("db:description", ns).text
            form = drug.find("db:state", ns).text
            indication = drug.find("db:indication", ns).text
            mechanism_of_action = drug.find("db:mechanism-of-action", ns).text
            food_interactions = (
                "\n".join(
                    [
                        food.text
                        for food in drug.findall(
                            "db:food-interactions/db:food-interaction", ns
                        )
                    ]
                )
                if drug.find("db:food-interactions", ns) is not None
                else "None"
            )
            for interaction in drug.findall(
                "db:drug-interactions/db:drug-interaction", ns
            ):
                target_name = interaction.find("db:name", ns).text
                interaction_description = interaction.find("db:description", ns).text
                drug_interactions.append({target_name: interaction_description})
            synonyms = [
                synonym.text for synonym in drug.findall("db:synonyms/db:synonym", ns)
            ]
            groups = [group.text for group in drug.findall("db:groups/db:group", ns)]

            new_Drug = Drug(
                name,
                id,
                type,
                description,
                form,
                indication,
                mechanism_of_action,
                food_interactions,
                drug_interactions=drug_interactions,
                synonyms=synonyms,
                groups=groups,
            )
            drugs.append(new_Drug)

        return drugs

    def parse_products(self) -> List[Product]:
        """Parse XML Data and return a list of Product objects."""

        tree = ET.parse(self.xml_data)
        root = tree.getroot()

        # Namespace handling for XML parsing
        ns = {"db": "http://www.drugbank.ca"}

        products = []

        for drug in root.findall("db:drug", ns):
            id = drug.find("db:drugbank-id[@primary='true']", ns).text
            for product in drug.findall("db:products/db:product", ns):
                name = product.find("db:name", ns).text
                producer = product.find("db:labeller", ns).text
                national_drug_code = product.find("db:ndc-product-code", ns).text
                form = product.find("db:route", ns).text  # check
                method_of_application = product.find("db:dosage-form", ns).text
                dose_information = product.find("db:strength", ns).text
                country = product.find("db:country", ns).text
                agency = product.find("db:source", ns).text

            new_Product = Product(
                id,
                name,
                producer,
                national_drug_code,
                form,
                method_of_application,
                dose_information,
                country,
                agency,
            )

            products.append(new_Product)

        return products

    def parse_pathways(self) -> List[Pathway]:
        """Parse XML Data and returns a list of Pathway objects."""
        tree = ET.parse(self.xml_data)
        root = tree.getroot()

        # Namespace handling for XML parsing
        ns = {"db": "http://www.drugbank.ca"}

        pathways = []

        for drug in root.findall("db:drug", ns):
            for pathway in drug.findall("db:pathways/db:pathway", ns):
                pathway_id = pathway.find("db:smpdb-id", ns).text
                pathway_name = pathway.find("db:name", ns).text
                category = pathway.find("db:category", ns).text

                drugs_list = [
                    drug_elem.find("db:name", ns).text
                    for drug_elem in pathway.findall("db:drugs/db:drug", ns)
                ]

                enzymes_list = [
                    enzyme_elem.text
                    for enzyme_elem in pathway.findall("db:enzymes/db:uniprot-id", ns)
                ]

                new_Pathway = Pathway(
                    id=pathway_id,
                    name=pathway_name,
                    category=category,
                    drugs=drugs_list,
                    enzymes=enzymes_list,
                )
                pathways.append(new_Pathway)

        return pathways
