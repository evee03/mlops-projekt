s99633
## Porównanie narzędzi do zarządzania środowiskiem

| Narzędzie | Czas instalacji (przykład) | Plik zależności | Komenda odtwarzająca środowisko | Rekomendacja |
| :--- | :--- | :--- | :--- | :--- |
| **venv** | Kilka/kilkanaście sekund | `requirements.txt` | `pip install -r requirements.txt` | Proste projekty, gdy nie chcemy instalować dodatkowych narzędzi poza standardowym Pythonem. |
| **uv** | Ułamek sekundy (~0.01s) | `requirements.txt` | `uv pip install -r requirements.txt` | Gdy zależy nam na ekstremalnej szybkości i instalujemy wyłącznie pakiety pythonowe. |
| **conda** | Często powyżej minuty | `environment.yml` | `conda env create -f environment.yml` | Złożone projekty ML, wymagające zewnętrznych bibliotek systemowych (np. sterowniki C++, CUDA). |
| **DVC** | - | Wersjonuje: **duże zbiory danych i modele ML** | **Czym różni się od Gita:** Git śledzi zmiany w małych plikach tekstowych (kodzie). DVC trzyma ciężkie pliki w zewnętrznym magazynie, a w Gicie zapisuje jedynie lekkie wskaźniki (metadane) do tych plików. |