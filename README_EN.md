# Information Security Risk Assessment Application

## Project Description
This project was developed for the "IT Risk Management" course (Targeting the highest grade). The application is an interactive tool designed to support analysts in the process of estimating and visualizing risk according to information security best practices. 

The application partially automates the risk management process, allowing users to transition from static spreadsheets to a dynamic environment.

## Implemented Features
* **Input Data Management:** Interactive form for adding assets, threats, vulnerabilities, and existing security controls.
* **Defining Evaluation Criteria:** Users can dynamically modify the "risk appetite" (defining thresholds for medium and high risks on the fly).
* **Automatic Calculation:** Risk levels are calculated in real-time based on a quantitative-qualitative method (Probability × Impact on a 1-5 scale).
* **Visualization:** Automatically generated, interactive Risk Matrix (scatter plot) with color coding.
* **Filtering and Analysis:** Ability to filter the risk register based on the assigned category.
* **Save and Load Projects (Export/Import):** Capability to download the register as a CSV file and load a previously saved file to continue working.

## Technical Requirements (Tech Stack)
The project is written in Python with a strong emphasis on a single-file architecture (`app.py` script), which significantly simplifies deployment and maintenance.
* **Streamlit** - Graphical User Interface engine (Web App)
* **Pandas** - Data processing and register structuring
* **Plotly** - Generating interactive visualizations (Risk Matrix)
* **NumPy** - Handling calculations and visual algorithms (Jitter on charts)

## Local Setup Instructions

1. Ensure you have a Python environment installed (version 3.8 or newer).
2. Clone or extract the project folder.
3. Open a terminal in the project folder and install the required libraries using the command:
   `pip install -r requirements.txt`
4. Run the application with the command:
   `streamlit run app.py`
5. The application will open automatically in your default web browser.
