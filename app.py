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
            background-color: #F28C00;
            border-radius: 5px;
            padding: 0.70rem;
            text-align: center;
            color: white;
            font-weight: 700;
            margin: 0.35rem 0;
        }

        .white-button {
            background-color: white;
            border-radius: 5px;
            padding: 0.70rem;
            text-align: center;
            color: #0099D6 !important;
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

        /* --------------------------------------------------
           BOTTONI PAGINA RICAVI / PAGINA ARPU
           Stile coerente con Ricavi Ricorrenti / Ricavi One-Off
        -------------------------------------------------- */

        div.stButton > button {
            border-radius: 6px;
            border: none;
            font-weight: 700;
            font-size: 15px;
            height: 3rem;
            box-shadow: none !important;
        }

        div.stButton > button[kind="primary"] {
            background-color: #F28C00 !important;
            color: white !important;
            border: 1px solid #F28C00 !important;
        }

        div.stButton > button[kind="primary"]:hover {
            background-color: #E07F00 !important;
            color: white !important;
            border: 1px solid #E07F00 !important;
        }

        div.stButton > button[kind="secondary"] {
            background-color: white !important;
            color: #0099D6 !important;
            border: 1px solid white !important;
        }

        div.stButton > button[kind="secondary"]:hover {
            background-color: #F7FBFD !important;
            color: #007FB3 !important;
            border: 1px solid white !important;
        }

        div.stButton > button:focus {
            box-shadow: none !important;
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
        ["RETAIL", "163.596.119", "20.737.160", "12.203.216", "4.663.997", "41.853", "201.242.345"],
        ["WHOLESALE", "4.413.669", "4.160.792", "7.863.751", "12.412.962", "2.964", "28.854.139"],
        ["Totale", "168.009.789", "24.897.952", "20.066.968", "17.076.959", "44.817", "230.096.485"],
    ]

    columns = [
        "BU",
        "CONSUMER",
        "SOHO",
        "BUSINESS",
        "TOP",
        "STAGIONALE",
        "Totale"
    ]

    html = """
    <style>
        .ricavi-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95rem;
        }

        .ricavi-table th {
            background-color: #0099D6;
            color: white;
            padding: 0.65rem;
            text-align: right;
            font-weight: 800;
            border: 1px solid rgba(255,255,255,0.15);
        }

        .ricavi-table th:first-child {
            text-align: left;
        }

        .ricavi-table td {
            padding: 0.60rem;
            border: 1px solid #e5e5e5;
            text-align: right;
            color: #222222;
            background-color: white;
            font-weight: 500;
        }

        .ricavi-table td:first-child {
            text-align: left;
            background-color: #EFEFEF;
            font-weight: 700;
        }

        .ricavi-table td.total-col {
            background-color: #D9D9D9;
            font-weight: 800;
        }

        .ricavi-table tr.total-row td {
            background-color: #CFCFCF;
            font-weight: 900;
        }

        .ricavi-table tr.total-row td:first-child {
            background-color: #CFCFCF;
        }

        .ricavi-table tr.total-row td.total-col {
            background-color: #CFCFCF;
            font-weight: 900;
        }
    </style>
    """

    html += '<table class="ricavi-table">'
    html += '<thead><tr>'

    for col in columns:
        html += f'<th>{col}</th>'

    html += '</tr></thead>'
    html += '<tbody>'

    for row in data:
        row_class = "total-row" if row[0] == "Totale" else ""
        html += f'<tr class="{row_class}">'

        for i, cell in enumerate(row):
            cell_class = "total-col" if i == len(row) - 1 else ""
            html += f'<td class="{cell_class}">{cell}</td>'

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

# --------------------------------------------------
# Curva FY precedente
# Solo linea grigia tratteggiata, senza punti e senza box.
# La curva viene alzata visivamente sopra i totaloni.
# --------------------------------------------------
def ricavi_chart(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    df = df.copy()

    # Colori stile grafico iniziale
    colore_retail = "#005B96"        # blu scuro
    colore_wholesale = "#F2C94C"     # giallo chiaro
    colore_fy_prec = "#8A8F98"       # grigio FY precedente
    colore_testo = "#111827"

    # --------------------------------------------------
    # Conversione in k€
    # --------------------------------------------------

    df["Retail k€"] = df["Retail"] * 1000
    df["Wholesale k€"] = df["Wholesale"] * 1000
    df["Totale k€"] = df["Totale"] * 1000

    # --------------------------------------------------
    # Totale stesso mese FY precedente
    # In produzione questa colonna dovrà arrivare dal dataset.
    # Se non trova il dato reale, usa valori mock temporanei.
    # --------------------------------------------------

    if "Totale FY Prec k€" in df.columns:
        df["Totale FY Prec k€"] = df["Totale FY Prec k€"]

    elif "Totale FY Prec" in df.columns:
        df["Totale FY Prec k€"] = df["Totale FY Prec"] * 1000

    elif "Totale FY precedente" in df.columns:
        df["Totale FY Prec k€"] = df["Totale FY precedente"] * 1000

    else:
        # MOCK temporaneo: da sostituire con dato reale FY precedente
        df["Totale FY Prec k€"] = df["Totale k€"] * np.array(
            [1.012, 1.006, 1.000, 0.995, 1.004, 0.998, 1.010, 1.006, 1.002, 0.997, 1.005, 1.004]
        )

    # --------------------------------------------------
    # Variazione % FY corrente vs FY precedente
    # Formula: (corrente - precedente) / precedente
    # --------------------------------------------------

    df["Delta % vs FY Prec"] = (
        (df["Totale k€"] - df["Totale FY Prec k€"])
        / df["Totale FY Prec k€"]
        * 100
    )

    # --------------------------------------------------
    # Testi assoluti dentro le barre
    # --------------------------------------------------

    retail_text = [
        f"{v:,.0f}".replace(",", ".")
        for v in df["Retail k€"]
    ]

    wholesale_text = [
        f"{v:,.0f}".replace(",", ".")
        for v in df["Wholesale k€"]
    ]

    # --------------------------------------------------
    # Barre Retail FY corrente
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
            insidetextanchor="middle",
            textfont=dict(
                size=15,
                color="white",
                family="Arial"
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Retail: %{y:,.0f}<extra></extra>"
            )
        ),
        secondary_y=False
    )

    # --------------------------------------------------
    # Barre Wholesale FY corrente
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
                size=13,
                color="#111827",
                family="Arial"
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Wholesale: %{y:,.0f}<extra></extra>"
            )
        ),
        secondary_y=False
    )

    # --------------------------------------------------
    # Totalone FY corrente sopra ogni istogramma
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
            yref="y"
        )

    # --------------------------------------------------
    # Curva FY precedente in valore assoluto
    # Sovrascritta alle barre tramite asse secondario nascosto
    # --------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=df["Mese"],
            y=df["Totale FY Prec k€"],
            name="PY Ricavi Ricorrenti",
            mode="lines+markers",
            line=dict(
                color=colore_fy_prec,
                width=3.5,
                dash="dash"
            ),
            marker=dict(
                size=9,
                color=colore_fy_prec,
                line=dict(
                    width=2,
                    color="white"
                )
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Totale FY prec.: %{y:,.0f}<br>"
                "Var. % vs FY prec.: %{customdata:+.1f}%<extra></extra>"
            ),
            customdata=df["Delta % vs FY Prec"]
        ),
        secondary_y=True
    )

    # --------------------------------------------------
    # Box sui punti della curva con variazione %
    # --------------------------------------------------

    for _, row in df.iterrows():
        delta_perc = row["Delta % vs FY Prec"]

        if delta_perc >= 0:
            testo_delta = f"+{delta_perc:.1f}%"
            colore_box = "#DCFCE7"
            colore_bordo = "#16A34A"
            colore_font = "#166534"
            y_shift = 24
        else:
            testo_delta = f"{delta_perc:.1f}%"
            colore_box = "#FEE2E2"
            colore_bordo = "#DC2626"
            colore_font = "#991B1B"
            y_shift = -24

        testo_delta = testo_delta.replace(".", ",")

        fig.add_annotation(
            x=row["Mese"],
            y=row["Totale FY Prec k€"],
            yref="y2",
            text=f"<b>{testo_delta}</b>",
            showarrow=False,
            font=dict(
                size=13,
                color=colore_font,
                family="Arial Black"
            ),
            bgcolor=colore_box,
            bordercolor=colore_bordo,
            borderwidth=1,
            borderpad=5,
            yshift=y_shift
        )

    # --------------------------------------------------
    # Layout
    # --------------------------------------------------

    fig.update_layout(
        barmode="stack",
        height=610,
        margin=dict(l=10, r=25, t=115, b=105),

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
            minsize=11
        )
    )

    # --------------------------------------------------
    # Asse X
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
    # Asse Y principale: barre
    # --------------------------------------------------

    fig.update_yaxes(
        visible=False,
        showgrid=False,
        zeroline=False,
        range=[0, df["Totale k€"].max() + 5000],
        secondary_y=False
    )

    # --------------------------------------------------
    # Asse Y secondario: curva FY precedente
    # Scala dedicata per sovrascriverla alle barre
    # e rendere leggibile la variazione mese su mese.
    # --------------------------------------------------

    fy_prec_center = df["Totale FY Prec k€"].mean()
    fy_prec_span = max(
        df["Totale FY Prec k€"].max() - df["Totale FY Prec k€"].min(),
        150
    )

    fig.update_yaxes(
        visible=False,
        showgrid=False,
        zeroline=False,
        range=[
            fy_prec_center - fy_prec_span * 2.2,
            fy_prec_center + fy_prec_span * 2.2
        ],
        secondary_y=True
    )

    return fig


def arpu_chart(df):
    fig = go.Figure()

    df = df.copy()

    # Colori stile immagine allegata
    colore_retail = "#005B96"        # blu scuro
    colore_wholesale = "#F2C94C"     # giallo chiaro
    colore_media = "#D65F2D"         # rosso/arancione linea
    colore_testo = "#111827"

    # --------------------------------------------------
    # Formattazione italiana con virgola decimale
    # --------------------------------------------------

    def fmt_decimal(value, decimals=1):
        return f"{value:.{decimals}f}".replace(".", ",")

    def fmt_delta(value, decimals=1):
        if value >= 0:
            return f"+{value:.{decimals}f}".replace(".", ",")
        else:
            return f"{value:.{decimals}f}".replace(".", ",")

    # --------------------------------------------------
    # Label asse X su due righe: 2025 / Apr
    # --------------------------------------------------

    df["Mese Label"] = df["Mese"].str.replace(" ", "<br>")

    # --------------------------------------------------
    # ARPU PY
    # In produzione questa colonna dovrà arrivare dal dataset.
    # Se non trova il dato reale, usa valori mock temporanei.
    # --------------------------------------------------

    if "ARPU Totale PY" in df.columns:
        df["ARPU Totale PY"] = df["ARPU Totale PY"]

    elif "ARPU PY" in df.columns:
        df["ARPU Totale PY"] = df["ARPU PY"]

    elif "ARPU Totale FY Prec" in df.columns:
        df["ARPU Totale PY"] = df["ARPU Totale FY Prec"]

    elif "ARPU Totale FY precedente" in df.columns:
        df["ARPU Totale PY"] = df["ARPU Totale FY precedente"]

    else:
        # MOCK temporaneo: da sostituire con dato reale PY
        df["ARPU Totale PY"] = df["ARPU Totale"] - np.array(
            [0.2, 0.1, 0.0, 0.3, 0.1, 0.2, -0.1, 0.0, 0.1, -0.1, 0.0, 0.2]
        )

    # --------------------------------------------------
    # Scostamento assoluto ARPU corrente vs PY
    # Formula: ARPU corrente - ARPU PY
    # --------------------------------------------------

    df["Delta ARPU vs PY"] = df["ARPU Totale"] - df["ARPU Totale PY"]

    retail_text = [
        fmt_decimal(v, 1)
        for v in df["ARPU Retail"]
    ]

    wholesale_text = [
        fmt_decimal(v, 1)
        for v in df["ARPU Wholesale"]
    ]

    # --------------------------------------------------
    # Barre Retail
    # --------------------------------------------------

    fig.add_trace(
        go.Bar(
            x=df["Mese Label"],
            y=df["ARPU Retail"],
            name="Retail",
            marker=dict(
                color=colore_retail,
                line=dict(
                    color="rgba(255,255,255,0.55)",
                    width=1
                )
            ),
            text=retail_text,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(
                size=15,
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
            x=df["Mese Label"],
            y=df["ARPU Wholesale"],
            name="Wholesale",
            marker=dict(
                color=colore_wholesale,
                line=dict(
                    color="rgba(255,255,255,0.55)",
                    width=1
                )
            ),
            text=wholesale_text,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(
                size=15,
                color=colore_testo,
                family="Arial"
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "ARPU Wholesale: %{text}<extra></extra>"
            )
        )
    )

    # --------------------------------------------------
    # Linea ARPU medio / totale
    # --------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=df["Mese Label"],
            y=df["ARPU Totale"],
            name="ARPU medioo",
            mode="lines+markers",
            line=dict(
                color=colore_media,
                width=3.5
            ),
            marker=dict(
                size=8,
                color=colore_media,
                line=dict(
                    width=1.5,
                    color=colore_media
                )
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "ARPU medio: %{y:.1f}<br>"
                "Delta vs PY: %{customdata:+.1f}<extra></extra>"
            ),
            customdata=df["Delta ARPU vs PY"]
        )
    )

    # --------------------------------------------------
    # Box su ogni punto della curva
    # Valore assoluto ARPU corrente + scostamento assoluto vs PY
    # --------------------------------------------------

    for _, row in df.iterrows():
        valore_arpu = row["ARPU Totale"]
        delta_arpu = row["Delta ARPU vs PY"]

        testo_box = (
            f"{fmt_decimal(valore_arpu, 1)} "
            f"({fmt_delta(delta_arpu, 1)})"
        )

        if delta_arpu >= 0:
            colore_box = "#DCFCE7"
            colore_bordo = "#16A34A"
            colore_font = "#166534"
            y_shift = 26
        else:
            colore_box = "#FEE2E2"
            colore_bordo = "#DC2626"
            colore_font = "#991B1B"
            y_shift = -26

        fig.add_annotation(
            x=row["Mese Label"],
            y=valore_arpu,
            text=f"<b>{testo_box}</b>",
            showarrow=False,
            font=dict(
                size=13,
                color=colore_font,
                family="Arial Black"
            ),
            bgcolor=colore_box,
            bordercolor=colore_bordo,
            borderwidth=1,
            borderpad=5,
            yshift=y_shift
        )

    # --------------------------------------------------
    # Layout
    # --------------------------------------------------

    valore_max = max(
        df["ARPU Retail"].max(),
        df["ARPU Wholesale"].max(),
        df["ARPU Totale"].max()
    )

    fig.update_layout(
        barmode="group",
        height=600,
        margin=dict(l=10, r=25, t=105, b=105),

        bargap=0.28,
        bargroupgap=0.08,

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
            minsize=11
        )
    )

    # --------------------------------------------------
    # Asse X
    # --------------------------------------------------

    fig.update_xaxes(
        tickangle=0,
        tickfont=dict(
            size=13,
            color="#6B7280",
            family="Arial"
        ),
        showline=False,
        showgrid=False,
        zeroline=False,
        automargin=True
    )

    # --------------------------------------------------
    # Asse Y nascosto
    # --------------------------------------------------

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

nav1, nav2, nav_space = st.columns([1.25, 1.25, 5.5])

with nav1:
    if st.button(
        "Pagina Ricavi",
        use_container_width=True,
        type="primary" if st.session_state.pagina_dashboard == "Ricavi" else "secondary"
    ):
        st.session_state.pagina_dashboard = "Ricavi"
        st.rerun()

with nav2:
    if st.button(
        "Pagina ARPU",
        use_container_width=True,
        type="primary" if st.session_state.pagina_dashboard == "ARPU" else "secondary"
    ):
        st.session_state.pagina_dashboard = "ARPU"
        st.rerun()


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
