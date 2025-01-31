class Polypeptide:

    def __init__(
        self,
        id: str,
        source: str,
        name: str,
        gene_name: str,
        genatlas_id: str,
        chromosome_location: str,
        cellular_location: str,
        mollecular_weight: str,
    ):
        self.id = id
        self.source = source
        self.name = name
        self.gene_name = gene_name
        self.genatlas_id = genatlas_id
        self.chromosome_location = chromosome_location
        self.cellular_location = cellular_location
        self.molecular_weight = mollecular_weight

    def to_dict(self) -> dict:
        """
        Converts the Polypeptide object to a dictionary representation.

        Returns:
            dict: A dictionary containing the polypeptide's attributes and their values.
        """
        return {
            "Polypeptide ID": self.id,
            "Source": self.source,
            "Name": self.name,
            "Gene name": self.gene_name,
            "GenAtlas ID": self.genatlas_id,
            "Chromosome number": self.chromosome_location,
            "Celular location": self.cellular_location,
            "Molecular weight": self.molecular_weight,
        }


class Target:

    def __init__(self, id: str, name: str, polypeptide: Polypeptide):
        self.id = id
        self.name = name
        self.polypeptide = polypeptide

    def to_dict(self) -> dict:
        """
        Converts the Target object to a dictionary representation.

        Returns:
            dict: A dictionary containing the target's attributes and their values.
        """
        return {
            "Target DrugBank ID": self.id,
            "Target Name": self.name,
            "Polypeptide": self.polypeptide.to_dict(),
        }
