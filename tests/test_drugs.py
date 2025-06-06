import pytest
from src.drugs import Drug
from src.products import Product


def test_drug_initialization():
    """Test initialization of Drug class."""

    product = Product(
        name="Product A",
        producer="Producer A",
        ndc="NDC001",
        form="Tablet",
        application="Oral",
        dosage="500mg",
        country="USA",
        agency="FDA",
    )

    drug = Drug(
        name="Drug A",
        drug_id="DB0001",
        drug_type="type A",
        description="Description A",
        state="Solid",
        indication="Indication A",
        mechanism_of_action="Mechanism A",
        drug_interactions=[{"Drug B": "Interaction B"}],
        food_interactions=["Sample food interactions."],
        synonyms=["Synonym 1", "Synonym 2"],
        groups=["Group 1", "Group2"],
        products=set([product]),
    )

    assert drug.name == "Drug A"
    assert drug.drug_id == "DB0001"
    assert drug.drug_type == "type A"
    assert drug.description == "Description A"
    assert drug.state == "Solid"
    assert drug.indication == "Indication A"
    assert drug.mechanism_of_action == "Mechanism A"
    assert drug.drug_interactions == [{"Drug B": "Interaction B"}]
    assert drug.food_interactions == ["Sample food interactions."]
    assert drug.synonyms == ["Synonym 1", "Synonym 2"]
    assert drug.groups == ["Group 1", "Group2"]
    assert len(drug.products) == 1
    assert product in drug.products


@pytest.mark.parametrize(
    "food_interactions,synonyms,groups,expected_food,expected_synonyms,expected_groups",
    [
        (None, None, None, ["None"], ["None"], ["None"]),
        (["Food1"], ["Drug2"], ["Group1"], ["Food1"], ["Drug2"], ["Group1"]),
    ],
)
def test_drug_optional_fields(
    food_interactions,
    synonyms,
    groups,
    expected_food,
    expected_synonyms,
    expected_groups,
):
    """Test the handling of optional fields in the Drug class, ensuring None values are replaced properly."""
    drug = Drug(
        name="Drug A",
        drug_id="DB9999",
        drug_type="type A",
        description="Description A",
        state="Solid",
        indication="Indication A",
        mechanism_of_action="Mechanism A",
        drug_interactions=[],
        food_interactions=food_interactions,
        synonyms=synonyms,
        groups=groups,
    )

    assert drug.food_interactions == expected_food
    assert drug.synonyms == expected_synonyms
    assert drug.groups == expected_groups


def test_drug_to_dict():
    """Test the conversion of a Drug object to a dictionary representation."""

    product = Product(
        name="Product A",
        producer="Producer A",
        ndc="NDC001",
        form="Tablet",
        application="Oral",
        dosage="500mg",
        country="USA",
        agency="FDA",
    )

    drug = Drug(
        name="Drug A",
        drug_id="DB0001",
        drug_type="type A",
        description="Description A",
        state="Solid",
        indication="Indication A",
        mechanism_of_action="Mechanism A",
        drug_interactions=[{"Drug B": "Interaction B"}],
        food_interactions=["Sample food interactions."],
        synonyms=["Synonym 1", "Synonym 2"],
        groups=["Group 1", "Group2"],
        products=set([product]),
    )
    drug_dict = drug.to_dict()

    assert drug_dict["DrugBank ID"] == "DB0001"
    assert drug_dict["Name"] == "Drug A"
    assert drug_dict["Type"] == "type A"
    assert drug_dict["Description"] == "Description A"
    assert drug_dict["Form"] == "Solid"
    assert drug_dict["Indications"] == "Indication A"
    assert drug_dict["Mechanism_of_action"] == "Mechanism A"
    assert drug_dict["Food_interactions"] == ["Sample food interactions."]
    assert drug_dict["Drug interactions"] == [{"Drug B": "Interaction B"}]
    assert drug_dict["Synonyms"] == ["Synonym 1", "Synonym 2"]
    assert drug_dict["Groups"] == ["Group 1", "Group2"]
    assert len(drug_dict["Products"]) == 1
    assert drug_dict["Products"][0]["Product name"] == "Product A"
