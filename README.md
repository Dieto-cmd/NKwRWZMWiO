# Crocodile Path Finder

Projekt na zaliczenie przedmiotu *Narzędzia komputerowe w rozwiązywaniu zadań matematycznych i obliczeniowych* (AGH).

## Treść zadania

Zostałaś schwytana i masz zostać rzucona krokodylom. Dostrzegasz szansę ucieczki — możesz przeskoczyć przez Nil, skacząc po krokodylach. Maksymalny skok to **5 łokci**. Program sprawdza, czy istnieje taka droga, a jeśli tak — wypisuje ją i wizualizuje w układzie współrzędnych.

## Algorytm

Program używa **DFS (przeszukiwanie w głąb)** z filtrem odległości:

- Odległości między krokodylami liczone są jako odległość euklidesowa z podanych współrzędnych
- Odległość od brzegu do krokodyla to jego współrzędna `x` (prostopadła do linii brzegu)
- DFS przechodzi tylko krawędziami o odległości ≤ 5 łokci
- Zwraca pierwszą znalezioną ścieżkę lub informuje o braku drogi

## Wymagania

Python 3.x oraz biblioteki:

```
pip install networkx matplotlib scipy
```

## Uruchomienie

```bash
py main.py                              # domyślny plik: input_coords.json
py main.py input_coords_no_path.json   # przykład bez drogi
py main.py moje_dane.json              # własny plik
```

## Format pliku wejściowego

Plik JSON z szerokością rzeki i listą pozycji krokodyli. Rzeka rozumiana jest jako dwie równoległe linie (brzegi) — program automatycznie oblicza wszystkie odległości.

```json
{
    "river_width": 18,
    "max_jump": 5,
    "crocodiles": [
        {"id": "A", "x": 3,  "y": 7},
        {"id": "B", "x": 8,  "y": 4},
        {"id": "C", "x": 14, "y": 9}
    ]
}
```

| Pole | Opis |
|------|------|
| `river_width` | Szerokość rzeki w łokciach |
| `max_jump` | Maksymalny skok (opcjonalne, domyślnie 5) |
| `id` | Nazwa krokodyla (dowolny tekst) |
| `x` | Odległość od lewego brzegu w łokciach |
| `y` | Pozycja wzdłuż rzeki w łokciach |

## Pliki dołączone do projektu

| Plik | Opis |
|------|------|
| `main.py` | Główny program |
| `find_path.py` | Implementacja algorytmu DFS |
| `input_coords.json` | 10 krokodyli, rzeka 18 łokci — droga istnieje |
| `input_coords_no_path.json` | 8 krokodyli, rzeka 20 łokci — brak drogi |
| `instrukcja.txt` | Szczegółowa instrukcja obsługi |

## Wizualizacja

Program otwiera okno z widokiem rzeki w układzie współrzędnych:

- Oś X — odległość od lewego brzegu w łokciach
- Oś Y — pozycja wzdłuż rzeki
- Zielony pasek po lewej — brzeg startowy
- Czerwony pasek po prawej — brzeg docelowy
- Niebieskie linie — osiągalne połączenia (≤ 5 łokci) z podpisanymi odległościami
- Pomarańczowe strzałki — znaleziona ścieżka przejścia

### Legenda węzłów

| Kolor | Znaczenie |
|-------|-----------|
| Zielony | Krokodyl poza ścieżką |
| Pomarańczowy | Krokodyl na znalezionej ścieżce |
