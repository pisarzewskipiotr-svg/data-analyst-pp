# Analiza ABC/XYZ zapasów magazynowych - Excel

Projekt analityczny łączący doświadczenie praktyczne pracy na magazynie (obsługa wózków widłowych) z umiejętnościami analizy danych. Cały model zbudowany jest w Excelu na syntetycznych, ale realistycznych danych sprzedażowych (500 SKU, 24 miesiące historii).

## Cel projektu

Zaprojektowanie i wdrożenie klasycznego modelu segmentacji zapasów (ABC/XYZ) wraz z wyliczeniem konkretnych parametrów operacyjnych (Safety Stock, Reorder Point, EOQ) — czyli dokładnie tego typu analizy, jaką wykonuje Supply Chain Analyst / Inventory Specialist w realnym magazynie.

## Dane

Dane zostały wygenerowane syntetycznie (Python, `numpy`/`pandas`) w sposób odwzorowujący realistyczne wzorce z magazynu:

- **500 unikalnych SKU** w 15 kategoriach produktowych
- **24 miesiące** historii sprzedaży (sierpień 2024 – lipiec 2026)
- Rozkład wartości sprzedaży zaprojektowany tak, by odpowiadał klasycznemu efektowi Pareto (rozkład log-normalny popytu bazowego)
- Trzy wzorce popytu przypisane losowo do produktów: **stabilny**, **sezonowy** i **nieregularny** (z okresowym zerowym popytem — tzw. *lumpy demand*), aby analiza XYZ miała sens demonstracyjny

## Struktura pliku (zakładki)

| Zakładka | Zawartość |
|---|---|
| **Data** | Surowe dane źródłowe (SKU, kategoria, data, ilość wydana, wartość jednostkowa) — 12 000 wierszy |
| **Pivot ABC (źródło)** | Tabela przestawna: suma wartości sprzedaży per SKU za cały okres |
| **ABC Analysis** | Klasyfikacja ABC (% udziału, % skumulowany, klasa A/B/C) + wykres Pareto |
| **Pivot XYZ (źródło)** | Tabela przestawna: ilość wydana per SKU per miesiąc (24 kolumny) |
| **XYZ Analysis** | Średnia, odchylenie standardowe, współczynnik zmienności (CV), klasyfikacja X/Y/Z |
| **Matrix ABC-XYZ** | Połączona macierz obu klasyfikacji, polityka zapasów, Lead Time, Safety Stock, Reorder Point, EOQ |

## Metodologia

### Klasyfikacja ABC (wartość sprzedaży)
Produkty posortowane malejąco wg wartości sprzedaży (ilość × cena), z podziałem na klasy na podstawie % skumulowanego:
- **A** — do 80% skumulowanej wartości
- **B** — 80–95%
- **C** — 95–100%

**Wynik:** A = 20.4% SKU (55.6 mln zł), B = 24.2% SKU (10.5 mln zł), C = 55.4% SKU (3.5 mln zł) — klasyczny rozkład Pareto.

### Klasyfikacja XYZ (zmienność popytu)
Na podstawie współczynnika zmienności (CV = odchylenie std. / średnia) liczonego z 24 miesięcy popytu:
- **X** — CV ≤ 0.5 (popyt stabilny)
- **Y** — 0.5 < CV ≤ 1.0 (popyt sezonowy/zmienny)
- **Z** — CV > 1.0 (popyt nieregularny, trudny do prognozowania)

**Wynik:** X = 40.0%, Y = 41.8%, Z = 18.2%.

### Macierz ABC/XYZ i polityka zapasów
Połączenie obu klasyfikacji (9 kombinacji: AX–CZ) z przypisaną polityką zapasów i poziomem obsługi (service level) — od 99% dla AX (wysoka wartość, stabilny popyt) do 85% dla CZ (niska wartość, nieregularny popyt, rekomendacja zamawiania na żądanie).

### Parametry operacyjne
Dla każdego SKU wyliczono:
- **Safety Stock** = Z-score(poziom obsługi) × dzienne odchylenie std. popytu × √(Lead Time)
- **Reorder Point** = średni dzienny popyt × Lead Time + Safety Stock
- **EOQ (Economic Order Quantity)** = √(2 × roczny popyt × koszt zamówienia / (% koszt utrzymania × wartość jednostkowa))

**Uproszczenia przyjęte świadomie:** koszt zamówienia (80 zł) i koszt utrzymania zapasu (22% rocznie) przyjęto jako stałe dla wszystkich SKU, dla uproszczenia modelu — w realnym wdrożeniu byłyby zróżnicowane np. wg kategorii produktowej lub dostawcy.

## Kluczowe wnioski biznesowe

- **20.4% SKU generuje ~80% wartości sprzedaży** — te produkty (klasa A) wymagają priorytetowego rozmieszczenia najbliżej strefy wysyłki i wysokiego poziomu obsługi.
- **55.4% asortymentu (klasa C) to zaledwie 5% wartości** — dla tych produktów uzasadnione jest ograniczenie kontroli zapasów i rzadsze, większe zamówienia.
- **Kombinacja AZ (wysoka wartość + nieregularny popyt)** to najtrudniejsza i najdroższa kategoria do zarządzania — wymaga wysokiego zapasu bezpieczeństwa mimo wysokiego kosztu utrzymania.
- Macierz ABC/XYZ pozwala różnicować politykę zapasów w sposób znacznie bardziej precyzyjny niż sama klasyfikacja ABC.

## Technologie

- Python (generowanie danych syntetycznych: `numpy`, `pandas`)
- Microsoft Excel (tabele przestawne, formuły tablicowe, XLOOKUP, funkcje statystyczne: `NORM.S.INV`, `STDEV.P`, warunkowe formatowanie, wykresy)

## Reprodukcja danych

Dane w pliku `dane_sprzedazy_sku.csv` zostały wygenerowane skryptem `generate_data.py`. 
Aby wygenerować dane na nowo (z tym samym seedem = identyczny wynik):

```bash
pip install pandas numpy python-dateutil
python generate_data.py
```

## Kontekst

Projekt powstał jako część budowy portfolio łączącego praktyczne doświadczenie magazynowe (uprawnienia na wózki widłowe, praca operacyjna) z wykształceniem w zakresie programowania i analizy danych — pod kątem stanowisk typu Supply Chain Analyst, Logistics Data Analyst, WMS/Inventory Specialist.
