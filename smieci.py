import xml.etree.ElementTree as ET


def test(xml):
    tree = ET.parse(xml)
    root = tree.getroot()

    # Namespace handling for XML parsing
    ns = {"db": "http://www.drugbank.ca"}

    gene_id = "FCGR3B"
    drugs = []

    for drug in root.findall("db:drug", ns):
        for target in drug.findall("db:targets/db:target/db:polypeptide", ns):
            if target.find("db:gene-name", ns).text == gene_id:
                drug_id = drug.find("db:drugbank-id[@primary='true']", ns).text
                products = []
                for product in drug.findall("db:products/db:product", ns):
                    name = product.find("db:name", ns).text
                    products.append(name)
                drugs.append({drug_id: products})

    return drugs


print(test("drugbank_partial.xml"))
