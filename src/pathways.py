from typing import List


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
        """
        Converts the Pathway object to a dictionary representation.

        Returns:
            dict: A dictionary containing the pathway's attributes and their values.
        """
        return {
            "Pathway_ID": self.id,
            "Name": self.name,
            "Category": self.category,
            "Drugs": self.drugs,
            "Enzymes": self.enzymes,
        }
