# Projekt_Python

## DANE AUTORA:
* JULIA WINIARZ
* NR INDEKSU: 453877

## POLECENIE:
Celem projektu jest przeanalizowanie zawartości okrojonej wersji bazy leków: DrugBank i utworzeniu rónego rodzaju tabel i wykresów podsumowujących zawartość bazy leków.

## PODZIAŁ KODU
Projekt został podzielony na wiele plików, zawierających pojedyncze klasy, których metody mają w miarę
możliwości ograniczoną odpowiedzialność. Projekt zawiera 5 podkatalogów - src: pliki definiujące główne klasy: Drug, Pathway, Product, Target i Polypeptide, analysis: własna analiza statystyczna oraz inne prostsze analizy, data_processing: ładowanie, parsowanie danych i tworzenie DataFrame, tests: lokalizacja zawierająca pliki z testami klas.


## URUCHOMIENIE I TESTOWANIE PROJEKTU
### URUCHOMIENIE PROJEKTU
Program uruchamiamy z terminalu (znajdując się w folderze Projekt_Python) poprzez komendę 'main.py'.
Nalezy wówczas podać ściezkę do pliku xml we fladze --path (w tym przypadku jest to drugbank_partial.xml).
Następnie nalezy we fladze --drug_id podać DrugBank ID leku, dla którego chcemy wyrysować graf synonimów (np.DB00047)
oraz we fladze --gene_id podać id genu, dla którego chcemy wyrysować graf zalezności (np.C1QA).
Wyniki zapisywane są w oddzielnych plikach: - DataFrame w formacie .json, wykresy w .png.

### TESTOWANIE PROJEKTU
Wszelkie testy zapisane są w folderze 'tests'. By je uruchomić nalezy w terminalu wpisać komendę 'pytest tests/'.
