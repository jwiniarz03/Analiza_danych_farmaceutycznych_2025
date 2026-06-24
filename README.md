# DrugBank Data Analyzer

Kompleksowe narzędzie analityczne zbudowane w języku Python do przetwarzania, statystycznej eksploracji i wizualizacji danych farmaceutycznych z bazy DrugBank. Projekt łączy inżynierię danych (ETL plików XML) z zaawansowaną analizą grafową oraz statystyczną.


## Architektura i technologie
Projekt wykorzystuje podejście obiektowe (OOP), dzieląc odpowiedzialność na odseparowane moduły:
- src/: Definicje głównych klas mapujących domenę (Drug, Pathway, Product, Target, Polypeptide).
- data_processing/: Logika odpowiedzialna za ładowanie, parsowanie struktury XML i budowanie obiektów DataFrame.
- analysis/ & visualisations/: Autorskie moduły realizujące testy statystyczne (m.in. ANOVA) oraz generowanie wykresów.
- Technologie: Python 3, Pandas, NetworkX, Matplotlib/Plotly, Pytest.


## Kluczowe funkcjonalności
- Data Wrangling & ETL: Ekstrakcja i strukturyzacja danych ze złożonych plików XML do zoptymalizowanych ramek danych (obejmujących informacje o lekach, białkach docelowych, produktach farmaceutycznych i szlakach metabolicznych).
- Analiza Sieciowa (Graph Analysis): Wykorzystanie biblioteki NetworkX do modelowania i wizualizacji złożonych relacji – w tym grafów dwudzielnych interakcji leków ze szlakami sygnałowymi oraz mapowania synonimów.
- Analiza Statystyczna: Autorska analiza molekularna obejmująca obliczanie średnich mas cząsteczkowych, badanie ich rozkładu oraz przeprowadzanie analizy wariancji (ANOVA) dla zgromadzonych celów białkowych (targets).
- Modułowe Wizualizacje: Automatyczne generowanie czytelnych raportów wizualnych w formacie .png (histogramy, wykresy kołowe, grafy zależności).


## Uruchomienie lokalne
### Główny pipeline analityczny
Aby przetworzyć dane i wygenerować statystyki w postaci plików .json oraz wykresów .png, uruchom główny skrypt z terminala:
```bash
    python main.py --path "sciezka/do/drugbank_partial.xml" --drug_id DB00047 --gene_id C1QA
```
- --path: Ścieżka do pliku XML z bazą danych.
- --drug_id: Identyfikator leku do wygenerowania grafu synonimów.
- --gene_id: Identyfikator genu do analizy zależności i wygenerowania interaktywnego grafu.

### Testowanie
Logika aplikacji jest pokryta testami jednostkowymi. Aby upewnić się, że środowisko i parsery danych działają poprawnie, uruchom:
```bash
    pytest tests/
```
