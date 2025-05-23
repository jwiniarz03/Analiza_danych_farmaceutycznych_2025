import xml.etree.ElementTree as ET
from typing import List
from src.targets import Target, Polypeptide
from src.drugs import Drug
from src.products import Product
from src.pathways import Pathway


class DataLoader:

    def __init__(self, xml_data: str):
        self.xml_data = xml_data

    def _load_data_from_file(self):
        tree = ET.parse(self.xml_data)
        root = tree.getroot()

        # Namespace handling for XML parsing
        ns = {"db": "http://www.drugbank.ca"}
        return root, ns

    def parse_targets(self) -> List[Target]:
        """Parse XML data and return a list of Target objects."""
        root, ns = self._load_data_from_file()

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
                    if resource == "GenAtlas":
                        genatlas_id = ext_id.find("db:identifier", ns).text

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
                    mollecular_weight=polypeptide_general.find(
                        "db:molecular-weight", ns
                    ).text,
                )

                new_Target = Target(id, name, polypeptide)
                targets.append(new_Target)

        return targets

    def parse_drugs(self) -> List[Drug]:
        """Parse XML data and return a list of Drug objects."""

        root, ns = self._load_data_from_file()

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
            food_interactions = [
                food.text
                for food in drug.findall("db:food-interactions/db:food-interaction", ns)
            ]

            for interaction in drug.findall(
                "db:drug-interactions/db:drug-interaction", ns
            ):
                drug_name = interaction.find("db:name", ns).text
                interaction_description = interaction.find("db:description", ns).text
                drug_interactions.append({drug_name: interaction_description})
            synonyms = [
                synonym.text for synonym in drug.findall("db:synonyms/db:synonym", ns)
            ]
            groups = [group.text for group in drug.findall("db:groups/db:group", ns)]

            products = set()
            for product in drug.findall("db:products/db:product", ns):
                product_name = product.find("db:name", ns).text
                producer = product.find("db:labeller", ns).text
                national_drug_code = product.find("db:ndc-product-code", ns).text
                form = product.find("db:dosage-form", ns).text
                method_of_application = product.find("db:route", ns).text
                dose_information = product.find("db:strength", ns).text
                country = product.find("db:country", ns).text
                agency = product.find("db:source", ns).text

                new_Product = Product(
                    product_name,
                    producer,
                    national_drug_code,
                    form,
                    method_of_application,
                    dose_information,
                    country,
                    agency,
                )
                products.add(new_Product)

            new_Drug = Drug(
                name,
                id,
                type,
                description,
                form,
                indication,
                mechanism_of_action,
                food_interactions=food_interactions,
                drug_interactions=drug_interactions,
                synonyms=synonyms,
                groups=groups,
                products=products,
            )

            drugs.append(new_Drug)

        return drugs

    def parse_pathways(self) -> List[Pathway]:
        """Parse XML Data and returns a list of Pathway objects."""
        root, ns = self._load_data_from_file()

        pathways = []
        drugs_list = []

        for drug in root.findall("db:drug", ns):
            for pathway in drug.findall("db:pathways/db:pathway", ns):
                pathway_id = pathway.find("db:smpdb-id", ns).text
                pathway_name = pathway.find("db:name", ns).text
                category = pathway.find("db:category", ns).text

                drugs_list = [
                    drug_elem.find("db:drugbank-id", ns).text
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
