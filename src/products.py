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
        """
        Converts the Product object to a dictionary representation.

        Returns:
            dict: A dictionary containing the product's attributes and their values.
        """
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
        """
        Compares the current Product object with another one to check for equality.

        Args:
            other (Product): The other Product object to compare with.

        Returns:
            bool: True if the two Product objects have the same attribute values;
                  False otherwise.
        """
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
        """
        Computes a hash value for the Product object based on its attributes.

        Returns:
            int: The hash value for the Product object, which allows it to be used
                 in sets or as dictionary keys.
        """
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
