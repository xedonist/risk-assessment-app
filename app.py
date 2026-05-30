import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import tempfile
import os

try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False

if 'risks' not in st.session_state:
    st.session_state.risks = []

input_keys = ['in_asset', 'in_threat', 'in_vuln', 'in_controls']
for key in input_keys:
    if key not in st.session_state:
        st.session_state[key] = ""
if 'in_prob' not in st.session_state: st.session_state.in_prob = 1
if 'in_imp' not in st.session_state: st.session_state.in_imp = 1
if 'in_treat' not in st.session_state: st.session_state.in_treat = "Redukcja"

translations = {
    "EN": {
        "title": "Information Security Risk Assessment",
        "method_title": "Assessment Method",
        "method_1": "Multiplicative (P * I)",
        "method_2": "Additive (P + I)",
        "scale_title": "Scale Max Value (e.g., 5 or 10)",
        "weight_p": "Prob. Weight",
        "weight_i": "Impact Weight",
        "sidebar_title": "Add New Risk",
        "asset": "Asset",
        "threat": "Threat",
        "vulnerability": "Vulnerability",
        "controls": "Controls",
        "probability": "Probability",
        "impact": "Impact",
        "treatment": "Treatment Strategy",
        "treat_red": "Reduction",
        "treat_acc": "Acceptance",
        "treat_trans": "Transfer",
        "treat_avoid": "Avoidance",
        "add_btn": "Add Risk to Register",
        "req_warning": "Fill Asset, Threat, and Vulnerability.",
        "add_success": "Risk added successfully!",
        "settings_title": "Risk Appetite Settings",
        "med_threshold": "Medium Risk Threshold",
        "high_threshold": "High Risk Threshold",
        "upload_csv": "Upload Project (CSV)",
        "import_btn": "Import CSV",
        "upload_error": "Error loading file or invalid format.",
        "low": "Low",
        "medium": "Medium",
        "high": "High",
        "matrix_title": "Risk Matrix",
        "download_csv": "Download CSV",
        "download_pdf": "Download PDF Report",
        "risk_level": "Risk Level",
        "live_risk": "Calculated Risk Level:",
        "category": "Category",
        "table_title": "Risk Register (Double-click to edit, select row & press DEL to delete)",
        "filter": "Filter by Category",
        "all": "All",
        "kpi_total": "Total Risks",
        "kpi_high": "High",
        "kpi_medium": "Medium",
        "kpi_low": "Low",
        "no_data": "No risks added yet. Use the sidebar to add entries."
    },
    "PL": {
        "title": "Ocena Ryzyka Bezpieczeństwa Informacji",
        "method_title": "Wybór metody szacowania",
        "method_1": "Ilościowo-Jakościowa (P * S)",
        "method_2": "Addytywna (P + S)",
        "scale_title": "Max Skala (np. 5 lub 10)",
        "weight_p": "Waga Prawdop.",
        "weight_i": "Waga Skutków",
        "sidebar_title": "Dodaj Nowe Ryzyko",
        "asset": "Aktywo",
        "threat": "Zagrożenie",
        "vulnerability": "Podatność",
        "controls": "Zabezpieczenia",
        "probability": "Prawdopodobieństwo",
        "impact": "Skutki",
        "treatment": "Postępowanie z ryzykiem",
        "treat_red": "Redukcja",
        "treat_acc": "Akceptacja",
        "treat_trans": "Przeniesienie",
        "treat_avoid": "Unikanie",
        "add_btn": "Dodaj do Rejestru",
        "req_warning": "Wypełnij Aktywo, Zagrożenie i Podatność.",
        "add_success": "Pomyślnie dodano ryzyko!",
        "settings_title": "Kryteria Akceptacji",
        "med_threshold": "Próg Średniego Ryzyka",
        "high_threshold": "Próg Wysokiego Ryzyka",
        "upload_csv": "Wgraj Projekt (CSV)",
        "import_btn": "Importuj CSV",
        "upload_error": "Błąd ładowania pliku.",
        "low": "Niski",
        "medium": "Średni",
        "high": "Wysoki",
        "matrix_title": "Macierz Ryzyka",
        "download_csv": "Pobierz CSV",
        "download_pdf": "Pobierz Raport PDF",
        "risk_level": "Poziom",
        "live_risk": "Wyliczony poziom ryzyka:",
        "category": "Kategoria",
        "table_title": "Rejestr Ryzyk (Kliknij dwukrotnie by edytować, zaznacz i wciśnij DEL by usunąć)",
        "filter": "Filtruj po Kategorii",
        "all": "Wszystkie",
        "kpi_total": "Całkowita liczba",
        "kpi_high": "Wysokie",
        "kpi_medium": "Średnie",
        "kpi_low": "Niskie",
        "no_data": "Brak danych. Skorzystaj z panelu bocznego, aby dodać ryzyko."
    }
}

st.set_page_config(page_title="Risk Assessment App", layout="wide")

lang = st.sidebar.radio("Language / Język", ["PL", "EN"], horizontal=True)
t = translations[lang]
treatment_options = [t["treat_red"], t["treat_acc"], t["treat_trans"], t["treat_avoid"]]

def get_category(score, med_t, high_t):
    if score < med_t: return t["low"]
    elif score < high_t: return t["medium"]
    return t["high"]

def clean_text_for_pdf(text):
    if not isinstance(text, str): return str(text)
    trans = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ")
    return text.translate(trans).encode('latin-1', 'replace').decode('latin-1')

st.sidebar.header(t["method_title"])
selected_method = st.sidebar.selectbox("", [t["method_1"], t["method_2"]], label_visibility="collapsed")
st.sidebar.divider()

st.sidebar.header(t["settings_title"])
max_scale = st.sidebar.number_input(t["scale_title"], min_value=3, max_value=20, value=5)

col1, col2 = st.sidebar.columns(2)
weight_p = col1.number_input(t["weight_p"], min_value=0.1, value=1.0, step=0.1)
weight_i = col2.number_input(t["weight_i"], min_value=0.1, value=1.0, step=0.1)

if selected_method == t["method_1"]:
    max_possible_score = (max_scale * weight_p) * (max_scale * weight_i)
else:
    max_possible_score = (max_scale * weight_p) + (max_scale * weight_i)

default_med = min(float(max_scale), float(max_possible_score))
default_high = max(default_med, min(float(max_scale * 3), float(max_possible_score)))

med_thresh = st.sidebar.number_input(t["med_threshold"], min_value=1.0, max_value=float(max_possible_score), value=default_med)
high_thresh = st.sidebar.number_input(t["high_threshold"], min_value=float(med_thresh), max_value=float(max_possible_score), value=default_high)
st.sidebar.divider()

st.sidebar.header(t["sidebar_title"])

st.sidebar.text_input(t["asset"] + " *", key="in_asset")
st.sidebar.text_input(t["threat"] + " *", key="in_threat")
st.sidebar.text_input(t["vulnerability"] + " *", key="in_vuln")
st.sidebar.text_input(t["controls"], key="in_controls")

st.sidebar.slider(f"{t['probability']} (1-{int(max_scale)})", 1, int(max_scale), key="in_prob")
st.sidebar.slider(f"{t['impact']} (1-{int(max_scale)})", 1, int(max_scale), key="in_imp")

if selected_method == t["method_1"]:
    current_risk_score = (st.session_state.in_prob * weight_p) * (st.session_state.in_imp * weight_i)
else:
    current_risk_score = (st.session_state.in_prob * weight_p) + (st.session_state.in_imp * weight_i)

current_risk_score = round(current_risk_score, 2)
current_category = get_category(current_risk_score, med_thresh, high_thresh)

color = "green" if current_category == t["low"] else "orange" if current_category == t["medium"] else "red"
st.sidebar.markdown(f"**{t['live_risk']}** <span style='color:{color}; font-size:18px; font-weight:bold;'>{current_risk_score} ({current_category})</span>", unsafe_allow_html=True)
st.sidebar.write("")

st.sidebar.selectbox(t["treatment"], treatment_options, key="in_treat")

def add_risk_callback():
    if st.session_state.in_asset and st.session_state.in_threat and st.session_state.in_vuln:
        st.session_state.risks.append({
            "asset": st.session_state.in_asset,
            "threat": st.session_state.in_threat,
            "vulnerability": st.session_state.in_vuln,
            "controls": st.session_state.in_controls,
            "probability": st.session_state.in_prob,
            "impact": st.session_state.in_imp,
            "treatment": st.session_state.in_treat
        })
        st.session_state.in_asset = ""
        st.session_state.in_threat = ""
        st.session_state.in_vuln = ""
        st.session_state.in_controls = ""
        st.session_state.in_prob = 1
        st.session_state.in_imp = 1

        st.toast(t["add_success"], icon="✅")
    else:
        st.toast(t["req_warning"], icon="⚠️")

st.sidebar.button(t["add_btn"], on_click=add_risk_callback, type="primary", use_container_width=True)

st.sidebar.divider()

st.sidebar.header(t["upload_csv"])
uploaded_file = st.sidebar.file_uploader("", type=["csv"], label_visibility="collapsed")
if st.sidebar.button(t["import_btn"]) and uploaded_file:
    try:
        import_df = pd.read_csv(uploaded_file, sep=';')

        reverse_map = {}
        for lang_dict in translations.values():
            for k in ["asset", "threat", "vulnerability", "controls", "probability", "impact", "treatment"]:
                if k in lang_dict:
                    reverse_map[lang_dict[k]] = k

        import_df = import_df.rename(columns=reverse_map)
        st.session_state.risks = import_df.to_dict('records')
        st.rerun()
    except Exception:
        st.sidebar.error(t.get("upload_error", "Error"))

st.title(t["title"])

base_cols = ["asset", "threat", "vulnerability", "controls", "probability", "impact", "treatment"]

if not st.session_state.risks:
    st.info(t["no_data"])
    df = pd.DataFrame(columns=base_cols)
else:
    df = pd.DataFrame(st.session_state.risks)

for col in base_cols:
    if col not in df.columns:
        df[col] = ""

df['probability'] = pd.to_numeric(df.get('probability', pd.Series(dtype=int)), errors='coerce').fillna(1).astype(int)
df['impact'] = pd.to_numeric(df.get('impact', pd.Series(dtype=int)), errors='coerce').fillna(1).astype(int)

if selected_method == t["method_1"]:
    df['risk_level'] = (df['probability'] * weight_p) * (df['impact'] * weight_i)
else:
    df['risk_level'] = (df['probability'] * weight_p) + (df['impact'] * weight_i)

df['risk_level'] = df['risk_level'].round(2)
df['category'] = df['risk_level'].apply(lambda x: get_category(x, med_thresh, high_thresh))

if not df.empty:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t["kpi_total"], len(df))
    c2.metric(t["kpi_high"], len(df[df['category'] == t["high"]]))
    c3.metric(t["kpi_medium"], len(df[df['category'] == t["medium"]]))
    c4.metric(t["kpi_low"], len(df[df['category'] == t["low"]]))

st.divider()

st.subheader(t["table_title"])

cat_filter = st.selectbox(t["filter"], [t["all"], t["low"], t["medium"], t["high"]])
display_df = df if cat_filter == t["all"] else df[df['category'] == cat_filter]

col_order = ["asset", "threat", "vulnerability", "controls", "probability", "impact", "risk_level", "category", "treatment"]

edited_df = st.data_editor(
    display_df,
    column_order=col_order,
    column_config={
        "asset": st.column_config.TextColumn(t["asset"], required=True),
        "threat": st.column_config.TextColumn(t["threat"], required=True),
        "vulnerability": st.column_config.TextColumn(t["vulnerability"], required=True),
        "controls": st.column_config.TextColumn(t["controls"]),
        "probability": st.column_config.NumberColumn(t["probability"], min_value=1, max_value=int(max_scale)),
        "impact": st.column_config.NumberColumn(t["impact"], min_value=1, max_value=int(max_scale)),
        "risk_level": st.column_config.NumberColumn(t["risk_level"], disabled=True),
        "category": st.column_config.TextColumn(t["category"], disabled=True),
        "treatment": st.column_config.SelectboxColumn(t["treatment"], options=treatment_options)
    },
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True
)

if 'asset' in edited_df.columns:
    clean_edited = edited_df.dropna(subset=['asset']).fillna("")
else:
    clean_edited = edited_df.fillna("")

for col in base_cols:
    if col not in clean_edited.columns:
        clean_edited[col] = ""

new_state = clean_edited[base_cols].to_dict('records')

if cat_filter == t["all"] and new_state != st.session_state.risks:
    st.session_state.risks = new_state
    st.rerun()

st.divider()

st.subheader(t["matrix_title"])
if not edited_df.empty:
    plot_df = edited_df.copy()
    plot_df['p_jitter'] = plot_df['probability'] + np.random.uniform(-0.15, 0.15, len(plot_df))
    plot_df['i_jitter'] = plot_df['impact'] + np.random.uniform(-0.15, 0.15, len(plot_df))

    fig = px.scatter(
        plot_df, x='i_jitter', y='p_jitter', color='category', hover_name=plot_df.get('asset', 'Item'),
        hover_data={'i_jitter': False, 'p_jitter': False, 'probability': True, 'impact': True, 'risk_level': True},
        color_discrete_map={t["low"]: "green", t["medium"]: "gold", t["high"]: "crimson"}, size_max=15
    )
    fig.update_layout(xaxis_title=t["impact"], yaxis_title=t["probability"], xaxis_range=[0.5, max_scale + 0.5], yaxis_range=[0.5, max_scale + 0.5])
    fig.update_traces(marker=dict(size=12, line=dict(width=1, color='black')))
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    export_df = edited_df[col_order].rename(columns={k: t.get(k, k) for k in col_order})

    col_export1, col_export2 = st.columns(2)
    col_export1.download_button(
        t["download_csv"],
        data=export_df.to_csv(index=False, sep=';').encode('utf-8-sig'),
        file_name="risk_register.csv", mime="text/csv"
    )

    if FPDF_AVAILABLE:
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt=clean_text_for_pdf(t["title"]), ln=True, align='C')
        pdf.ln(5)

        pdf.set_font("Arial", 'B', 9)
        col_widths = [50, 50, 50, 25, 30, 65]
        headers = [t["asset"], t["threat"], t["vulnerability"], t["risk_level"], t["category"], t["treatment"]]

        for width, header in zip(col_widths, headers):
            pdf.cell(width, 8, txt=clean_text_for_pdf(header)[:30], border=1, align='C')
        pdf.ln()

        pdf.set_font("Arial", '', 8)
        for _, row in export_df.iterrows():
            pdf.cell(col_widths[0], 8, txt=clean_text_for_pdf(str(row.get(t["asset"], "")))[:35], border=1)
            pdf.cell(col_widths[1], 8, txt=clean_text_for_pdf(str(row.get(t["threat"], "")))[:35], border=1)
            pdf.cell(col_widths[2], 8, txt=clean_text_for_pdf(str(row.get(t["vulnerability"], "")))[:35], border=1)
            pdf.cell(col_widths[3], 8, txt=str(row.get(t["risk_level"], "")), border=1, align='C')
            pdf.cell(col_widths[4], 8, txt=clean_text_for_pdf(str(row.get(t["category"], ""))), border=1, align='C')
            pdf.cell(col_widths[5], 8, txt=clean_text_for_pdf(str(row.get(t["treatment"], "")))[:45], border=1)
            pdf.ln()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf.output(tmp.name)
            with open(tmp.name, "rb") as f:
                pdf_bytes = f.read()
        os.remove(tmp.name)

        col_export2.download_button(t["download_pdf"], data=pdf_bytes, file_name="risk_report.pdf", mime="application/pdf")
    else:
        col_export2.error("Do eksportu PDF wymagana jest biblioteka FPDF. Wpisz w terminalu: pip install fpdf")