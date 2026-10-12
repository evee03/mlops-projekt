s99633
## Porównanie narzędzi do zarządzania środowiskiem

| Narzędzie | Czas instalacji (przykład) | Plik zależności | Komenda odtwarzająca środowisko | Rekomendacja |
| :--- | :--- | :--- | :--- | :--- |
| **venv** | Kilka/kilkanaście sekund | `requirements.txt` | `pip install -r requirements.txt` | Proste projekty, gdy nie chcemy instalować dodatkowych narzędzi poza standardowym Pythonem. |
| **uv** | Ułamek sekundy (~0.01s) | `requirements.txt` | `uv pip install -r requirements.txt` | Gdy zależy nam na ekstremalnej szybkości i instalujemy wyłącznie pakiety pythonowe. |
| **conda** | Często powyżej minuty | `environment.yml` | `conda env create -f environment.yml` | Złożone projekty ML, wymagające zewnętrznych bibliotek systemowych (np. sterowniki C++, CUDA). |
| **DVC** | - | Wersjonuje: **duże zbiory danych i modele ML** | **Czym różni się od Gita:** Git śledzi zmiany w małych plikach tekstowych (kodzie). DVC trzyma ciężkie pliki w zewnętrznym magazynie, a w Gicie zapisuje jedynie lekkie wskaźniki (metadane) do tych plików. |

## Ćwiczenie 3: Odtwarzanie projektu z repozytorium inną osobę

### Wykonane kroki:
1. Sklonowanie obcego repozytorium: `git clone https://github.com/Squashim/mlops-projekt.git`
2. Próba instalacji zależności: `pip install -r requirements.txt`

### Napotkane problemy i wnioski:
* **Konflikt wersji zależności i Pythona:** Podczas instalacji pakietów pojawił się błąd `ERROR: No matching distribution found for numpy==2.5.4`. Wersja biblioteki zdefiniowana przez inną osobę w pliku `requirements.txt` wymagała innej wersji interpretera Pythona niż ta zainstalowana w naszym środowisku testowym (Python 3.11).
* **Brak uniwersalności `requirements.txt`:** Zwykły plik `requirements.txt` przypisany do sztywnej wersji pakietu nie gwarantuje reprodukowarności na różnych maszynach z innymi wersjami Pythona lub systemów operacyjnych.
* **Rozwiązanie MLOps:** Użycie narzędzi takich jak `conda` z plikiem `environment.yml` lub pełna konteneryzacja za pomocą `Docker` pozwala uniknąć tego typu rozbieżności w wersjach środowiska między członkami zespołu.