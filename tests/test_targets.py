import pytest
from src.targets import Polypeptide, Target


def test_polypeptide_initialization():
    """Test initialization of Polypeptide class."""
    polypeptide = Polypeptide(
        id="P001",
        source="Source A",
        name="Polypeptide A",
        gene_name="Gene A",
        genatlas_id="GA001",
        chromosome_location="Chromosome A",
        cellular_location="Nucleus",
    )

    assert polypeptide.id == "P001"
    assert polypeptide.source == "Source A"
    assert polypeptide.name == "Polypeptide A"
    assert polypeptide.gene_name == "Gene A"
    assert polypeptide.genatlas_id == "GA001"
    assert polypeptide.chromosome_location == "Chromosome A"
    assert polypeptide.cellular_location == "Nucleus"


def test_polypeptide_to_dict():
    """Test the conversion of Polypeptide object to a dictionary."""
    polypeptide = Polypeptide(
        id="P001",
        source="Source A",
        name="Polypeptide A",
        gene_name="Gene A",
        genatlas_id="GA001",
        chromosome_location="Chromosome A",
        cellular_location="Nucleus",
    )
    polypeptide_dict = polypeptide.to_dict()

    assert polypeptide_dict["Polypeptide ID"] == "P001"
    assert polypeptide_dict["Source"] == "Source A"
    assert polypeptide_dict["Name"] == "Polypeptide A"
    assert polypeptide_dict["Gene name"] == "Gene A"
    assert polypeptide_dict["GenAtlas ID"] == "GA001"
    assert polypeptide_dict["Chromosome number"] == "Chromosome A"
    assert polypeptide_dict["Celular location"] == "Nucleus"


def test_target_initialization():
    """Test initialization of Target class."""
    polypeptide = Polypeptide(
        id="P001",
        source="Source A",
        name="Polypeptide A",
        gene_name="Gene A",
        genatlas_id="GA001",
        chromosome_location="Chromosome A",
        cellular_location="Nucleus",
    )
    target = Target(id="T001", name="Target A", polypeptide=polypeptide)

    assert target.id == "T001"
    assert target.name == "Target A"
    assert target.polypeptide == polypeptide


def test_target_to_dict():
    """Test the conversion of Target object to a dictionary."""
    polypeptide = Polypeptide(
        id="P001",
        source="Source A",
        name="Polypeptide A",
        gene_name="Gene A",
        genatlas_id="GA001",
        chromosome_location="Chromosome A",
        cellular_location="Nucleus",
    )
    target = Target(id="T001", name="Target A", polypeptide=polypeptide)
    target_dict = target.to_dict()

    assert target_dict["Target DrugBank ID"] == "T001"
    assert target_dict["Target Name"] == "Target A"
    assert target_dict["Polypeptide"]["Polypeptide ID"] == "P001"
    assert target_dict["Polypeptide"]["Source"] == "Source A"
    assert target_dict["Polypeptide"]["Name"] == "Polypeptide A"
    assert target_dict["Polypeptide"]["Gene name"] == "Gene A"
    assert target_dict["Polypeptide"]["GenAtlas ID"] == "GA001"
    assert target_dict["Polypeptide"]["Chromosome number"] == "Chromosome A"
    assert target_dict["Polypeptide"]["Celular location"] == "Nucleus"
