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
    ):
        self.id = id
        self.source = source
        self.name = name
        self.gene_name = gene_name
        self.genatlas_id = genatlas_id
        self.chromosome_location = chromosome_location
        self.cellular_location = cellular_location

    def to_dict(self) -> dict:
        return {
            "Polypeptide ID": self.id,
            "Source": self.source,
            "Name": self.name,
            "Gene name": self.gene_name,
            "GenAtlas ID": self.genatlas_id,
            "Chromosome number": self.chromosome_location,
            "Celular location": self.cellular_location,
        }


class Target:

    def __init__(self, id: str, name: str, polypeptide: Polypeptide):
        self.id = id
        self.name = name
        self.polypeptide = polypeptide

    def to_dict(self) -> dict:
        return {
            "Target DrugBank ID": self.id,
            "Target Name": self.name,
            "Polypeptide": self.polypeptide.to_dict(),
        }
