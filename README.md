# Aplikacja do Szacowania Ryzyka w Bezpieczeństwie Informacji

## Opis Projektu
Projekt zrealizowany w ramach przedmiotu "Zarządzanie Ryzykiem IT" (Zadanie na ocenę celującą). Aplikacja stanowi interaktywne narzędzie wspierające analityków w procesie szacowania i wizualizacji ryzyka zgodnie z najlepszymi praktykami bezpieczeństwa informacji. 

Aplikacja częściowo automatyzuje proces zarządzania ryzykiem, pozwalając na odejście od statycznych arkuszy kalkulacyjnych na rzecz dynamicznego środowiska.

## Zrealizowane Wymagania
* **Zarządzanie danymi wejściowymi:** Interaktywny formularz do dodawania aktywów, zagrożeń, podatności oraz istniejących zabezpieczeń.
* **Definiowanie kryteriów oceny:** Użytkownik ma możliwość płynnej modyfikacji "apetytu na ryzyko" (dynamiczne definiowanie progów dla ryzyk średnich i wysokich).
* **Automatyczne wyliczanie:** Poziom ryzyka jest wyliczany w czasie rzeczywistym na podstawie metody ilościowo-jakościowej (Prawdopodobieństwo × Skutek w skali 1-5).
* **Wizualizacja:** Automatycznie generowana, interaktywna Macierz Ryzyka (wykres punktowy) oznaczona kolorami.
* **Filtrowanie i analiza:** Możliwość filtrowania rejestru ryzyk na podstawie przypisanej kategorii.
* **Zapis i odczyt projektów (Eksport/Import):** Możliwość pobrania rejestru jako pliku CSV oraz wczytania wcześniej zapisanego pliku do dalszej pracy.

## Wymagania Techniczne (Stos Technologiczny)
Projekt został napisany w języku Python ze szczególnym naciskiem na architekturę jednoplikową (skrypt `app.py`), co znacząco ułatwia wdrożenie i utrzymanie.
* **Streamlit** - silnik interfejsu graficznego (GUI / Web App)
* **Pandas** - przetwarzanie danych i strukturyzacja rejestru
* **Plotly** - generowanie interaktywnych wizualizacji (Macierz Ryzyka)
* **NumPy** - obsługa obliczeń i algorytmów wizualnych (Jitter na wykresach)

## Instrukcja Uruchomienia Lokalnego

1. Upewnij się, że masz zainstalowane środowisko Python (wersja 3.8 lub nowsza).
2. Sklonuj lub rozpakuj folder z projektem.
3. Otwórz terminal w folderze projektu i zainstaluj wymagane biblioteki poleceniem:
   `pip install -r requirements.txt`
4. Uruchom aplikację komendą:
   `streamlit run app.py`
5. Aplikacja otworzy się automatycznie w domyślnej przeglądarce internetowej.
