import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Finance | Ricavi Ricorrenti",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }

    [data-testid="stSidebar"] {
        background-color: #00A3D9;
        padding-top: 0.5rem;
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    [data-testid="stSidebar"] .stSelectbox label {
        color: white;
        font-weight: 700;
        font-size: 0.75rem;
    }

    [data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #333333 !important;
    }

    .logo-box {
        text-align: center;
        font-size: 3.2rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
    }

    .orange-button {
        background-color: #f28c00;
        border-radius: 5px;
        padding: 0.55rem;
        text-align: center;
        color: white;
        font-weight: 700;
        margin: 0.35rem 0;
    }

    .white-button {
        background-color: white;
        border-radius: 5px;
        padding: 0.55rem;
        text-align: center;
        color: #00A3D9 !important;
        font-weight: 700;
        margin: 0.35rem 0 1rem 0;
    }

    .title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .dashboard-title {
        font-size: 1.7rem;
        font-weight: 700;
        color: #2a2a2a;
    }

    .last-update {
        font-size: 0.8rem;
        color: #111111;
        font-weight: 600;
    }

    .card {
        background-color: white;
        border-radius: 8px;
        padding: 0.85rem 1rem;
        box-shadow: 0 0 0 1px rgba(0,0,0,0.03);
        height: 92px;
    }

    .card-title {
        font-size: 0.85rem;
        color: #6b6b6b;
        margin-bottom: 0.25rem;
    }

    .card-value {
        font-size: 1.45rem;
        color: #2a2a2a;
        font-weight: 600;
    }

    .panel {
        background-color: white;
        border-radius: 8px;
        padding: 0.65rem;
        height: 100%;
        box-shadow: 0 0 0 1px rgba(0,0,0,0.03);
    }

    .panel-title {
        font-size: 1rem;
        color: #3a3a3a;
        font-weight: 500;
        margin-bottom: 0.4rem;
    }

    .small-caption {
        color: #666666;
        font-size: 0.75rem;
    }

    body {
        background-color: #f3f3f3;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 1rem;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.78rem;
    }

    th {
        background-color: #0099D6;
        color: white;
        padding: 0.35rem;
        text-align: right;
    }

    th:first-child {
        text-align: left;
    }

    td {
        padding: 0.35rem;
        border-bottom: 1px solid #dddddd;
        text-align: right;
        color: #222222;
    }

    td:first-child {
        text-align: left;
        background-color: #e6e6e6;
    }

    tr.total-row td {
        background-color: #d9d9d9;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.markdown('<div class="logo-box">ė</div>', unsafe_allow_html=True)
    st.markdown('<div class="orange-button">Ricavi Ricorrenti</div>', unsafe_allow_html=True)
    st.markdown('<div class="white-button">Ricavi One-Off</div>', unsafe_allow_html=True)

    fiscal_year = st.selectbox("Fiscal Year", ["2026", "2025", "2024"])
    month = st.selectbox("Month", ["Marzo", "Febbraio", "Gennaio", "Dicembre"])
    bu = st.selectbox("BU", ["Tutte", "Retail", "Wholesale"])
    region = st.selectbox("Region", ["Tutte", "Nord", "Centro", "Sud"])
    cluster = st.selectbox("Commercial Cluster", ["Tutte", "Cluster A", "Cluster B"])
    segment = st.selectbox("Segmento", ["Tutte", "Consumer", "Business"])
    canale = st.selectbox("Canale", ["Tutte", "DigitalPush", "Retail", "Wholesale"])
    partner = st.selectbox("Partner", ["Tutte", "Partner A", "Partner B"])
    tecnologia = st.selectbox("Tecnologia", ["Tutte", "Fibra", "Mobile", "FWA"])


# --------------------------------------------------
# Mock data
# --------------------------------------------------

months = [
    "2025 Apr", "2025 Mag", "2025 Giu", "2025 Lug",
    "2025 Ago", "2025 Set", "2025 Ott", "2025 Nov",
    "2025 Dic", "2026 Gen", "2026 Feb", "2026 Mar"
]

retail = np.array([16.30, 16.50, 16.45, 16.47, 16.38, 16.60, 16.44, 16.34, 16.26, 16.18, 16.32, 16.30])
wholesale = np.array([2.94, 2.80, 2.81, 2.79, 2.76, 2.77, 2.80, 2.84, 2.80, 2.76, 2.74, 2.70])
totale = retail + wholesale

arpu_retail = np.array([26.5, 26.5, 26.4, 26.6, 26.5, 26.5, 26.5, 26.5, 26.5, 26.5, 26.5, 26.45])
arpu_wholesale = np.array([48.8, 48.9, 48.8, 48.9, 48.8, 48.8, 48.7, 48.8, 48.8, 48.9, 48.8, 48.86])
arpu_totale = np.array([28.2, 28.2, 28.2, 28.2, 28.2, 28.3, 28.2, 28.2, 28.2, 28.2, 28.2, 28.29])

df_month = pd.DataFrame({
    "Mese": months,
    "Retail": retail,
    "Wholesale": wholesale,
    "Totale": totale,
    "ARPU Retail": arpu_retail,
    "ARPU Wholesale": arpu_wholesale,
    "ARPU Totale": arpu_totale
})


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def sparkline(values):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=values,
        mode="lines",
        fill="tozeroy",
        line=dict(width=2),
        hoverinfo="skip"
    ))
    fig.update_layout(
        height=55,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )
    return fig


def kpi_card(title, value, values=None):
    left, right = st.columns([1.15, 0.85])

    with left:
        st.markdown(
            f"""
            <div class="card-title">{title}</div>
            <div class="card-value">{value}</div>
            """,
            unsafe_allow_html=True
        )

    with right:
        if values is not None:
            st.plotly_chart(
                sparkline(values),
                use_container_width=True,
                config={"displayModeBar": False}
            )


def simple_card(title_1, value_1, title_2, value_2):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"""
            <div class="card-title">{title_1}</div>
            <div class="card-value">{value_1}</div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""
            <div class="card-title">{title_2}</div>
            <div class="card-value">{value_2}</div>
            """,
            unsafe_allow_html=True
        )


def money_table():
    data = [
        ["RETAIL", "345.207", "1.168.215", "1.644.236", "", "", "", "", "16.297.676"],
        ["WHOLESALE", "32.414", "31.063", "28.949", "1.106.147", "1.278.845", "5.654", "61", "2.698.346"],
        ["Totale", "377.622", "1.199.278", "1.673.185", "1.106.147", "1.278.845", "5.654", "61", "18.996.022"],
    ]

    columns = [
        "BU", "ail", "DigitalPush", "Business", "SMALL TELCO",
        "TOP TELCO", "BIG OLO", "", "Totale"
    ]

    html = "<table><thead><tr>"
    for col in columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"

    for row in data:
        cls = "total-row" if row[0] == "Totale" else ""
        html += f"<tr class='{cls}'>"
        for cell in row:
            html += f"<td>{cell}</td>"
        html += "</tr>"

    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)


def arpu_table():
    data = [
        ("RETAIL", "26,45"),
        ("WHOLESALE", "48,86"),
        ("Totale", "28,29"),
    ]

    html = '<table class="arpu-table">'
    html += '<thead><tr><th>BU</th><th>ARPU CB</th></tr></thead>'
    html += '<tbody>'

    for bu_name, value in data:
        cls = "total-row" if bu_name == "Totale" else ""
        html += f'<tr class="{cls}"><td>{bu_name}</td><td>{value}</td></tr>'

    html += '</tbody></table>'

    st.markdown(html, unsafe_allow_html=True)
def ricavi_chart(df):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["Mese"],
        y=df["Retail"],
        name="RETAIL",
        text=[f"{v:.0f}..." for v in df["Retail"]],
        textposition="inside"
    ))

    fig.add_trace(go.Bar(
        x=df["Mese"],
        y=df["Wholesale"],
        name="WHOLESALE"
    ))

    fig.update_layout(
        barmode="stack",
        height=285,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        yaxis=dict(visible=False),
        xaxis=dict(tickfont=dict(size=10)),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    for i, total_value in enumerate(df["Totale"]):
        fig.add_annotation(
            x=df["Mese"].iloc[i],
            y=total_value + 0.25,
            text=f"{total_value:.3f}",
            showarrow=False,
            font=dict(size=10, color="#666666")
        )

    return fig


def arpu_chart(df):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["Mese"],
        y=df["ARPU Retail"],
        name="Retail"
    ))

    fig.add_trace(go.Bar(
        x=df["Mese"],
        y=df["ARPU Wholesale"],
        name="Wholesale"
    ))

    fig.add_trace(go.Scatter(
        x=df["Mese"],
        y=df["ARPU Totale"],
        name="Totale",
        mode="lines+markers",
        line=dict(width=3)
    ))

    fig.update_layout(
        height=285,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        yaxis=dict(visible=False),
        xaxis=dict(tickfont=dict(size=10)),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    return fig


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <div class="title-row">
        <div class="dashboard-title">Finance | Ricavi Ricorrenti</div>
        <div class="last-update">Last Update: 12/06/2026</div>
    </div>
    """,
    unsafe_allow_html=True
)

radio_col_1, radio_col_2 = st.columns([8, 1])
with radio_col_2:
    cb_type = st.radio(
        "",
        ["CB Netta", "CB Totale"],
        horizontal=True,
        label_visibility="collapsed"
    )


# --------------------------------------------------
# KPI row
# --------------------------------------------------

kpi1, kpi2, kpi3, kpi4 = st.columns([1.35, 1.35, 1.35, 1.35])

with kpi1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    kpi_card("Ricavi Ricorrenti", "19,00Mln", totale)
    st.markdown('</div>', unsafe_allow_html=True)

with kpi2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    simple_card("Wholesale", "2,70Mln", "Retail", "16,30Mln")
    st.markdown('</div>', unsafe_allow_html=True)

with kpi3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    kpi_card("ARPU CB Netta", "28,29", arpu_totale)
    st.markdown('</div>', unsafe_allow_html=True)

with kpi4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    simple_card("Wholesale", "48,86", "Retail", "26,45")
    st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# Top detail row
# --------------------------------------------------

left_top, right_top = st.columns([1.08, 1.08])

with left_top:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.3, 0.55, 0.8])
    with c1:
        st.markdown('<div class="panel-title">Dettaglio Ricavi Ricorrenti</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="small-caption">Righe: &nbsp; BU</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="small-caption">Colonne: &nbsp; Canale</div>', unsafe_allow_html=True)

    money_table()

    st.markdown(
        """
        <div style="height:118px;"></div>
        <div style="height:6px;background:#a8a8a8;border-radius:4px;margin:0 0.3rem;"></div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

with right_top:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.4, 0.55, 0.9])
    with c1:
        st.markdown('<div class="panel-title">Dettaglio ARPU CB Netta</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="small-caption">Righe: &nbsp; BU</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="small-caption">Colonne: &nbsp; Nessuna s...</div>', unsafe_allow_html=True)

    arpu_table()

    st.markdown('<div style="height:170px;"></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# Bottom chart row
# --------------------------------------------------

left_bottom, right_bottom = st.columns([1.08, 1.08])

with left_bottom:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Ricavi per BU (k€)</div>', unsafe_allow_html=True)
    st.plotly_chart(
        ricavi_chart(df_month),
        use_container_width=True,
        config={"displayModeBar": False}
    )
    st.markdown('</div>', unsafe_allow_html=True)

with right_bottom:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    c1, c2 = st.columns([1.5, 0.5])
    with c1:
        st.markdown('<div class="panel-title">ARPU CB Netta per Mese</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(
            '<div class="small-caption">○ Geografica &nbsp;&nbsp; ● Temporale</div>',
            unsafe_allow_html=True
        )

    st.plotly_chart(
        arpu_chart(df_month),
        use_container_width=True,
        config={"displayModeBar": False}
    )

    st.markdown('</div>', unsafe_allow_html=True)
