import pytest
import xml.etree.ElementTree as ET
from unittest.mock import patch, MagicMock
from data_processing.data_loader import DataLoader
from src.drugs import Drug
from src.targets import Target, Polypeptide
from src.pathways import Pathway

MOCK_XML = """<drugbank xmlns="http://www.drugbank.ca">
    <drug type="small molecule">
        <drugbank-id primary="true">DB0001</drugbank-id>
        <name>DrugOne</name>
        <description>Test drug description</description>
        <state>solid</state>
        <indication>Used for testing</indication>
        <mechanism-of-action>Test mechanism</mechanism-of-action>
        <targets>
            <target>
                <id>T0001</id>
                <name>TargetOne</name>
                <polypeptide id="P0001" source="Swiss-Prot">
                    <name>ProteinOne</name>
                    <gene-name>GeneOne</gene-name>
                    <molecular-weight>50000.0</molecular-weight>
                    <chromosome-location>10</chromosome-location>
                    <cellular-location>cell membrane</cellular-location>
                </polypeptide>
            </target>
        </targets>
        <pathways>
            <pathway>
                <smpdb-id>SMP0001</smpdb-id>
                <name>PathwayOne</name>
                <category>Metabolic</category>
            </pathway>
        </pathways>
    </drug>
</drugbank>"""


@pytest.fixture
def mock_dataloader():
    with patch.object(DataLoader, "_load_data_from_file") as mock_load_data:
        root = ET.ElementTree(ET.fromstring(MOCK_XML)).getroot()
        ns = {"db": "http://www.drugbank.ca"}
        mock_load_data.return_value = (root, ns)
        yield DataLoader("mock.xml")


def test_parse_drugs_content(mock_dataloader):
    drugs = mock_dataloader.parse_drugs()
    assert len(drugs) == 1
    assert isinstance(drugs[0], Drug)
    assert drugs[0].name == "DrugOne"
    assert drugs[0].drug_id == "DB0001"
    assert drugs[0].description == "Test drug description"


def test_parse_targets_content(mock_dataloader):
    targets = mock_dataloader.parse_targets()
    print(len(targets) == 1)
    assert isinstance(targets[0], Target)
    assert targets[0].id == "T0001"
    assert targets[0].name == "TargetOne"
    print(targets[0].polypeptide)
    assert isinstance(targets[0].polypeptide, Polypeptide)
    assert targets[0].polypeptide.name == "ProteinOne"
    assert targets[0].polypeptide.molecular_weight == "50000.0"


def test_parse_pathways_content(mock_dataloader):
    pathways = mock_dataloader.parse_pathways()
    assert len(pathways) == 1
    assert isinstance(pathways[0], Pathway)
    assert pathways[0].id == "SMP0001"
    assert pathways[0].name == "PathwayOne"
    assert pathways[0].category == "Metabolic"


def test_empty_xml():
    empty_loader = DataLoader("empty.xml")
    with patch(
        "xml.etree.ElementTree.parse",
        return_value=ET.ElementTree(ET.Element("drugbank")),
    ):
        assert empty_loader.parse_drugs() == []
        assert empty_loader.parse_targets() == []
        assert empty_loader.parse_pathways() == []
