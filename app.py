import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import unicodedata
from fpdf import FPDF
import io

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
        "treatment": "Risk Treatment",
        "mitigate": "Mitigate",
        "accept": "Accept",
        "transfer": "Transfer",
        "avoid": "Avoid",
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
        "download_pdf_btn": "Download PDF",
        "risk_level": "Risk Level",
        "category": "Category",
        "table_title": "Risk Register",
        "no_data": "No risks added yet. Please use the sidebar to add entries.",
        "total_risks": "Total Risks",
        "critical_risks": "Critical Risks",
        "medium_risks": "Medium Risks",
        "low_risks": "Low Risks",
        "report_title": "Risk Report"
    },
    "PL": {
        "title": "Ocena Ryzyka Bezpieczeństwa Informacji",
        "sidebar_title": "Dodaj Nowe Ryzyko",
        "asset": "Nazwa Aktywa",
        "threat": "Zagrożenie",
        "vulnerability": "Podatność",
        "controls": "Istniejące Zabezpieczenia",
        "treatment": "Postępowanie z ryzykiem",
        "mitigate": "Redukcja (Mitigate)",
        "accept": "Akceptacja (Accept)",
        "transfer": "Przeniesienie (Transfer)",
        "avoid": "Unikanie (Avoid)",
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
        "download_pdf_btn": "Pobierz PDF",
        "risk_level": "Poziom Ryzyka",
        "category": "Kategoria",
        "table_title": "Rejestr Ryzyk",
        "no_data": "Brak dodanych ryzyk. Użyj panelu bocznego, aby dodać wpisy.",
        "total_risks": "Całkowita liczba ryzyk",
        "critical_risks": "Ryzyka Wysokie",
        "medium_risks": "Ryzyka Średnie",
        "low_risks": "Ryzyka Niskie",
        "report_title": "Raport Ryzyka"
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

def normalize_text_for_pdf(text):
    pl_map = {'ą':'a', 'ć':'c', 'ę':'e', 'ł':'l', 'ń':'n', 'ó':'o', 'ś':'s', 'ź':'z', 'ż':'z',
              'Ą':'A', 'Ć':'C', 'Ę':'E', 'Ł':'L', 'Ń':'N', 'Ó':'O', 'Ś':'S', 'Ź':'Z', 'Ż':'Z'}
    res = str(text)
    for k, v in pl_map.items():
        res = res.replace(k, v)
    return unicodedata.normalize('NFKD', res).encode('ascii', 'ignore').decode('ascii')

def truncate(text, max_len):
    text = str(text)
    return text[:max_len-2] + ".." if len(text) > max_len else text

def generate_pdf(dataframe, t_dict):
    pdf = FPDF()
    pdf.add_page(orientation="L")
    
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, normalize_text_for_pdf(t_dict["report_title"]), ln=True, align="C")
    pdf.ln(5)
    
    col_widths = [40, 45, 45, 45, 45, 20, 35]
    char_limits = [20, 24, 24, 24, 24, 10, 18]
    
    pdf.set_font("Arial", "B", 8)
    headers = [t_dict["asset"], t_dict["threat"], t_dict["vulnerability"], 
               t_dict["treatment"], t_dict["controls"], t_dict["risk_level"], t_dict["category"]]
    
    for i, header in enumerate(headers):
        h_text = normalize_text_for_pdf(header)
        pdf.cell(col_widths[i], 10, truncate(h_text, char_limits[i]), border=1, align="C")
    pdf.ln()
    
    pdf.set_font("Arial", "", 8)
    for _, row in dataframe.iterrows():
        pdf.cell(col_widths[0], 10, truncate(normalize_text_for_pdf(row[t_dict["asset"]]), char_limits[0]), border=1)
        pdf.cell(col_widths[1], 10, truncate(normalize_text_for_pdf(row[t_dict["threat"]]), char_limits[1]), border=1)
        pdf.cell(col_widths[2], 10, truncate(normalize_text_for_pdf(row[t_dict["vulnerability"]]), char_limits[2]), border=1)
        pdf.cell(col_widths[3], 10, truncate(normalize_text_for_pdf(row[t_dict["treatment"]]), char_limits[3]), border=1)
        pdf.cell(col_widths[4], 10, truncate(normalize_text_for_pdf(row[t_dict["controls"]]), char_limits[4]), border=1)
        pdf.cell(col_widths[5], 10, str(row[t_dict["risk_level"]]), border=1, align="C")
        pdf.cell(col_widths[6], 10, truncate(normalize_text_for_pdf(row[t_dict["category"]]), char_limits[6]), border=1)
        pdf.ln()
        
    pdf_out = pdf.output(dest="S")
    if isinstance(pdf_out, (bytes, bytearray)):
        return bytes(pdf_out)
    return pdf_out.encode("latin-1", "replace")

st.sidebar.header(t["settings_title"])
med_thresh = st.sidebar.number_input(t["med_threshold"], min_value=2, max_value=25, value=5)
high_thresh = st.sidebar.number_input(t["high_threshold"], min_value=int(med_thresh), max_value=25, value=15)
st.sidebar.divider()

st.sidebar.header(t["sidebar_title"])
asset_input = st.sidebar.text_input(t["asset"])
threat_input = st.sidebar.text_input(t["threat"])
vuln_input = st.sidebar.text_input(t["vulnerability"])
controls_input = st.sidebar.text_input(t["controls"])

treatment_options_internal = ["mitigate", "accept", "transfer", "avoid"]
treatment_options_display = [t[opt] for opt in treatment_options_internal]
treatment_selection = st.sidebar.selectbox(t["treatment"], treatment_options_display)
treatment_internal = treatment_options_internal[treatment_options_display.index(treatment_selection)]

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
            "treatment": treatment_internal,
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
                reverse_map[lang_dict["treatment"]] = "treatment"
                reverse_map[lang_dict["probability"]] = "probability"
                reverse_map[lang_dict["impact"]] = "impact"
            
            new_risks = []
            for _, row in import_df.iterrows():
                risk = {"controls": "", "treatment": "mitigate"}
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
    df['treatment_display'] = df['treatment'].map(lambda x: t[x] if x in t else x)
    
    display_df = df.rename(columns={
        "asset": t["asset"],
        "threat": t["threat"],
        "vulnerability": t["vulnerability"],
        "controls": t["controls"],
        "treatment_display": t["treatment"],
        "probability": t["probability"],
        "impact": t["impact"],
        "risk_level": t["risk_level"],
        "category": t["category"]
    }).drop(columns=["internal_category", "treatment"])
    
    st.subheader(t["table_title"])
    
    filter_options = [t["all"], t["low"], t["medium"], t["high"]]
    selected_filter = st.selectbox(t["filter"], filter_options)
    
    if selected_filter == t["all"]:
        filtered_df = display_df
    else:
        filtered_df = display_df[display_df[t["category"]] == selected_filter]
        
    dash_col1, dash_col2, dash_col3, dash_col4 = st.columns(4)
    dash_col1.metric(t["total_risks"], len(filtered_df))
    dash_col2.metric(t["critical_risks"], len(filtered_df[filtered_df[t["category"]] == t["high"]]))
    dash_col3.metric(t["medium_risks"], len(filtered_df[filtered_df[t["category"]] == t["medium"]]))
    dash_col4.metric(t["low_risks"], len(filtered_df[filtered_df[t["category"]] == t["low"]]))
    
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
                t["treatment"]: True,
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
        
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            csv_data = filtered_df.to_csv(index=False, sep=';').encode('utf-8-sig')
            st.download_button(
                label=t["download_btn"],
                data=csv_data,
                file_name="risk_register.csv",
                mime="text/csv"
            )
            
        with btn_col2:
            pdf_data = generate_pdf(filtered_df, t)
            st.download_button(
                label=t["download_pdf_btn"],
                data=pdf_data,
                file_name="risk_report.pdf",
                mime="application/pdf"
            )
