class Product:

    def __init__(
        self,
        id: str,
        name: str,
        producer: str,
        ndc: str,
        form: str,
        application: str,
        dosage: str,
        country: str,
        agency: str,
    ):
        self.id = id
        self.name = name
        self.producer = producer
        self.ndc = ndc
        self.form = form
        self.application = application
        self.dosage = dosage
        self.country = country
        self.agency = agency

    def to_dict(self) -> dict:
        return {
            "Drug ID": self.id,
            "Product name": self.name,
            "Producer": self.producer,
            "National Drug Code": self.ndc,
            "Form": self.form,
            "Method of application": self.application,
            "Dose information": self.dosage,
            "Country": self.country,
            "Agency": self.agency,
        }
