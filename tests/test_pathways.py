import pytest
from src.pathways import Pathway


def test_pathway_initialization():
    """Test initialization of Pathway class."""
    pathway = Pathway(
        id="SMP00001",
        name="Pathway A",
        category="Category A",
        drugs=["Drug A", "Drug B"],
        enzymes=["Enzyme A"],
    )

    assert pathway.id == "SMP00001"
    assert pathway.name == "Pathway A"
    assert pathway.category == "Category A"
    assert pathway.drugs == ["Drug A", "Drug B"]
    assert pathway.enzymes == ["Enzyme A"]


@pytest.mark.parametrize(
    "drugs,enzymes,expected_drugs,expected_enzymes",
    [
        (None, None, ["None"], ["None"]),
        (["Drug A"], ["Enzyme B"], ["Drug A"], ["Enzyme B"]),
    ],
)
def test_pathway_optional_fields(drugs, enzymes, expected_drugs, expected_enzymes):
    """Test initialization of Pathway with optional fields and default values."""
    pathway = Pathway(
        id="PW002",
        name="Pathway B",
        category="Category B",
        drugs=drugs,
        enzymes=enzymes,
    )

    assert pathway.drugs == expected_drugs
    assert pathway.enzymes == expected_enzymes


def test_pathway_to_dict():
    """Test that the pathway object correctly converts to a dictionary."""
    pathway = Pathway(
        id="SMP00001",
        name="Pathway C",
        category="Category C",
        drugs=["Drug A", "Drug C"],
        enzymes=["Enzyme A", "Enzyme C"],
    )
    pathway_dict = pathway.to_dict()

    assert pathway_dict["Pathway_ID"] == "SMP00001"
    assert pathway_dict["Name"] == "Pathway C"
    assert pathway_dict["Category"] == "Category C"
    assert pathway_dict["Drugs"] == ["Drug A", "Drug C"]
    assert pathway_dict["Enzymes"] == ["Enzyme A", "Enzyme C"]
