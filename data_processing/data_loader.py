import xml.etree.ElementTree as ET


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
