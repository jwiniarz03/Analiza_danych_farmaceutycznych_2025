import pytest
from src.products import Product


def test_product_initialization():
    """Test initialization of Product class."""
    product = Product(
        name="Product A",
        producer="Producer A",
        ndc="12345-678",
        form="Tablet",
        application="Oral",
        dosage="10 mg",
        country="US",
        agency="FDA",
    )

    assert product.name == "Product A"
    assert product.producer == "Producer A"
    assert product.ndc == "12345-678"
    assert product.form == "Tablet"
    assert product.application == "Oral"
    assert product.dosage == "10 mg"
    assert product.country == "US"
    assert product.agency == "FDA"


@pytest.mark.parametrize(
    "product_1,product_2,expected_result",
    [
        (
            Product(
                name="Product A",
                producer="Producer A",
                ndc="12345-678",
                form="Tablet",
                application="Oral",
                dosage="10 mg",
                country="US",
                agency="FDA",
            ),
            Product(
                name="Product A",
                producer="Producer A",
                ndc="12345-678",
                form="Tablet",
                application="Oral",
                dosage="10 mg",
                country="US",
                agency="FDA",
            ),
            True,
        ),
        (
            Product(
                name="Product A",
                producer="Producer A",
                ndc="12345-678",
                form="Tablet",
                application="Oral",
                dosage="10 mg",
                country="US",
                agency="FDA",
            ),
            Product(
                name="Product B",
                producer="Producer B",
                ndc="12345-679",
                form="Capsule",
                application="Topical",
                dosage="20 mg",
                country="Canada",
                agency="EMA",
            ),
            False,
        ),
    ],
)
def test_product_equality(product_1, product_2, expected_result):
    """Test equality (__eq__) of Product objects."""
    assert (product_1 == product_2) == expected_result


def test_product_to_dict():
    """Test the conversion of Product object to a dictionary."""
    product = Product(
        name="Product A",
        producer="Producer A",
        ndc="12345-678",
        form="Tablet",
        application="Oral",
        dosage="10 mg",
        country="US",
        agency="FDA",
    )
    product_dict = product.to_dict()

    assert product_dict["Product name"] == "Product A"
    assert product_dict["Producer"] == "Producer A"
    assert product_dict["National Drug Code"] == "12345-678"
    assert product_dict["Form"] == "Tablet"
    assert product_dict["Method of application"] == "Oral"
    assert product_dict["Dose information"] == "10 mg"
    assert product_dict["Country"] == "US"
    assert product_dict["Agency"] == "FDA"


def test_product_hash():
    """Test the hashing of Product objects (__hash__)."""
    product_1 = Product(
        name="Product A",
        producer="Producer A",
        ndc="12345-678",
        form="Tablet",
        application="Oral",
        dosage="10 mg",
        country="US",
        agency="FDA",
    )
    product_2 = Product(
        name="Product A",
        producer="Producer A",
        ndc="12345-678",
        form="Tablet",
        application="Oral",
        dosage="10 mg",
        country="US",
        agency="FDA",
    )

    assert hash(product_1) == hash(product_2)


@pytest.mark.parametrize(
    "product_1,product_2,expected_result",
    [
        (
            Product(
                name="Product A",
                producer="Producer A",
                ndc="12345-678",
                form="Tablet",
                application="Oral",
                dosage="10 mg",
                country="US",
                agency="FDA",
            ),
            Product(
                name="Product A",
                producer="Producer A",
                ndc="12345-678",
                form="Tablet",
                application="Oral",
                dosage="10 mg",
                country="US",
                agency="FDA",
            ),
            True,
        ),
        (
            Product(
                name="Product A",
                producer="Producer A",
                ndc="12345-678",
                form="Tablet",
                application="Oral",
                dosage="10 mg",
                country="US",
                agency="FDA",
            ),
            Product(
                name="Product B",
                producer="Producer B",
                ndc="12345-679",
                form="Capsule",
                application="Topical",
                dosage="20 mg",
                country="Canada",
                agency="EMA",
            ),
            False,
        ),
    ],
)
def test_product_equality(product_1, product_2, expected_result):
    """Test equality (__eq__) of Product objects."""
    assert (product_1 == product_2) == expected_result
