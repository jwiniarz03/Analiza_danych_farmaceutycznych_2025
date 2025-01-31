import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from data_processing.data_frames import UniversalDataFrame

# Mock data for testing
MOCK_TARGETS = [
    MagicMock(
        id="T001",
        polypeptide=MagicMock(
            id="P001",
            source="GenSource",
            name="PolypeptideName",
            gene_name="Gene1",
            genatlas_id="G001",
            chromosome_location="1",
            cellular_location="Cytoplasm",
        ),
    )
]

MOCK_DRUGS = [
    MagicMock(
        drug_id="D001",
        name="Drug1",
        to_dict=lambda: {
            "DrugBank ID": "D001",
            "Name": "Drug1",
            "Type": "Type1",
            "Description": "Desc1",
            "Form": "Tablet",
            "Indications": "Ind1",
            "Mechanism_of_action": "MOA1",
            "Food_interactions": "None",
            "Groups": ["approved", "investigational"],
        },
        products=[
            MagicMock(
                name="Product1",
                producer="Producer1",
                ndc="12345",
                form="Tablet",
                application="Oral",
                dosage="10mg",
                country="USA",
                agency="FDA",
            )
        ],
        drug_interactions=[{"Drug2": "Interaction description"}],
        synonyms=["Synonym1", "Synonym2"],
        groups=["approved", "investigational"],
    )
]

MOCK_PATHWAYS = [
    MagicMock(
        to_dict=lambda: {"Pathway_ID": "P001", "Name": "Pathway1", "Drugs": ["D001"]},
        drugs=["D001"],
    )
]


@pytest.fixture
def mock_data_loader():
    with patch("data_processing.data_frames.DataLoader") as MockDataLoader:
        instance = MockDataLoader.return_value
        instance.parse_targets.return_value = MOCK_TARGETS
        instance.parse_drugs.return_value = MOCK_DRUGS
        instance.parse_pathways.return_value = MOCK_PATHWAYS
        yield instance


@pytest.mark.parametrize(
    "method, expected_columns",
    [
        (
            "create_targets_interactions_dataframe",
            [
                "DrugBank ID",
                "Source",
                "External ID",
                "Polypeptide name",
                "Gene name",
                "GenAtlas ID",
                "Chromosome number",
                "Cellular location",
            ],
        ),
        (
            "create_drugs_basic_informations_df",
            [
                "DrugBank ID",
                "Name",
                "Type",
                "Description",
                "Form",
                "Indications",
                "Mechanism_of_action",
                "Food_interactions",
            ],
        ),
        ("create_pathways_data_frame", ["Pathway_ID", "Name", "Drugs"]),
        ("create_synonyms_data_frame", ["DrugBank ID", "Synonyms"]),
        ("create_nr_of_pathways_data_frame", ["DrugBank_ID", "Nr_of_pathways"]),
        (
            "create_drug_interactions_data_frame",
            ["DrugBank ID", "Drug Name", "Target Name", "Interaction Description"],
        ),
    ],
)
def test_dataframe_creation(mock_data_loader, method, expected_columns):
    """Tests creation of DataFrames."""
    udf = UniversalDataFrame("dummy.xml")
    dataframe = getattr(udf, method)()

    assert isinstance(dataframe, pd.DataFrame), f"{method} did not return a DataFrame"
    assert (
        list(dataframe.columns) == expected_columns
    ), f"Unexpected columns for {method}"


@pytest.mark.parametrize(
    "method",
    [
        "create_targets_interactions_dataframe",
        "create_drugs_basic_informations_df",
        "create_pathways_data_frame",
        "create_synonyms_data_frame",
        "create_nr_of_pathways_data_frame",
        "create_drug_interactions_data_frame",
    ],
)
def test_dataframe_non_empty(mock_data_loader, method):
    """Tests if DataFrame is not empty."""
    udf = UniversalDataFrame("dummy.xml")
    dataframe = getattr(udf, method)()
    assert not dataframe.empty, f"{method} returned an empty DataFrame"


@pytest.mark.parametrize("expected_count", [1])
def test_approved_not_withdrawn_count(mock_data_loader, expected_count):
    """Tests counting approved not withdrawn drugs."""
    udf = UniversalDataFrame("dummy.xml")
    df = udf.create_groups_data_frame()
    assert (
        "approved" in df["Groups"].values
    ), "Missing 'approved' group in groups DataFrame"
