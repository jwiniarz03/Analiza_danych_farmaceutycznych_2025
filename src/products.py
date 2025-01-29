class Product:

    def __init__(
        self,
        name: str,
        producer: str,
        ndc: str,
        form: str,
        application: str,
        dosage: str,
        country: str,
        agency: str,
    ):
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
            "Product name": self.name,
            "Producer": self.producer,
            "National Drug Code": self.ndc,
            "Form": self.form,
            "Method of application": self.application,
            "Dose information": self.dosage,
            "Country": self.country,
            "Agency": self.agency,
        }

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return (
            self.name == other.name
            and self.producer == other.producer
            and self.ndc == other.ndc
            and self.form == other.form
            and self.application == other.application
            and self.dosage == other.dosage
            and self.country == other.country
            and self.agency == other.agency
        )

    def __hash__(self):
        return hash(
            (
                self.name,
                self.producer,
                self.ndc,
                self.form,
                self.application,
                self.dosage,
                self.country,
                self.agency,
            )
        )
