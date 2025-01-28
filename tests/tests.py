import pytest
from unittest.mock import patch, mock_open, MagicMock
from data_processing.data_loader import (
    load_basic_drug_data,
    load_drug_synonyms_data,
    load_products_data,
    load_pathways_drugs_data,
    DataLoader,
)
from src.targets import Target, Polypeptide
from src.drugs import Drug
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.etree.ElementTree as ET


@pytest.fixture
def sample_xml_content():
    """
    Fixture providing a sample XML content string for testing.
    """
    root = Element(
        "{http://www.drugbank.ca}drugbank", version="5.1", exported_on="2024-03-14"
    )
    drug = SubElement(
        root,
        "{http://www.drugbank.ca}drug",
        type="biotech",
        created="2005-06-13",
        updated="2024-01-02",
    )

    drugbank_id = SubElement(
        drug, "{http://www.drugbank.ca}drugbank-id", primary="true"
    )
    drugbank_id.text = "DB00001"

    name = SubElement(drug, "{http://www.drugbank.ca}name")
    name.text = "SampleDrug"

    description = SubElement(drug, "{http://www.drugbank.ca}description")
    description.text = "Sample drug description."

    state = SubElement(drug, "{http://www.drugbank.ca}state")
    state.text = "solid"

    indication = SubElement(drug, "{http://www.drugbank.ca}indication")
    indication.text = "Used for testing."

    mechanism = SubElement(drug, "{http://www.drugbank.ca}mechanism-of-action")
    mechanism.text = "Inhibits some enzyme."

    target = SubElement(drug, "{http://www.drugbank.ca}targets")
    target_entry = SubElement(target, "target")
    target_id = SubElement(target_entry, "{http://www.drugbank.ca}id")
    target_id.text = "T001"
    target_name = SubElement(target_entry, "{http://www.drugbank.ca}name")
    target_name.text = "SampleTarget"

    polypeptide = SubElement(
        target_entry,
        "{http://www.drugbank.ca}polypeptide",
        id="P12345",
        source="GenBank",
    )
    poly_name = SubElement(polypeptide, "name")
    poly_name.text = "SamplePolypeptide"

    gene_name = SubElement(polypeptide, "{http://www.drugbank.ca}gene-name")
    gene_name.text = "GENE1"

    chromosome_location = SubElement(
        polypeptide, "{http://www.drugbank.ca}chromosome-location"
    )
    chromosome_location.text = "7q21"

    cellular_location = SubElement(
        polypeptide, "{http://www.drugbank.ca}cellular-location"
    )
    cellular_location.text = "cytoplasm"

    return tostring(root).decode()


@patch("builtins.open", new_callable=mock_open)
@patch("xml.etree.ElementTree.parse")
def test_parse_targets(mock_parse, mock_file, sample_xml_content):
    """
    Test parse_targets method of DataLoader class.
    """

    mock_file.return_value.read.return_value = sample_xml_content

    mock_tree = MagicMock()
    mock_root = ET.fromstring(sample_xml_content)
    mock_tree.getroot.return_value = mock_root
    mock_parse.return_value = mock_tree

    loader = DataLoader("dummy.xml")

    targets = loader.parse_targets()

    assert len(targets) == 1
    target = targets[0]
    assert isinstance(target, Target)
    assert target.id == "T001"
    assert target.name == "SampleTarget"
    assert target.polypeptide.name == "SamplePolypeptide"
    assert target.polypeptide.gene_name == "GENE1"
