import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# --------------------------------------------------
# CONFIG PAGINA
# --------------------------------------------------

st.set_page_config(
    page_title="Finance | Ricavi Ricorrenti",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: 100%;
        }

        body {
            background-color: #f3f3f3;
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
            margin-bottom: 0.7rem;
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

        .section-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #2a2a2a;
            margin-top: 0.5rem;
            margin-bottom: 0.7rem;
        }

        .kpi-card {
            background-color: white;
            border-radius: 10px;
            padding: 1rem 1.2rem;
            min-height: 105px;
            box-shadow: 0 0 0 1px rgba(0,0,0,0.05);
        }

        .kpi-title {
            font-size: 0.9rem;
            color: #6b6b6b;
            margin-bottom: 0.25rem;
        }

        .kpi-value {
            font-size: 1.75rem;
            color: #2a2a2a;
            font-weight: 700;
        }

        .small-kpi-title {
            font-size: 0.85rem;
            color: #6b6b6b;
            margin-bottom: 0.2rem;
        }

        .small-kpi-value {
            font-size: 1.45rem;
            color: #2a2a2a;
            font-weight: 700;
        }

        .panel-title {
            font-size: 1.05rem;
            color: #3a3a3a;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }

        .small-caption {
            color: #666666;
            font-size: 0.78rem;
            padding-top: 0.2rem;
        }

        div.stButton > button {
            border-radius: 7px;
            border: 1px solid #0099D6;
            font-weight: 700;
            background-color: white;
            color: #0099D6;
            height: 2.6rem;
        }

        div.stButton > button:hover {
            border-color: #f28c00;
            color: #f28c00;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }

        th {
            background-color: #0099D6;
            color: white;
            padding: 0.55rem;
            text-align: right;
            font-weight: 700;
        }

        th:first-child {
            text-align: left;
        }

        td {
            padding: 0.55rem;
            border-bottom: 1px solid #dddddd;
            text-align: right;
            color: #222222;
        }

        td:first-child {
            text-align: left;
            background-color: #e6e6e6;
            font-weight: 600;
        }

        tr.total-row td {
            background-color: #d9d9d9;
            font-weight: 800;
        }

        .arpu-table {
            max-width: 420px;
        }

        .stPlotlyChart {
            background-color: white;
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
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
# DATI MOCK
# --------------------------------------------------

months = [
    "2025 Apr", "2025 Mag", "2025 Giu", "2025 Lug",
    "2025 Ago", "2025 Set", "2025 Ott", "2025 Nov",
    "2025 Dic", "2026 Gen", "2026 Feb", "2026 Mar"
]

retail = np.array([16.30, 16.50, 16.45, 16.47, 16.38, 16.60, 16.44, 16.34, 16.26, 16.18, 16.32, 16.30])
wholesale = np.array([2.94, 2.80, 2.81, 2.79, 2.76, 2.77, 2.80, 2.84, 2.80, 2.76, 2.74, 2.70])
totale = retail + wholesale

arpu_retail = np.array([26.50, 26.50, 26.40, 26.60, 26.50, 26.50, 26.50, 26.50, 26.50, 26.50, 26.50, 26.45])
arpu_wholesale = np.array([48.80, 48.90, 48.80, 48.90, 48.80, 48.80, 48.70, 48.80, 48.80, 48.90, 48.80, 48.86])
arpu_totale = np.array([28.20, 28.20, 28.20, 28.20, 28.20, 28.30, 28.20, 28.20, 28.20, 28.20, 28.20, 28.29])

df_month = pd.DataFrame(
    {
        "Mese": months,
        "Retail": retail,
        "Wholesale": wholesale,
        "Totale": totale,
        "ARPU Retail": arpu_retail,
        "ARPU Wholesale": arpu_wholesale,
        "ARPU Totale": arpu_totale,
    }
)


# --------------------------------------------------
# FUNZIONI KPI
# --------------------------------------------------

def sparkline(values):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=values,
            mode="lines",
            fill="tozeroy",
            line=dict(width=2, color="#0067A6"),
            fillcolor="rgba(0, 103, 166, 0.25)",
            hoverinfo="skip"
        )
    )

    fig.update_layout(
        height=65,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    return fig


def kpi_card(title, value, values=None):
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown(
            f"""
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        if values is not None:
            st.plotly_chart(
                sparkline(values),
                use_container_width=True,
                config={"displayModeBar": False}
            )


def double_kpi_card(title_1, value_1, title_2, value_2):
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            f"""
            <div class="small-kpi-title">{title_1}</div>
            <div class="small-kpi-value">{value_1}</div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="small-kpi-title">{title_2}</div>
            <div class="small-kpi-value">{value_2}</div>
            """,
            unsafe_allow_html=True
        )


# --------------------------------------------------
# FUNZIONI TABELLE
# --------------------------------------------------

def money_table():
    data = [
        ["RETAIL", "345.207", "1.168.215", "1.644.236", "", "", "", "", "16.297.676"],
        ["WHOLESALE", "32.414", "31.063", "28.949", "1.106.147", "1.278.845", "5.654", "61", "2.698.346"],
        ["Totale", "377.622", "1.199.278", "1.673.185", "1.106.147", "1.278.845", "5.654", "61", "18.996.022"],
    ]

    columns = [
        "BU",
        "ail",
        "DigitalPush",
        "Business",
        "SMALL TELCO",
        "TOP TELCO",
        "BIG OLO",
        "",
        "Totale"
    ]

    html = '<table>'
    html += '<thead><tr>'

    for col in columns:
        html += f'<th>{col}</th>'

    html += '</tr></thead>'
    html += '<tbody>'

    for row in data:
        cls = "total-row" if row[0] == "Totale" else ""
        html += f'<tr class="{cls}">'

        for cell in row:
            html += f'<td>{cell}</td>'

        html += '</tr>'

    html += '</tbody></table>'

    st.markdown(html, unsafe_allow_html=True)


def arpu_table():
    data = [
        ["RETAIL", "26,45"],
        ["WHOLESALE", "48,86"],
        ["Totale", "28,29"],
    ]

    columns = ["BU", "ARPU CB"]

    html = '<table class="arpu-table">'
    html += '<thead><tr>'

    for col in columns:
        html += f'<th>{col}</th>'

    html += '</tr></thead>'
    html += '<tbody>'

    for row in data:
        cls = "total-row" if row[0] == "Totale" else ""
        html += f'<tr class="{cls}">'

        for cell in row:
            html += f'<td>{cell}</td>'

        html += '</tr>'

    html += '</tbody></table>'

    st.markdown(html, unsafe_allow_html=True)


# --------------------------------------------------
# FUNZIONI GRAFICI
# --------------------------------------------------

def ricavi_chart(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    df = df.copy()

    # Palette moderna
    colore_retail = "#2563EB"        # blu elettrico
    colore_wholesale = "#00BFA6"     # teal/acqua
    colore_delta = "#E11D48"         # rosso/magenta trend
    colore_testo = "#111827"

    # --------------------------------------------------
    # Conversione in k€
    # --------------------------------------------------

    df["Retail k€"] = df["Retail"] * 1000
    df["Wholesale k€"] = df["Wholesale"] * 1000
    df["Totale k€"] = df["Totale"] * 1000

    df["Delta Totale k€"] = df["Totale k€"] - df["Totale k€"].iloc[0]

    df["Perc Retail"] = df["Retail k€"] / df["Totale k€"] * 100
    df["Perc Wholesale"] = df["Wholesale k€"] / df["Totale k€"] * 100

    retail_text = [f"{v:.0f}%" for v in df["Perc Retail"]]
    wholesale_text = [f"{v:.0f}%" for v in df["Perc Wholesale"]]

    # --------------------------------------------------
    # Barre Retail
    # Percentuale in basso nel primo segmento
    # --------------------------------------------------

    fig.add_trace(
        go.Bar(
            x=df["Mese"],
            y=df["Retail k€"],
            name="Retail",
            marker=dict(
                color=colore_retail,
                line=dict(
                    color="rgba(255,255,255,0.45)",
                    width=1
                )
            ),
            text=retail_text,
            textposition="inside",
            insidetextanchor="start",
            textfont=dict(
                size=18,
                color="white",
                family="Arial"
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Retail: %{y:,.0f}<br>"
                "Quota Retail: %{text}<extra></extra>"
            )
        ),
        secondary_y=False
    )

    # --------------------------------------------------
    # Barre Wholesale
    # --------------------------------------------------

    fig.add_trace(
        go.Bar(
            x=df["Mese"],
            y=df["Wholesale k€"],
            name="Wholesale",
            marker=dict(
                color=colore_wholesale,
                line=dict(
                    color="rgba(255,255,255,0.45)",
                    width=1
                )
            ),
            text=wholesale_text,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(
                size=18,
                color="white",
                family="Arial"
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Wholesale: %{y:,.0f}<br>"
                "Quota Wholesale: %{text}<extra></extra>"
            )
        ),
        secondary_y=False
    )

    # --------------------------------------------------
    # Linea trend: scostamento totale
    # --------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=df["Mese"],
            y=df["Delta Totale k€"],
            name="Scostamento totale vs inizio",
            mode="lines+markers",
            line=dict(
                color=colore_delta,
                width=3.5
            ),
            marker=dict(
                size=10,
                color=colore_delta,
                line=dict(
                    width=2.5,
                    color="white"
                )
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Scostamento totale: %{y:+,.0f}<extra></extra>"
            )
        ),
        secondary_y=True
    )

    # --------------------------------------------------
    # Totale sopra ogni istogramma
    # Ancora più alto sopra le barre
    # --------------------------------------------------

    for _, row in df.iterrows():
        fig.add_annotation(
            x=row["Mese"],
            y=row["Totale k€"] + 1800,
            text=f"<b>{row['Totale k€']:,.0f}</b>".replace(",", "."),
            showarrow=False,
            font=dict(
                size=22,
                color=colore_testo,
                family="Arial Black"
            ),
            yref="y1"
        )

    # --------------------------------------------------
    # Etichette rosse del delta
    # --------------------------------------------------

    for _, row in df.iterrows():
        delta_value = row["Delta Totale k€"]

        fig.add_annotation(
            x=row["Mese"],
            y=delta_value,
            yref="y2",
            text=f"<b>{delta_value:+,.0f}</b>".replace(",", "."),
            showarrow=False,
            font=dict(
                size=14,
                color=colore_delta,
                family="Arial Black"
            ),
            bgcolor="rgba(255,255,255,0.96)",
            bordercolor=colore_delta,
            borderwidth=1,
            borderpad=5,
            yshift=24 if delta_value >= 0 else -24
        )

    # --------------------------------------------------
    # Layout
    # --------------------------------------------------

    fig.update_layout(
        barmode="stack",
        height=610,
        margin=dict(l=10, r=25, t=110, b=105),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="left",
            x=0,
            font=dict(size=13)
        ),

        hovermode="x unified",

        paper_bgcolor="white",
        plot_bgcolor="white",

        uniformtext=dict(
            mode="show",
            minsize=14
        )
    )

    # --------------------------------------------------
    # Asse X più leggibile
    # --------------------------------------------------

    fig.update_xaxes(
        tickangle=-25,
        tickfont=dict(
            size=15,
            color="#111827",
            family="Arial"
        ),
        showline=False,
        showgrid=False,
        zeroline=False,
        automargin=True
    )

    # --------------------------------------------------
    # Asse Y ricavi nascosto
    # Più spazio superiore per i totaloni
    # --------------------------------------------------

    fig.update_yaxes(
        visible=False,
        showgrid=False,
        zeroline=False,
        range=[0, max(df["Totale k€"]) + 6800],
        secondary_y=False
    )

    # --------------------------------------------------
    # Asse Y delta nascosto
    # Via di mezzo: evita sovrapposizioni ma non schiaccia troppo la linea
    # --------------------------------------------------

    delta_min = df["Delta Totale k€"].min()
    delta_max = df["Delta Totale k€"].max()
    delta_abs = max(abs(delta_min), abs(delta_max), 100)

    fig.update_yaxes(
    visible=False,
    showgrid=False,
    zeroline=False,
    range=[
        delta_min - delta_abs * 2,
        delta_max + delta_abs * 2
    ],
    secondary_y=True
    )
    
    return fig




def arpu_chart(df):
    fig = go.Figure()

    df = df.copy()

    # Stessa palette del grafico Ricavi
    colore_retail = "#2563EB"        # blu elettrico
    colore_wholesale = "#00BFA6"     # teal/acqua
    colore_totale = "#E11D48"        # rosso/magenta
    colore_testo = "#111827"

    # Formattazione italiana con virgola decimale
    def fmt_decimal(value, decimals=1):
        return f"{value:.{decimals}f}".replace(".", ",")

    retail_text = [fmt_decimal(v, 1) for v in df["ARPU Retail"]]
    wholesale_text = [fmt_decimal(v, 1) for v in df["ARPU Wholesale"]]
    totale_text = [fmt_decimal(v, 1) for v in df["ARPU Totale"]]

    # --------------------------------------------------
    # Barre Retail
    # --------------------------------------------------

    fig.add_trace(
        go.Bar(
            x=df["Mese"],
            y=df["ARPU Retail"],
            name="Retail",
            marker=dict(
                color=colore_retail,
                line=dict(
                    color="rgba(255,255,255,0.45)",
                    width=1
                )
            ),
            text=retail_text,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(
                size=17,
                color="white",
                family="Arial"
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "ARPU Retail: %{text}<extra></extra>"
            )
        )
    )

    # --------------------------------------------------
    # Barre Wholesale
    # --------------------------------------------------

    fig.add_trace(
        go.Bar(
            x=df["Mese"],
            y=df["ARPU Wholesale"],
            name="Wholesale",
            marker=dict(
                color=colore_wholesale,
                line=dict(
                    color="rgba(255,255,255,0.45)",
                    width=1
                )
            ),
            text=wholesale_text,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(
                size=17,
                color="white",
                family="Arial"
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "ARPU Wholesale: %{text}<extra></extra>"
            )
        )
    )

    # --------------------------------------------------
    # Linea Totale ARPU
    # --------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=df["Mese"],
            y=df["ARPU Totale"],
            name="Media",
            mode="lines+markers",
            line=dict(
                color=colore_totale,
                width=3.5
            ),
            marker=dict(
                size=10,
                color=colore_totale,
                line=dict(
                    width=2.5,
                    color="white"
                )
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "ARPU Totale: %{y:.1f}<extra></extra>"
            )
        )
    )

    # --------------------------------------------------
    # Etichette della linea Totale
    # Con sfondo bianco per non confondersi con le barre
    # --------------------------------------------------

    for _, row in df.iterrows():
        fig.add_annotation(
            x=row["Mese"],
            y=row["ARPU Totale"],
            text=f"<b>{fmt_decimal(row['ARPU Totale'], 1)}</b>",
            showarrow=False,
            font=dict(
                size=14,
                color=colore_totale,
                family="Arial Black"
            ),
            bgcolor="rgba(255,255,255,0.96)",
            bordercolor=colore_totale,
            borderwidth=1,
            borderpad=5,
            yshift=24
        )

   

    # --------------------------------------------------
    # Layout
    # --------------------------------------------------

    fig.update_layout(
        barmode="group",
        height=600,
        margin=dict(l=10, r=25, t=100, b=105),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="left",
            x=0,
            font=dict(
                size=13,
                color=colore_testo,
                family="Arial"
            )
        ),

        hovermode="x unified",

        paper_bgcolor="white",
        plot_bgcolor="white",

        uniformtext=dict(
            mode="show",
            minsize=13
        )
    )

    # --------------------------------------------------
    # Asse X più leggibile
    # --------------------------------------------------

    fig.update_xaxes(
        tickangle=-25,
        tickfont=dict(
            size=15,
            color=colore_testo,
            family="Arial"
        ),
        showline=False,
        showgrid=False,
        zeroline=False,
        automargin=True
    )

    # --------------------------------------------------
    # Asse Y nascosto, ma con spazio sopra
    # --------------------------------------------------

    valore_max = max(
        df["ARPU Retail"].max(),
        df["ARPU Wholesale"].max(),
        df["ARPU Totale"].max()
    )

    fig.update_yaxes(
        visible=False,
        showgrid=False,
        zeroline=False,
        range=[0, valore_max + 14]
    )

    return fig


# --------------------------------------------------
# STATO PAGINA
# --------------------------------------------------

if "pagina_dashboard" not in st.session_state:
    st.session_state.pagina_dashboard = "Ricavi"


# --------------------------------------------------
# HEADER
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


# --------------------------------------------------
# BOTTONI NAVIGAZIONE
# --------------------------------------------------

nav1, nav2, nav_space = st.columns([1, 1, 6])

with nav1:
    if st.button("Pagina Ricavi", use_container_width=True):
        st.session_state.pagina_dashboard = "Ricavi"

with nav2:
    if st.button("Pagina ARPU", use_container_width=True):
        st.session_state.pagina_dashboard = "ARPU"


st.markdown("<br>", unsafe_allow_html=True)


# --------------------------------------------------
# PAGINA 1 - RICAVI
# --------------------------------------------------

if st.session_state.pagina_dashboard == "Ricavi":

    st.markdown('<div class="section-title">Ricavi</div>', unsafe_allow_html=True)

    kpi_col1, kpi_col2 = st.columns(2)

    with kpi_col1:
        with st.container(border=True):
            kpi_card("Ricavi Ricorrenti", "19,00Mln", totale)

    with kpi_col2:
        with st.container(border=True):
            double_kpi_card("Wholesale", "2,70Mln", "Retail", "16,30Mln")

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        head1, head2, head3 = st.columns([2.2, 0.7, 1])

        with head1:
            st.markdown(
                '<div class="panel-title">Dettaglio Ricavi Ricorrenti</div>',
                unsafe_allow_html=True
            )

        with head2:
            st.markdown(
                '<div class="small-caption">Righe: BU</div>',
                unsafe_allow_html=True
            )

        with head3:
            st.markdown(
                '<div class="small-caption">Colonne: Canale</div>',
                unsafe_allow_html=True
            )

        money_table()

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(
            '<div class="panel-title">Ricavi per BU (k€)</div>',
            unsafe_allow_html=True
        )

        st.plotly_chart(
            ricavi_chart(df_month),
            use_container_width=True,
            config={"displayModeBar": False}
        )


# --------------------------------------------------
# PAGINA 2 - ARPU
# --------------------------------------------------

else:

    st.markdown('<div class="section-title">ARPU</div>', unsafe_allow_html=True)

    kpi_col1, kpi_col2 = st.columns(2)

    with kpi_col1:
        with st.container(border=True):
            kpi_card("ARPU CB Netta", "28,29", arpu_totale)

    with kpi_col2:
        with st.container(border=True):
            double_kpi_card("Wholesale", "48,86", "Retail", "26,45")

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        head1, head2, head3 = st.columns([2.2, 0.7, 1])

        with head1:
            st.markdown(
                '<div class="panel-title">Dettaglio ARPU CB Netta</div>',
                unsafe_allow_html=True
            )

        with head2:
            st.markdown(
                '<div class="small-caption">Righe: BU</div>',
                unsafe_allow_html=True
            )

        with head3:
            st.markdown(
                '<div class="small-caption">Colonne: Nessuna selezione</div>',
                unsafe_allow_html=True
            )

        arpu_table()

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        top1, top2 = st.columns([2.5, 1])

        with top1:
            st.markdown(
                '<div class="panel-title">ARPU CB Netta per Mese (€)</div>',
                unsafe_allow_html=True
            )

        with top2:
            st.markdown(
                '<div class="small-caption">○ Geografica &nbsp;&nbsp; ● Temporale</div>',
                unsafe_allow_html=True
            )

        st.plotly_chart(
            arpu_chart(df_month),
            use_container_width=True,
            config={"displayModeBar": False}
        )
