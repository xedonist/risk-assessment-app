import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

if 'risks' not in st.session_state:
    st.session_state.risks = []

translations = {
    "EN": {
        "title": "Information Security Risk Assessment",
        "sidebar_title": "Add New Risk",
        "asset": "Asset Name",
        "threat": "Threat",
        "vulnerability": "Vulnerability",
        "controls": "Existing Controls",
        "probability": "Probability (1-5)",
        "impact": "Consequences (1-5)",
        "add_btn": "Add to Register",
        "req_warning": "Please fill in Asset, Threat, and Vulnerability.",
        "settings_title": "Risk Appetite Settings",
        "med_threshold": "Medium Risk Threshold",
        "high_threshold": "High Risk Threshold",
        "upload_csv": "Upload Project (CSV)",
        "import_btn": "Import CSV",
        "upload_success": "Project loaded successfully!",
        "upload_error": "Error loading file or invalid format.",
        "low": "Low",
        "medium": "Medium",
        "high": "High",
        "filter": "Filter by Category",
        "all": "All",
        "matrix_title": "Risk Matrix",
        "download_btn": "Download CSV",
        "risk_level": "Risk Level",
        "category": "Category",
        "table_title": "Risk Register",
        "no_data": "No risks added yet. Please use the sidebar to add entries."
    },
    "PL": {
        "title": "Ocena Ryzyka Bezpieczeństwa Informacji",
        "sidebar_title": "Dodaj Nowe Ryzyko",
        "asset": "Nazwa Aktywa",
        "threat": "Zagrożenie",
        "vulnerability": "Podatność",
        "controls": "Istniejące Zabezpieczenia",
        "probability": "Prawdopodobieństwo (1-5)",
        "impact": "Skutki (1-5)",
        "add_btn": "Dodaj do Rejestru",
        "req_warning": "Proszę wypełnić Aktywo, Zagrożenie i Podatność.",
        "settings_title": "Kryteria Akceptacji Ryzyka",
        "med_threshold": "Próg Średniego Ryzyka",
        "high_threshold": "Próg Wysokiego Ryzyka",
        "upload_csv": "Wgraj Projekt (CSV)",
        "import_btn": "Importuj CSV",
        "upload_success": "Projekt załadowany pomyślnie!",
        "upload_error": "Błąd ładowania pliku lub zły format.",
        "low": "Niski",
        "medium": "Średni",
        "high": "Wysoki",
        "filter": "Filtruj po Kategorii",
        "all": "Wszystkie",
        "matrix_title": "Macierz Ryzyka",
        "download_btn": "Pobierz CSV",
        "risk_level": "Poziom Ryzyka",
        "category": "Kategoria",
        "table_title": "Rejestr Ryzyk",
        "no_data": "Brak dodanych ryzyk. Użyj panelu bocznego, aby dodać wpisy."
    }
}

lang = st.sidebar.radio("Language / Język", ["EN", "PL"], horizontal=True)
t = translations[lang]

def get_internal_category(score, med_t, high_t):
    if score < med_t:
        return "low"
    elif score < high_t:
        return "medium"
    else:
        return "high"

st.sidebar.header(t["settings_title"])
med_thresh = st.sidebar.number_input(t["med_threshold"], min_value=2, max_value=25, value=5)
high_thresh = st.sidebar.number_input(t["high_threshold"], min_value=int(med_thresh), max_value=25, value=15)
st.sidebar.divider()

st.sidebar.header(t["sidebar_title"])
asset_input = st.sidebar.text_input(t["asset"])
threat_input = st.sidebar.text_input(t["threat"])
vuln_input = st.sidebar.text_input(t["vulnerability"])
controls_input = st.sidebar.text_input(t["controls"])
prob_input = st.sidebar.slider(t["probability"], 1, 5, 1)
impact_input = st.sidebar.slider(t["impact"], 1, 5, 1)

if st.sidebar.button(t["add_btn"]):
    if not asset_input or not threat_input or not vuln_input:
        st.sidebar.error(t["req_warning"])
    else:
        st.session_state.risks.append({
            "asset": asset_input,
            "threat": threat_input,
            "vulnerability": vuln_input,
            "controls": controls_input,
            "probability": prob_input,
            "impact": impact_input
        })
        st.sidebar.success("Added!")

st.sidebar.divider()

st.sidebar.header(t["upload_csv"])
uploaded_file = st.sidebar.file_uploader("", type=["csv"])
if st.sidebar.button(t["import_btn"]):
    if uploaded_file is not None:
        try:
            import_df = pd.read_csv(uploaded_file, sep=';')
            
            reverse_map = {}
            for lang_code, lang_dict in translations.items():
                reverse_map[lang_dict["asset"]] = "asset"
                reverse_map[lang_dict["threat"]] = "threat"
                reverse_map[lang_dict["vulnerability"]] = "vulnerability"
                reverse_map[lang_dict["controls"]] = "controls"
                reverse_map[lang_dict["probability"]] = "probability"
                reverse_map[lang_dict["impact"]] = "impact"
            
            new_risks = []
            for _, row in import_df.iterrows():
                risk = {"controls": ""}
                for col in import_df.columns:
                    if col in reverse_map:
                        risk[reverse_map[col]] = row[col]
                
                if "asset" in risk and "probability" in risk and "impact" in risk:
                    risk["probability"] = int(risk["probability"])
                    risk["impact"] = int(risk["impact"])
                    new_risks.append(risk)
                    
            st.session_state.risks = new_risks
            st.sidebar.success(t["upload_success"])
            st.rerun()
        except Exception as e:
            st.sidebar.error(t["upload_error"])

st.title(t["title"])

if not st.session_state.risks:
    st.info(t["no_data"])
else:
    df = pd.DataFrame(st.session_state.risks)
    
    df['risk_level'] = df['probability'] * df['impact']
    df['internal_category'] = df['risk_level'].apply(lambda x: get_internal_category(x, med_thresh, high_thresh))
    df['category'] = df['internal_category'].map(lambda x: t[x])
    
    display_df = df.rename(columns={
        "asset": t["asset"],
        "threat": t["threat"],
        "vulnerability": t["vulnerability"],
        "controls": t["controls"],
        "probability": t["probability"],
        "impact": t["impact"],
        "risk_level": t["risk_level"],
        "category": t["category"]
    }).drop(columns=["internal_category"])
    
    st.subheader(t["table_title"])
    filter_options = [t["all"], t["low"], t["medium"], t["high"]]
    selected_filter = st.selectbox(t["filter"], filter_options)
    
    if selected_filter == t["all"]:
        filtered_df = display_df
    else:
        filtered_df = display_df[display_df[t["category"]] == selected_filter]
        
    st.dataframe(filtered_df, use_container_width=True)
    
    st.divider()

    st.subheader(t["matrix_title"])
    
    if not filtered_df.empty:
        color_map = {
            t["low"]: "green",
            t["medium"]: "yellow",
            t["high"]: "red"
        }
        
        plot_df = filtered_df.copy()
        plot_df['plot_impact'] = plot_df[t["impact"]] + np.random.uniform(-0.15, 0.15, len(plot_df))
        plot_df['plot_prob'] = plot_df[t["probability"]] + np.random.uniform(-0.15, 0.15, len(plot_df))
        
        fig = px.scatter(
            plot_df,
            x='plot_impact',
            y='plot_prob',
            color=t["category"],
            hover_name=t["asset"],
            hover_data={
                'plot_impact': False,
                'plot_prob': False,
                t["probability"]: True,
                t["impact"]: True,
                t["threat"]: True,
                t["vulnerability"]: True,
                t["controls"]: True,
                t["risk_level"]: True
            },
            color_discrete_map=color_map,
            size_max=15
        )
        
        fig.update_layout(
            xaxis=dict(title=t["impact"], range=[0.5, 5.5], tickmode='linear', dtick=1),
            yaxis=dict(title=t["probability"], range=[0.5, 5.5], tickmode='linear', dtick=1)
        )
        fig.update_traces(marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey')))
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        csv_data = filtered_df.to_csv(index=False, sep=';').encode('utf-8-sig')
        st.download_button(
            label=t["download_btn"],
            data=csv_data,
            file_name="risk_register.csv",
            mime="text/csv"
        )