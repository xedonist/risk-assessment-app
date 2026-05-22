# Aplikacja do Szacowania Ryzyka w Bezpieczeństwie Informacji

## Opis Projektu
Projekt zrealizowany w ramach przedmiotu "Zarządzanie Ryzykiem IT" (Zadanie na ocenę celującą). Aplikacja stanowi interaktywne narzędzie wspierające analityków w procesie szacowania, wizualizacji oraz obsługi ryzyka zgodnie z najlepszymi praktykami bezpieczeństwa informacji (m.in. ISO 27005). 

Aplikacja częściowo automatyzuje proces zarządzania ryzykiem, pozwalając na odejście od statycznych arkuszy kalkulacyjnych na rzecz dynamicznego środowiska.

## Zrealizowane Wymagania i Zaawansowane Funkcje
* **Zarządzanie danymi wejściowymi:** Interaktywny formularz do dodawania aktywów, zagrożeń, podatności oraz istniejących zabezpieczeń.
* **Strategia Postępowania z Ryzykiem (Risk Treatment):** Możliwość przypisania decyzji dla każdego ryzyka (Redukcja, Akceptacja, Przeniesienie, Unikanie).
* **Dynamiczne Dashboardy:** Główne wskaźniki KPI (całkowita liczba ryzyk, podział na kategorie krytyczności) wyświetlane w czasie rzeczywistym nad rejestrem.
* **Definiowanie kryteriów oceny:** Użytkownik ma możliwość płynnej modyfikacji "apetytu na ryzyko" (dynamiczne definiowanie progów dla ryzyk średnich i wysokich).
* **Automatyczne wyliczanie:** Poziom ryzyka jest wyliczany w czasie rzeczywistym na podstawie metody ilościowo-jakościowej (Prawdopodobieństwo x Skutek w skali 1-5).
* **Wizualizacja:** Automatycznie generowana, interaktywna Macierz Ryzyka (wykres punktowy) oznaczona kolorami.
* **Eksport i Zapis (Import/Eksport):** Możliwość pobrania rejestru jako pliku CSV, zaawansowany eksport do profesjonalnego raportu PDF oraz opcja wczytania wcześniej zapisanego pliku do dalszej pracy.

## Wymagania Techniczne (Stos Technologiczny)
Projekt został napisany w języku Python ze szczególnym naciskiem na architekturę jednoplikową (skrypt `app.py`), co znacząco ułatwia wdrożenie i utrzymanie.
* **Streamlit** - silnik interfejsu graficznego (GUI / Web App)
* **Pandas** - przetwarzanie danych i strukturyzacja rejestru
* **Plotly** - generowanie interaktywnych wizualizacji (Macierz Ryzyka)
* **NumPy** - obsługa obliczeń i algorytmów wizualnych (Jitter na wykresach)
* **FPDF** - generowanie profesjonalnych raportów tekstowych (PDF)

## Instrukcja Uruchomienia Lokalnego

1. Upewnij się, że masz zainstalowane środowisko Python (wersja 3.8 lub nowsza).
2. Sklonuj lub rozpakuj folder z projektem.
3. Otwórz terminal w folderze projektu i zainstaluj wymagane biblioteki poleceniem:
   `pip install -r requirements.txt`
4. Uruchom aplikację komendą:
   `streamlit run app.py`
5. Aplikacja otworzy się automatycznie w domyślnej przeglądarce internetowej.

---

# Information Security Risk Assessment Application

## Project Description
This project was developed for the "IT Risk Management" course (Targeting the highest grade). The application is an interactive tool designed to support analysts in the process of estimating, visualizing, and treating risk according to information security best practices (e.g., ISO 27005).

## Implemented Features
* **Input Data Management:** Interactive form for adding assets, threats, vulnerabilities, and existing security controls.
* **Risk Treatment Strategy:** Ability to assign a treatment decision for each risk (Mitigate, Accept, Transfer, Avoid).
* **Dynamic Dashboards:** Key Performance Indicators (total risks, breakdown by category) displayed in real-time above the register.
* **Defining Evaluation Criteria:** Users can dynamically modify the "risk appetite" (defining thresholds for medium and high risks on the fly).
* **Automatic Calculation:** Risk levels are calculated in real-time based on a quantitative-qualitative method (Probability x Impact on a 1-5 scale).
* **Visualization:** Automatically generated, interactive Risk Matrix (scatter plot) with color coding.
* **Export and Import:** Capability to download the register as a CSV file, generate professional PDF reports, and load a previously saved project file to continue working.

## Technical Requirements (Tech Stack)
* **Streamlit** - Graphical User Interface engine (Web App)
* **Pandas** - Data processing and register structuring
* **Plotly** - Generating interactive visualizations (Risk Matrix)
* **NumPy** - Handling calculations and visual algorithms (Jitter on charts)
* **FPDF** - Generating text reports (PDF)

## Local Setup Instructions

1. Ensure you have a Python environment installed (version 3.8 or newer).
2. Clone or extract the project folder.
3. Open a terminal in the project folder and install the required libraries using the command:
   `pip install -r requirements.txt`
4. Run the application with the command:
   `streamlit run app.py`
5. The application will open automatically in your default web browser.
