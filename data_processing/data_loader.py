import xml.etree.ElementTree as ET


def load_basic_drug_data(xml_file: str) -> dict[str, dict[str, str]]:
    """
    Load the DrugBank partial XML file and parse its data.

    Args:
        xml_file (str): Path to the DrugBank XML file.

    Returns:
        dict of dicts: Dictionary with drug id as keys and drug information as values.
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
