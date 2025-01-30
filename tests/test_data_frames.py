import pytest
from unittest.mock import MagicMock
from data_processing.data_loader import DataLoader
from data_processing.data_frames import UniversalDataFrame
import pandas as pd
import tempfile
import xml.etree.ElementTree as ET


def read_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root.find("name").text  # Pobieramy zawartość tagu <name>


@pytest.fixture
def mock_data_loader():
    """Fixture do mockowania klasy DataLoader."""
    mock_loader = MagicMock(spec=DataLoader)
    return mock_loader


@pytest.fixture
def mock_universal_dataframe(mock_data_loader):
    """Fixture do inicjowania obiektu UniversalDataFrame z mockowanym DataLoader."""
    mock_data_loader.parse_targets.return_value = []  # Zwracamy pustą listę dla testów
    mock_data_loader.parse_drugs.return_value = []  # Podobnie dla leków
    mock_data_loader.parse_pathways.return_value = []  # I dla ścieżek
    return UniversalDataFrame("mock_file.xml")


def test_create_targets_interactions_dataframe(mock_universal_dataframe):
    """Test dla create_targets_interactions_dataframe."""
    mock_universal_dataframe.targets = [
        MagicMock(
            id="T123",
            polypeptide=MagicMock(
                source="Source A",
                id="P123",
                name="Polypeptide A",
                gene_name="Gene A",
                genatlas_id="GA123",
                chromosome_location="X",
                cellular_location="Cytoplasm",
            ),
        )
    ]

    xml_content = """<?xml version="1.0"?>
    <data>
        <name>Test Name</name>
    </data>"""

    with tempfile.NamedTemporaryFile(
        mode="w+", suffix=".xml", delete=False
    ) as temp_file:
        temp_file.write(xml_content)
        temp_file.seek(0)  # Resetujemy wskaźnik pliku

        # Testujemy funkcję na rzeczywistym pliku XML
        result = read_xml(temp_file.name)
        assert result == "Test Name"

    df = mock_universal_dataframe.create_targets_interactions_dataframe()

    assert df.shape == (1, 8), f"Expected shape (1, 8), got {df.shape}"
    assert df["DrugBank ID"].iloc[0] == "T123"
    assert df["Source"].iloc[0] == "Source A"
    assert df["Polypeptide name"].iloc[0] == "Polypeptide A"


def test_create_drugs_basic_informations_df(mock_universal_dataframe):
    """Test dla create_drugs_basic_informations_df."""
    # mock_drug = MagicMock(
    #     to_dict=MagicMock(
    #         return_value={
    #             "DrugBank ID": "D123",
    #             "Name": "Drug A",
    #             "Type": "Small molecule",
    #             "Description": "Test drug",
    #             "Form": "Tablet",
    #             "Indications": "Indication A",
    #             "Mechanism_of_action": "Action A",
    #             "Food_interactions": "None",
    #         }
    #     )
    # )
    # mock_universal_dataframe.drugs = [mock_drug]

    # df = mock_universal_dataframe.create_drugs_basic_informations_df()

    # print(df.shape)
    # print(df["DrugBank ID"].iloc[0])

    # assert df.shape == (1, 8), f"Expected shape (1, 8), got {df.shape}"
    # assert df["DrugBank ID"].iloc[0] == "D123"
    # assert df["Name"].iloc[0] == "Drug A"
    # assert df["Food_interactions"].iloc[0] == "None"


@pytest.mark.parametrize(
    "products, expected_columns",
    [
        (
            [
                MagicMock(
                    name="Product A",
                    producer="Producer A",
                    ndc="NDC123",
                    form="Tablet",
                    application="Oral",
                    dosage="10mg",
                    country="USA",
                    agency="FDA",
                )
            ],
            [
                "DrugBank ID",
                "Product Name",
                "Producer",
                "National Drug Code",
                "Form",
                "Method of application",
                "Dose information",
                "Country",
                "Agency",
            ],
        )
    ],
)
def test_create_products_data_frame(
    mock_universal_dataframe, products, expected_columns
):
    """Test dla create_products_data_frame z parametryzacją."""
    mock_drug = MagicMock(drug_id="D123", products=products)
    mock_universal_dataframe.drugs = [mock_drug]

    df = mock_universal_dataframe.create_products_data_frame(
        mock_universal_dataframe.drugs
    )

    assert all(
        col in df.columns for col in expected_columns
    ), f"Expected columns {expected_columns}, got {df.columns}"
    assert df["DrugBank ID"].iloc[0] == "D123"
    assert df["Product Name"].iloc[0] == "Product A"


def test_create_pathways_data_frame(mock_universal_dataframe):
    """Test dla create_pathways_data_frame."""
    mock_pathway = MagicMock(
        to_dict=MagicMock(
            return_value={"Pathway_ID": "P123", "Name": "Pathway A", "Drugs": ["D123"]}
        )
    )
    mock_universal_dataframe.pathways = [mock_pathway]

    df = mock_universal_dataframe.create_pathways_data_frame()

    assert df.shape == (1, 2), f"Expected shape (1, 2), got {df.shape}"
    assert df["Pathway_ID"].iloc[0] == "P123"
    assert df["Name"].iloc[0] == "Pathway A"
    assert df["Drugs"].iloc[0] == "D123"


@pytest.mark.parametrize("drugs, expected_count", [(["D123", "D124", "D125"], 3)])
def test_create_nr_of_pathways_data_frame(
    mock_universal_dataframe, drugs, expected_count
):
    """Test dla create_nr_of_pathways_data_frame z parametryzacją."""
    mock_universal_dataframe.pathways = [MagicMock(drugs=drugs)]

    df = mock_universal_dataframe.create_nr_of_pathways_data_frame()

    assert len(df) == expected_count, f"Expected {expected_count} rows, got {len(df)}"
    assert all(drug in df["DrugBank_ID"].values for drug in drugs)
