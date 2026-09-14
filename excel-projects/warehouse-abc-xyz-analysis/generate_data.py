"""
Generator syntetycznych danych sprzedaży/wydań magazynowych
------------------------------------------------------------
Tworzy ~500 SKU w wielu kategoriach, z danymi miesięcznymi za 24 miesiące.

Kolumny wynikowe:
  SKU, Nazwa produktu, Kategoria, Data, Ilość wydana, Wartość jednostkowa
"""

import random
import numpy as np
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

random.seed(42)
np.random.seed(42)

# ---------------------------------------------------------------------
# 1. Definicja kategorii i przykładowych nazw produktów w każdej z nich
# ---------------------------------------------------------------------
CATEGORIES = {
    "Elektronika": ["Słuchawki bezprzewodowe", "Powerbank 10000mAh", "Kabel USB-C", "Ładowarka sieciowa",
                    "Głośnik Bluetooth", "Kamera IP", "Router Wi-Fi", "Dysk SSD 1TB"],
    "AGD": ["Czajnik elektryczny", "Toster", "Mikser ręczny", "Robot kuchenny", "Odkurzacz pionowy",
            "Żelazko parowe", "Suszarka do włosów", "Blender kielichowy"],
    "RTV": ["Telewizor 43''", "Soundbar", "Odtwarzacz Blu-ray", "Antena DVB-T", "Projektor LED",
            "Radio kuchenne", "Kamera sportowa"],
    "Odzież": ["Koszulka bawełniana", "Bluza z kapturem", "Spodnie jeansowe", "Kurtka zimowa",
               "Sweter wełniany", "Koszula flanelowa", "Legginsy sportowe"],
    "Obuwie": ["Buty sportowe", "Sandały letnie", "Kozaki zimowe", "Trampki klasyczne",
               "Klapki basenowe", "Buty trekkingowe"],
    "Kosmetyki": ["Krem nawilżający", "Szampon do włosów", "Żel pod prysznic", "Perfumy 50ml",
                  "Balsam do ciała", "Dezodorant w kulce", "Maseczka do twarzy"],
    "Zabawki": ["Klocki konstrukcyjne", "Lalka interaktywna", "Samochodzik zdalnie sterowany",
                "Puzzle 1000 elementów", "Gra planszowa", "Pluszak duży"],
    "Artykuły biurowe": ["Długopis żelowy", "Zeszyt A5", "Segregator A4", "Papier do drukarki",
                         "Zszywacz biurowy", "Kalkulator naukowy", "Marker permanentny"],
    "Sport i rekreacja": ["Piłka do piłki nożnej", "Mata do jogi", "Hantle 5kg", "Rower stacjonarny",
                          "Rolki fitness", "Namiot turystyczny", "Plecak trekkingowy"],
    "Ogród": ["Sekator ogrodowy", "Wąż ogrodowy 20m", "Doniczka ceramiczna", "Kosiarka elektryczna",
              "Nawóz uniwersalny", "Grill węglowy", "Parasol ogrodowy"],
    "Motoryzacja": ["Olej silnikowy 5W40", "Wycieraczki samochodowe", "Żarówka LED H7",
                    "Płyn do spryskiwaczy", "Odświeżacz powietrza do auta", "Osłona przeciwsłoneczna"],
    "Spożywcze": ["Kawa mielona 500g", "Herbata czarna 100g", "Oliwa z oliwek 500ml",
                  "Makaron pszenny 500g", "Czekolada mleczna", "Płatki śniadaniowe"],
    "Meble": ["Krzesło biurowe", "Regał na książki", "Stolik kawowy", "Szafka nocna",
              "Fotel wypoczynkowy", "Biurko komputerowe"],
    "Oświetlenie": ["Żarówka LED E27", "Lampa biurkowa", "Taśma LED RGB", "Lampion ogrodowy",
                    "Żyrandol sufitowy"],
    "Narzędzia": ["Wiertarka udarowa", "Zestaw kluczy nasadowych", "Młotek stolarski",
                  "Poziomica 60cm", "Taśma miernicza", "Szlifierka kątowa"],
}

CATEGORY_LIST = list(CATEGORIES.keys())

# Bazowa cena jednostkowa (zł) dla każdej kategorii - żeby wartości były realistyczne
CATEGORY_PRICE_RANGE = {
    "Elektronika": (30, 400),
    "AGD": (50, 600),
    "RTV": (150, 2000),
    "Odzież": (20, 200),
    "Obuwie": (40, 350),
    "Kosmetyki": (8, 120),
    "Zabawki": (15, 250),
    "Artykuły biurowe": (2, 60),
    "Sport i rekreacja": (20, 500),
    "Ogród": (15, 600),
    "Motoryzacja": (10, 250),
    "Spożywcze": (3, 50),
    "Meble": (80, 1200),
    "Oświetlenie": (10, 300),
    "Narzędzia": (25, 700),
}

N_SKU = 500
N_MONTHS = 24
START_DATE = date(2024, 8, 1)  # 24 miesiące wstecz od ~sierpnia 2026

# ---------------------------------------------------------------------
# 2. Generowanie listy SKU
# ---------------------------------------------------------------------
VARIANTS = ["", " Mini", " Pro", " Plus", " Classic", " XL", " Eco", " Premium", " Compact", " Advanced"]

# Budujemy pulę unikalnych kombinacji (nazwa_bazowa + wariant) per kategoria,
# żeby żadne dwa SKU w tej samej kategorii nie miały identycznej nazwy produktu.
category_name_pools = {}
for cat, base_names in CATEGORIES.items():
    combos = [f"{bn}{v}".strip() for bn in base_names for v in VARIANTS]
    random.shuffle(combos)
    category_name_pools[cat] = combos

category_name_index = {cat: 0 for cat in CATEGORY_LIST}

def get_unique_product_name(category):
    pool = category_name_pools[category]
    idx = category_name_index[category]
    if idx < len(pool):
        name = pool[idx]
    else:
        # Pula kombinacji wyczerpana (mało prawdopodobne przy N_SKU=500) -
        # dodajemy numer wersji, żeby nazwa nadal była unikalna.
        base_idx = idx - len(pool)
        base_combo = pool[base_idx % len(pool)]
        name = f"{base_combo} (wersja {base_idx // len(pool) + 2})"
    category_name_index[category] += 1
    return name

skus = []
for i in range(1, N_SKU + 1):
    category = random.choice(CATEGORY_LIST)
    product_name = get_unique_product_name(category)

    price_low, price_high = CATEGORY_PRICE_RANGE[category]
    unit_price = round(np.random.uniform(price_low, price_high), 2)

    # Bazowy miesięczny popyt - rozkład log-normalny zamiast jednostajnego,
    # żeby uzyskać realistyczny efekt Pareto: nieliczne produkty o bardzo
    # wysokim popycie, większość ze skromną sprzedażą (klasyczny "długi ogon").
    base_demand = np.random.lognormal(mean=2.2, sigma=1.3)
    base_demand = np.clip(base_demand, 1, 2000)

    # Sezonowość i szum - zależne od wzorca popytu przypisanego do SKU (patrz niżej),
    # żeby uzyskać realistyczny rozkład w analizie XYZ (stabilne/sezonowe/nieregularne popyty).
    demand_pattern = np.random.choice(
        ["stabilny", "sezonowy", "nieregularny"], p=[0.30, 0.40, 0.30]
    )
    if demand_pattern == "stabilny":
        seasonal_amplitude = np.random.uniform(0, 0.15)
        noise_std = 0.08
        zero_month_prob = 0.0
    elif demand_pattern == "sezonowy":
        seasonal_amplitude = np.random.uniform(0.5, 1.0)
        noise_std = 0.20
        zero_month_prob = 0.0
    else:  # nieregularny - popyt "lumpy", trudny do prognozowania
        seasonal_amplitude = np.random.uniform(0.1, 0.4)
        noise_std = 0.70
        zero_month_prob = 0.30

    seasonal_phase = np.random.uniform(0, 2 * np.pi)

    # Trend - lekki wzrost/spadek w czasie
    trend = np.random.uniform(-0.01, 0.02)

    skus.append({
        "SKU": f"SKU-{i:04d}",
        "Nazwa produktu": product_name,
        "Kategoria": category,
        "Wartość jednostkowa": unit_price,
        "base_demand": base_demand,
        "seasonal_amplitude": seasonal_amplitude,
        "seasonal_phase": seasonal_phase,
        "trend": trend,
        "noise_std": noise_std,
        "zero_month_prob": zero_month_prob,
        "demand_pattern": demand_pattern,
    })

sku_df = pd.DataFrame(skus)

# ---------------------------------------------------------------------
# 3. Generowanie danych miesięcznych (24 miesiące) dla każdego SKU
# ---------------------------------------------------------------------
records = []
for _, row in sku_df.iterrows():
    for m in range(N_MONTHS):
        current_date = START_DATE + relativedelta(months=m)

        # Model popytu: bazowy popyt * sezonowość * trend + szum (zależny od wzorca popytu)
        seasonal_factor = 1 + row["seasonal_amplitude"] * np.sin(2 * np.pi * m / 12 + row["seasonal_phase"])
        trend_factor = 1 + row["trend"] * m
        noise = max(0, np.random.normal(1.0, row["noise_std"]))

        quantity = row["base_demand"] * seasonal_factor * trend_factor * noise

        # Dla wzorca "nieregularnego" - część miesięcy ma zerowy popyt (typowy "lumpy demand")
        if np.random.random() < row["zero_month_prob"]:
            quantity = 0

        quantity = max(0, round(quantity))  # brak ujemnych ilości

        # Lekka losowa fluktuacja ceny jednostkowej (np. promocje, inflacja)
        unit_price = round(row["Wartość jednostkowa"] * np.random.uniform(0.95, 1.05), 2)

        records.append({
            "SKU": row["SKU"],
            "Nazwa produktu": row["Nazwa produktu"],
            "Kategoria": row["Kategoria"],
            "Data": current_date.strftime("%Y-%m-%d"),
            "Ilość wydana": int(quantity),
            "Wartość jednostkowa": unit_price,
        })

result_df = pd.DataFrame(records)

# ---------------------------------------------------------------------
# 4. Zapis do CSV
# ---------------------------------------------------------------------
output_path = "/mnt/user-data/outputs/dane_sprzedazy_sku.csv"
result_df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"Wygenerowano {len(result_df):,} wierszy dla {N_SKU} SKU w {len(CATEGORY_LIST)} kategoriach.")
print(f"Zakres dat: {result_df['Data'].min()} - {result_df['Data'].max()}")
print(f"Zapisano do: {output_path}")
print("\nPodgląd danych:")
print(result_df.head(10).to_string(index=False))
print("\nLiczba SKU na kategorię:")
print(sku_df["Kategoria"].value_counts())
