from typing import List
from src.drugs import Drug


class Pathway:

    def __init__(self, id: str, name: str, category: str, drugs: List[Drug]):
        self.id = id
        self.name = name
        self.category = category
        self.drugs = drugs

    def to_dict(self) -> dict:
        return {
            "Path_ID": self.id,
            "Name": self.name,
            "Category": self.category,
            "Drugs": ", ".join([drug.name for drug in self.drugs]),
        }
