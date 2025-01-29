from typing import List, Set
from src.products import Product


class Drug:

    def __init__(
        self,
        name: str,
        drug_id: str,
        drug_type: str,
        description: str,
        state: str,
        indication: str,
        mechanism_of_action: str,
        drug_interactions: List[dict],
        food_interactions: List[str] = None,
        synonyms: List[str] = None,
        groups: List[str] = None,
        products: Set["Product"] = None,
    ):
        self.name = name
        self.drug_id = drug_id
        self.drug_type = drug_type
        self.description = description
        self.state = state
        self.indication = indication
        self.mechanism_of_action = mechanism_of_action
        self.drug_interactions = drug_interactions
        self.food_interactions = food_interactions if food_interactions else ["None"]
        self.synonyms = synonyms if synonyms else ["None"]
        self.groups = groups if groups else ["None"]
        self.products = products if products else set()

    def to_dict(self) -> dict:
        return {
            "DrugBank ID": self.drug_id,
            "Name": self.name,
            "Type": self.drug_type,
            "Description": self.description,
            "Form": self.state,
            "Indications": self.indication,
            "Mechanism_of_action": self.mechanism_of_action,
            "Food_interactions": self.food_interactions,
            "Drug interactions": self.drug_interactions,
            "Synonyms": self.synonyms,
            "Groups": self.groups,
            "Products": [product.to_dict() for product in self.products],
        }
