import pytest
from unittest import mock
from data_processing.data_loader import DataLoader
from src.targets import Target, Polypeptide
import xml.etree.ElementTree as ET

# Mock XML data for testing
mock_xml_data = """
<drug xmlns="http://www.drugbank.ca">
    <targets>
        <target>
            <id>BE0000048</id>
            <name>Prothrombin</name>
            <polypeptide id="P00734" source="Swiss-Prot">
                <name>Prothrombin</name>
                <gene-name>F2</gene-name>
                <chromosome-location>11</chromosome-location>
                <cellular-location>Secreted</cellular-location>
                <external-identifiers>
                    <external-identifier>
                        <resource>GenAtlas</resource>
                        <identifier>AT12345</identifier>
                    </external-identifier>
                </external-identifiers>
            </polypeptide>
        </target>
    </targets>
</drug>
"""

mock_invalid_xml_data = """
<drug xmlns="http://www.drugbank.ca">
    <targets>
        <target>
            <id>BE0000048</id>
            <name>Prothrombin</name>
            <polypeptide></polypeptide>
        </target>
    </targets>
</drug>
"""


@pytest.fixture
def data_loader():
    # Mock the open function to return the mock XML data
    with mock.patch("builtins.open", mock.mock_open(read_data=mock_xml_data)):
        return DataLoader("mocked_file.xml")


@pytest.fixture
def invalid_data_loader():
    # Mock the open function to return the invalid XML data
    with mock.patch("builtins.open", mock.mock_open(read_data=mock_invalid_xml_data)):
        return DataLoader("mocked_invalid_file.xml")


def test_parse_targets_success(data_loader):
    # Mock the ET.parse method to return a pre-parsed XML structure from the mock data
    with mock.patch.object(
        ET, "parse", return_value=ET.ElementTree(ET.fromstring(mock_xml_data))
    ):
        targets = data_loader.parse_targets()

    # Print the parsed targets to debug
    print(f"Parsed targets: {targets}")

    # Assertions to check that the data has been parsed correctly
    assert len(targets) == 1  # Should find 1 target in the XML
    target = targets[0]
    assert target.id == "BE0000048"
    assert target.name == "Prothrombin"
    assert target.polypeptide.id == "P00734"
    assert target.polypeptide.gene_name == "F2"
    assert target.polypeptide.chromosome_location == "11"
    assert target.polypeptide.cellular_location == "Secreted"
    assert target.polypeptide.genatlas_id == "AT12345"


def test_parse_targets_missing_polypeptide(invalid_data_loader):
    # Mock the ET.parse method to return a pre-parsed XML structure from the invalid data
    with mock.patch.object(
        ET, "parse", return_value=ET.ElementTree(ET.fromstring(mock_invalid_xml_data))
    ):
        targets = invalid_data_loader.parse_targets()

    # Assertions to check that no target is created due to missing polypeptide data
    assert len(targets) == 0  # No target should be parsed due to missing polypeptide


def test_parse_targets_no_target_in_xml():
    # XML with no targets
    mock_no_target_xml_data = """
    <drug xmlns="http://www.drugbank.ca">
        <targets></targets>
    </drug>
    """

    with mock.patch("builtins.open", mock.mock_open(read_data=mock_no_target_xml_data)):
        data_loader = DataLoader("mocked_no_target_file.xml")
        with mock.patch.object(
            ET,
            "parse",
            return_value=ET.ElementTree(ET.fromstring(mock_no_target_xml_data)),
        ):
            targets = data_loader.parse_targets()

    # Assertions to check that no targets are parsed
    assert len(targets) == 0


def test_parse_targets_invalid_xml():
    # Test case when the XML is malformed or invalid
    with mock.patch("builtins.open", mock.mock_open(read_data="<invalid>")):
        data_loader = DataLoader("mocked_invalid_file.xml")
        with mock.patch.object(
            ET, "parse", side_effect=ET.ParseError("XML parsing error")
        ):
            with pytest.raises(ET.ParseError):
                data_loader.parse_targets()
