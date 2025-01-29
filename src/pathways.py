from typing import List
from src.drugs import Drug


class Pathway:

    def __init__(
        self,
        id: str,
        name: str,
        category: str,
        drugs: List[str] = None,
        enzymes: List[str] = None,
    ):
        self.id = id
        self.name = name
        self.category = category
        self.drugs = drugs if drugs else ["None"]
        self.enzymes = enzymes if enzymes else ["None"]

    def to_dict(self) -> dict:
        return {
            "Pathway_ID": self.id,
            "Name": self.name,
            "Category": self.category,
            "Drugs": self.drugs,
            "Enzymes": self.enzymes,
        }
