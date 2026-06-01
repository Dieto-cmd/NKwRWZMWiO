# Crocodile Path Finder

Projekt na zaliczenie przedmiotu *Narzędzia komputerowe w rozwiązywaniu zadań matematycznych i obliczeniowych* (AGH).

## Treść zadania

Zostałaś schwytana i masz zostać rzucona krokodylom. Dostrzegasz szansę ucieczki — możesz przeskoczyć przez Nil, skacząc po krokodylach. Maksymalny skok to **5 łokci**. Program sprawdza, czy istnieje taka droga, a jeśli tak — wypisuje ją.

## Algorytm

Program używa **DFS (przeszukiwanie w głąb)** z filtrem odległości:

- Graf wczytywany jest z pliku JSON
- Krawędzie o wadze > 5 są ignorowane (skok za daleki)
- DFS szuka dowolnej ścieżki od węzła startowego do docelowego używając tylko dozwolonych krawędzi

## Wymagania

Python 3.x oraz biblioteki:

```
pip install networkx matplotlib scipy
```

## Uruchomienie

```bash
py main.py                        # domyślny plik: input_node_link_data.json
py main.py input_no_path.json     # własny plik z danymi
```

## Format pliku wejściowego

Plik JSON z listą węzłów i krawędzi. Jeden węzeł musi mieć `"start": true`, jeden `"end": true`. Pole `value` to odległość między krokodylami (w łokciach).

```json
{
    "nodes": [
        {"id": "A", "start": true},
        {"id": "B"},
        {"id": "C", "end": true}
    ],
    "links": [
        {"source": "A", "target": "B", "value": 3},
        {"source": "B", "target": "C", "value": 4}
    ]
}
```

## Przykładowe pliki

| Plik | Opis |
|------|------|
| `input_node_link_data.json` | 13 węzłów, droga istnieje |
| `input_no_path.json` | 8 węzłów, brak przejścia (wszystkie mosty za daleko) |

## Wynik

Program wypisuje znalezioną ścieżkę w konsoli i otwiera okno z wizualizacją grafu:

- **lewy wykres** — pełny graf; krawędzie niebieskie = osiągalne, pomarańczowe przerywane = za daleko
- **prawy wykres** — znaleziona ścieżka wyróżniona na pomarańczowo

### Legenda węzłów

| Kolor | Znaczenie |
|-------|-----------|
| Zielony | Węzeł startowy |
| Czerwony | Węzeł docelowy |
| Pomarańczowy | Węzeł na znalezionej ścieżce |
| Niebieski | Pozostałe węzły |

## Struktura projektu

```
.
├── main.py                     # główny program
├── find_path.py                # algorytm DFS
├── input_node_link_data.json   # przykład: droga istnieje
└── input_no_path.json          # przykład: brak drogi
```
