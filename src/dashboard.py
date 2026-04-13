import streamlit as st
import pandas as pd
import numpy as np
from src.data_manager import DataManager
from src.stats_manager import StatsManager
from src.visualizer import Visualizer


# ──────────────────────────────────────────────────────────────────
# CSS
# ──────────────────────────────────────────────────────────────────

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background: #f8fafc !important;
    color: #0f172a !important;
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 14px !important;
    -webkit-font-smoothing: antialiased !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: none !important;
    min-width: 220px !important;
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] h3 { color: #f1f5f9 !important; }
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stCaption {
    color: #94a3b8 !important;
    font-size: 12px !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stRadio label {
    color: #94a3b8 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
    font-weight: 600 !important;
}

/* Sidebar radio as nav */
[data-testid="stSidebar"] .stRadio > div {
    gap: 2px !important;
}
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
}
[data-testid="stSidebar"] .stRadio input:checked ~ div p {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Sidebar selectbox */
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 5px !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 5px !important;
}

/* File uploader in sidebar */
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: #1e293b !important;
    border: 1.5px dashed #334155 !important;
    border-radius: 8px !important;
    padding: 0.5rem !important;
}

/* ── Main content ── */
.main .block-container {
    padding: 1.5rem 2rem 3rem !important;
    max-width: 1500px !important;
}

/* ── Topbar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1rem 1.5rem;
    margin-bottom: 1.25rem;
}
.topbar-title { font-size: 1.1rem; font-weight: 700; color: #0f172a; margin: 0; }
.topbar-sub   { font-size: 0.75rem; color: #64748b; margin: 2px 0 0; }
.topbar-right { display: flex; align-items: center; gap: 0.6rem; }
.badge {
    display: inline-block;
    font-size: 0.65rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em;
    padding: 0.22rem 0.6rem; border-radius: 4px;
}
.badge-dark  { background: #0f172a; color: #ffffff; }
.badge-blue  { background: #dbeafe; color: #1d4ed8; }
.badge-green { background: #dcfce7; color: #15803d; }
.badge-red   { background: #fee2e2; color: #b91c1c; }
.badge-amber { background: #fef3c7; color: #b45309; }

/* ── Section label ── */
.sec-label {
    font-size: 0.68rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #94a3b8; margin: 0 0 0.75rem; padding-bottom: 0.5rem;
    border-bottom: 1px solid #e2e8f0;
}

/* ── Cards ── */
.card {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 1.25rem 1.4rem;
    margin-bottom: 1rem;
}
.card-tight { padding: 0.9rem 1.2rem; }

/* ── KPI card ── */
.kpi-row { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem; }
.kpi-card {
    flex: 1; min-width: 140px;
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 1.1rem 1.25rem;
}
.kpi-label {
    font-size: 0.65rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.09em;
    color: #94a3b8; margin: 0 0 0.35rem;
}
.kpi-value {
    font-size: 1.7rem; font-weight: 800;
    color: #0f172a; letter-spacing: -0.02em; margin: 0;
    line-height: 1.15;
}
.kpi-sub { font-size: 0.72rem; color: #64748b; margin: 4px 0 0; }

/* ── Finding cards ── */
.finding {
    border-left: 3px solid #2563eb;
    background: #f8fafc; border-radius: 0 8px 8px 0;
    padding: 0.75rem 1rem; margin-bottom: 0.6rem;
}
.finding-warn  { border-left-color: #d97706; }
.finding-ok    { border-left-color: #16a34a; }
.finding-bad   { border-left-color: #dc2626; }
.finding-title { font-size: 0.84rem; font-weight: 600; color: #0f172a; margin: 0 0 3px; }
.finding-detail{ font-size: 0.78rem; color: #475569; margin: 0; line-height: 1.55; }

/* ── Metric overrides ── */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    padding: 0.9rem 1.1rem !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.66rem !important; font-weight: 700 !important;
    text-transform: uppercase !important; letter-spacing: 0.08em !important;
    color: #94a3b8 !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.55rem !important; font-weight: 800 !important;
    color: #0f172a !important; letter-spacing: -0.02em !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #0f172a !important; color: #ffffff !important;
    border: none !important; border-radius: 5px !important;
    padding: 0.4rem 1rem !important;
    font-size: 0.78rem !important; font-weight: 600 !important;
    letter-spacing: 0.04em !important; text-transform: uppercase !important;
    transition: background 0.15s !important;
}
.stButton > button:hover { background: #1e293b !important; }
[data-testid="stDownloadButton"] > button {
    background: #0f172a !important; color: #ffffff !important;
    border: none !important; border-radius: 5px !important;
    font-size: 0.78rem !important; font-weight: 600 !important;
    letter-spacing: 0.04em !important; text-transform: uppercase !important;
}
[data-testid="stDownloadButton"] > button:hover { background: #1e293b !important; }

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] { border-bottom: 1px solid #e2e8f0 !important; }
[data-testid="stTabs"] [role="tab"] {
    font-size: 0.75rem !important; font-weight: 600 !important;
    text-transform: uppercase !important; letter-spacing: 0.05em !important;
    color: #94a3b8 !important; padding: 0.55rem 0.9rem !important;
    border-radius: 0 !important; border-bottom: 2px solid transparent !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #0f172a !important; border-bottom: 2px solid #0f172a !important;
    background: transparent !important;
}

/* ── Tables ── */
[data-testid="stDataFrame"] {
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important; overflow: hidden !important;
}

/* ── Form controls (main area) ── */
.stSelectbox > label, .stMultiSelect > label,
.stNumberInput > label, .stRadio > label, .stSlider > label {
    font-size: 0.72rem !important; font-weight: 600 !important;
    text-transform: uppercase !important; letter-spacing: 0.06em !important;
    color: #64748b !important;
}
.stSelectbox > div > div, .stMultiSelect > div > div {
    background: #ffffff !important; border: 1px solid #cbd5e1 !important;
    border-radius: 5px !important; color: #0f172a !important; font-size: 13px !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #ffffff !important; border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
}
[data-testid="stExpander"] summary {
    font-size: 0.77rem !important; font-weight: 600 !important;
    text-transform: uppercase !important; letter-spacing: 0.06em !important;
    color: #475569 !important;
}

/* ── Alerts ── */
.stAlert { border-radius: 7px !important; font-size: 0.82rem !important; }

/* ── HR ── */
hr { border: none !important; border-top: 1px solid #e2e8f0 !important; margin: 1.5rem 0 !important; }

/* ── Empty state ── */
.empty-state {
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 4.5rem 2.5rem; text-align: center; margin-top: 1rem;
}
.empty-title { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin: 0 0 0.5rem; }
.empty-sub {
    font-size: 0.85rem; color: #64748b; margin: 0 auto 2.5rem;
    max-width: 400px; line-height: 1.65;
}
.feat-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(175px, 1fr));
    gap: 1rem; text-align: left; margin-bottom: 2rem;
}
.feat-card {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 8px; padding: 1rem 1.1rem;
}
.feat-name { font-size: 0.8rem; font-weight: 700; color: #0f172a; margin: 0 0 4px; }
.feat-desc { font-size: 0.73rem; color: #64748b; margin: 0; line-height: 1.55; }
.fmt-note  { font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.07em; }
</style>
"""


# ──────────────────────────────────────────────────────────────────
# APP
# ──────────────────────────────────────────────────────────────────

class DashboardApp:

    PAGES = [
        "Overview",
        "Exploration",
        "Statistical Analysis",
        "Forecasting",
        "Anomaly Detection",
        "Raw Data",
    ]

    def __init__(self):
        st.set_page_config(
            page_title="DataInsight Pro",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        st.markdown(CSS, unsafe_allow_html=True)

        if 'data_manager' not in st.session_state:
            st.session_state.data_manager = DataManager()
        if 'visualizer' not in st.session_state:
            st.session_state.visualizer = Visualizer()
        if 'stats_manager' not in st.session_state:
            st.session_state.stats_manager = None
        if 'page' not in st.session_state:
            st.session_state.page = "Overview"

        self.dm  = st.session_state.data_manager
        self.viz = st.session_state.visualizer
        self.sm  = st.session_state.stats_manager

    # ── helpers ──────────────────────────────────────────────────

    def _kpi(self, label: str, value: str, sub: str = ''):
        return (
            f'<div class="kpi-card">'
            f'<p class="kpi-label">{label}</p>'
            f'<p class="kpi-value">{value}</p>'
            + (f'<p class="kpi-sub">{sub}</p>' if sub else '')
            + '</div>'
        )

    def _badge(self, text: str, kind: str = 'dark') -> str:
        return f'<span class="badge badge-{kind}">{text}</span>'

    def _finding(self, title: str, detail: str, kind: str = 'info'):
        cls_map = {'info': '', 'warning': 'finding-warn',
                   'success': 'finding-ok', 'error': 'finding-bad'}
        cls = cls_map.get(kind, '')
        return (f'<div class="finding {cls}">'
                f'<p class="finding-title">{title}</p>'
                f'<p class="finding-detail">{detail}</p>'
                f'</div>')

    def _sec(self, text: str):
        st.markdown(f'<p class="sec-label">{text}</p>', unsafe_allow_html=True)

    # ── Sidebar ──────────────────────────────────────────────────

    def render_sidebar(self):
        with st.sidebar:
            st.markdown("""
                <div style="padding:1.25rem 1rem 1rem;border-bottom:1px solid #1e293b;margin-bottom:1rem;">
                    <p style="font-size:1rem;font-weight:800;color:#f1f5f9;margin:0;letter-spacing:-0.01em;">
                        DataInsight Pro
                    </p>
                    <p style="font-size:0.7rem;color:#475569;margin:3px 0 0;text-transform:uppercase;letter-spacing:0.08em;">
                        Decision Analytics Platform
                    </p>
                </div>
            """, unsafe_allow_html=True)

            # Navigation
            st.markdown('<p style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#475569;margin:0 0 0.5rem;">Navigation</p>', unsafe_allow_html=True)
            page = st.radio("nav", self.PAGES, label_visibility="collapsed",
                            key="page_radio")
            st.session_state.page = page

            st.markdown('<div style="border-top:1px solid #1e293b;margin:1rem 0;"></div>', unsafe_allow_html=True)

            # Data upload
            st.markdown('<p style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#475569;margin:0 0 0.5rem;">Data Source</p>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Upload CSV or Excel",
                type=['csv', 'xlsx', 'xls'],
                label_visibility="collapsed",
            )
            if uploaded_file is not None:
                if self.dm.load_data(uploaded_file):
                    self.dm.clean_data()
                    self.sm = StatsManager(self.dm.data)
                    st.session_state.stats_manager = self.sm
                    st.success("Dataset loaded.")

            if self.dm.data is not None:
                info = self.dm.get_data_info()
                st.markdown(
                    f'<p style="font-size:11px;color:#475569;margin-top:0.5rem;">'
                    f'{info["rows"]:,} rows &nbsp;·&nbsp; {info["columns"]} columns</p>',
                    unsafe_allow_html=True,
                )

            # Viz settings (shown only when data is loaded)
            if self.dm.data is not None and page == "Exploration":
                st.markdown('<div style="border-top:1px solid #1e293b;margin:1rem 0;"></div>', unsafe_allow_html=True)
                st.markdown('<p style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#475569;margin:0 0 0.5rem;">Chart Settings</p>', unsafe_allow_html=True)
                numeric_cols = self.dm.get_data_info()['numeric_columns']
                all_cols     = self.dm.get_data_info()['column_names']
                cat_cols     = self.dm.get_data_info()['categorical_columns']

                chart_type = st.selectbox("Chart Type",
                    ["Histogram", "Scatter Plot", "Box Plot",
                     "Bar Chart", "Line Chart", "Correlation Heatmap"])
                st.session_state['chart_type'] = chart_type

                if chart_type == "Histogram":
                    st.session_state['chart_cols'] = st.selectbox("Column", numeric_cols)
                elif chart_type in ("Scatter Plot", "Line Chart"):
                    c1, c2 = st.columns(2)
                    xc = c1.selectbox("X", all_cols if chart_type == "Line Chart" else numeric_cols, key='cx')
                    yc = c2.selectbox("Y", numeric_cols, key='cy')
                    st.session_state['chart_cols'] = (xc, yc)
                elif chart_type == "Box Plot":
                    st.session_state['chart_cols'] = st.multiselect(
                        "Columns", numeric_cols,
                        default=numeric_cols[:min(4, len(numeric_cols))], max_selections=6)
                elif chart_type == "Bar Chart":
                    cats = cat_cols if cat_cols else all_cols
                    c1, c2 = st.columns(2)
                    xc = c1.selectbox("Category", cats, key='bx')
                    yc = c2.selectbox("Value",    numeric_cols, key='by')
                    st.session_state['chart_cols'] = (xc, yc)
                elif chart_type == "Correlation Heatmap":
                    st.session_state['chart_cols'] = None

    # ── Topbar ───────────────────────────────────────────────────

    def _topbar(self, page: str):
        health_badge = ''
        if self.sm is not None:
            h = self.sm.calculate_health_score()
            if h:
                kind = ('green' if h['rating'] in ('Excellent', 'Good')
                        else 'amber' if h['rating'] == 'Fair' else 'red')
                health_badge = self._badge(f"Health: {h['score']:.0f}/100 — {h['rating']}", kind)
        row_badge = ''
        if self.dm.data is not None:
            info = self.dm.get_data_info()
            row_badge = self._badge(f"{info['rows']:,} rows · {info['columns']} cols", 'blue')

        st.markdown(
            f'<div class="topbar">'
            f'<div><p class="topbar-title">DataInsight Pro</p>'
            f'<p class="topbar-sub">Decision Analytics Platform &nbsp;·&nbsp; {page}</p></div>'
            f'<div class="topbar-right">{row_badge} {health_badge}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ──────────────────────────────────────────────────────────────
    # PAGE: OVERVIEW
    # ──────────────────────────────────────────────────────────────

    def page_overview(self):
        self._sec("Executive Summary")
        if self.sm is None:
            st.info("Upload a dataset to view the executive summary and key findings.")
            return

        findings = self.sm.generate_executive_summary()
        html = ''.join(self._finding(f['title'], f['detail'], f['type']) for f in findings)
        st.markdown(html, unsafe_allow_html=True)

        st.markdown("---")

        # KPIs
        self._sec("Key Performance Indicators")
        info   = self.dm.get_data_info()
        health = self.sm.calculate_health_score()
        h_val  = f"{health['score']:.0f}" if health else 'N/A'
        h_sub  = health['rating'] if health else ''

        kpis_html = (
            '<div class="kpi-row">'
            + self._kpi("Total Records",      f"{info['rows']:,}")
            + self._kpi("Columns",            f"{info['columns']}")
            + self._kpi("Numeric Fields",     f"{len(info['numeric_columns'])}")
            + self._kpi("Categorical Fields", f"{len(info['categorical_columns'])}")
            + self._kpi("Data Quality Score", f"{h_val}/100", h_sub)
            + self._kpi("Missing Values",     f"{self.dm.data.isnull().sum().sum():,}",
                         f"{self.dm.data.isnull().sum().sum() / (info['rows'] * info['columns']) * 100:.1f}% of cells")
            + '</div>'
        )
        st.markdown(kpis_html, unsafe_allow_html=True)

        st.markdown("---")

        # Health gauge + top correlations
        col_g, col_c = st.columns([1, 2])
        with col_g:
            self._sec("Data Quality Gauge")
            if health:
                fig = self.viz.create_health_gauge(health['score'], health['rating'])
                st.plotly_chart(fig, use_container_width=True)
                # Component breakdown
                comp = health['components']
                for name, val in [("Completeness", comp['missing_score']),
                                   ("No Duplicates", comp['duplicate_score']),
                                   ("No Outliers",   comp['outlier_score']),
                                   ("Consistency",   comp['consistency_score'])]:
                    color = '#16a34a' if val >= 80 else '#d97706' if val >= 50 else '#dc2626'
                    pct   = f"{val:.0f}%"
                    st.markdown(
                        f'<div style="display:flex;align-items:center;justify-content:space-between;'
                        f'padding:5px 0;border-bottom:1px solid #f1f5f9;">'
                        f'<span style="font-size:12px;color:#475569;">{name}</span>'
                        f'<span style="font-size:12px;font-weight:700;color:{color};">{pct}</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

        with col_c:
            self._sec("Top Variable Relationships")
            top_corr = self.sm.get_top_correlations(n=8)
            if not top_corr.empty:
                st.dataframe(top_corr, use_container_width=True, hide_index=True,
                             height=260)
                st.info(self.sm.generate_correlation_insight())
            else:
                st.info("No numeric columns available for correlation analysis.")

        st.markdown("---")

        # Variance analysis table
        self._sec("Volatility & Variability Analysis")
        var_df = self.sm.get_variance_analysis()
        if not var_df.empty:
            c1, c2 = st.columns([2, 1])
            with c1:
                st.dataframe(var_df, use_container_width=True, hide_index=True, height=280)
            with c2:
                fig = self.viz.create_cv_chart(var_df)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns available.")

    # ──────────────────────────────────────────────────────────────
    # PAGE: EXPLORATION
    # ──────────────────────────────────────────────────────────────

    def page_exploration(self):
        if self.sm is None:
            st.info("Upload a dataset to begin exploration.")
            return

        chart_type = st.session_state.get('chart_type', 'Histogram')
        chart_cols = st.session_state.get('chart_cols', None)

        self._sec(f"Interactive Chart — {chart_type}")
        try:
            if chart_type == "Correlation Heatmap":
                corr = self.sm.get_correlations()
                if corr is not None:
                    fig = self.viz.create_heatmap(corr)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No numeric columns for correlation heatmap.")

            elif chart_type == "Histogram" and chart_cols:
                fig = self.viz.create_histogram(self.dm.data, chart_cols)
                st.plotly_chart(fig, use_container_width=True)
                st.info(self.sm.generate_distribution_insight(chart_cols))

            elif chart_type == "Scatter Plot" and chart_cols:
                fig = self.viz.create_scatter(self.dm.data, chart_cols[0], chart_cols[1])
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Box Plot" and chart_cols:
                fig = self.viz.create_box_plot(self.dm.data, chart_cols)
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Bar Chart" and chart_cols:
                fig = self.viz.create_bar_chart(self.dm.data, chart_cols[0], chart_cols[1])
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Line Chart" and chart_cols:
                fig = self.viz.create_line_chart(self.dm.data, chart_cols[0], chart_cols[1])
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.info("Configure chart settings in the sidebar.")
        except Exception as e:
            st.error(f"Chart error: {e}")

        st.markdown("---")

        # Column summary table
        self._sec("Column Summary")
        c1, c2 = st.columns([1, 2])
        with c1:
            type_counts = self.dm.data.dtypes.astype(str).value_counts()
            fig = self.viz.create_pie_chart(type_counts.index.tolist(),
                                             type_counts.values.tolist(), "Column Types")
            fig.update_layout(height=280, margin=dict(t=10, b=30, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            master = self.sm.get_comprehensive_summary()
            if not master.empty:
                master['Missing (%)'] = master['Missing (%)'].map('{:.1f}%'.format)
                st.dataframe(master, use_container_width=True, hide_index=True, height=280,
                             column_config={
                                 "Missing (%)": st.column_config.ProgressColumn(
                                     "Missing (%)", format="%s", min_value=0, max_value=100)
                             })

    # ──────────────────────────────────────────────────────────────
    # PAGE: STATISTICAL ANALYSIS
    # ──────────────────────────────────────────────────────────────

    def page_stats(self):
        if self.sm is None:
            st.info("Upload a dataset to run statistical analyses.")
            return

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Outlier Detection",
            "Group Comparison",
            "Regression",
            "Hypothesis Testing",
            "Pareto Analysis",
        ])

        # ── Outlier Detection ──
        with tab1:
            self._sec("IQR-Based Outlier Detection")
            st.markdown(
                "Outliers are identified where values fall outside **Q1 − 1.5×IQR** "
                "or **Q3 + 1.5×IQR**. Review flagged records before drawing conclusions."
            )
            outliers = self.sm.get_outliers()
            if outliers:
                col_select = st.selectbox("Inspect Column", list(outliers.keys()))
                if col_select:
                    df_out = outliers[col_select]
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Outlier Rows",  len(df_out))
                    m2.metric("Min Outlier Value", f"{df_out[col_select].min():.4f}")
                    m3.metric("Max Outlier Value", f"{df_out[col_select].max():.4f}")
                    st.dataframe(df_out, use_container_width=True, height=300)
            else:
                st.success("No IQR outliers detected across all numeric columns.")
            st.info(self.sm.generate_outlier_insight())

        # ── Group Comparison ──
        with tab2:
            self._sec("Grouped Aggregation & Comparison")
            st.markdown("Aggregate a numeric metric by a categorical dimension to reveal segment differences.")
            cat_cols = self.dm.get_data_info()['categorical_columns']
            num_cols = self.dm.get_data_info()['numeric_columns']
            if cat_cols and num_cols:
                c1, c2, c3 = st.columns(3)
                g_col   = c1.selectbox("Group By",    cat_cols)
                v_col   = c2.selectbox("Metric",      num_cols)
                agg_fn  = c3.selectbox("Aggregation", ["mean", "sum", "count", "min", "max", "std"])
                grouped = self.sm.get_grouped_stats(g_col, v_col, agg_fn)
                if not grouped.empty:
                    col_left, col_right = st.columns([1, 2])
                    with col_left:
                        st.dataframe(grouped, use_container_width=True, hide_index=True)
                    with col_right:
                        fig = self.viz.create_horizontal_bar_chart(
                            grouped, x_col=grouped.columns[1],
                            y_col=grouped.columns[0],
                            title=f"{grouped.columns[1]} by {grouped.columns[0]}")
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Both categorical and numeric columns are required.")

        # ── Regression ──
        with tab3:
            self._sec("Linear Regression Analysis")
            st.markdown(
                "Fits a linear model **y = mx + b** and reports goodness-of-fit (R²) "
                "and statistical significance."
            )
            num_cols = self.dm.get_data_info()['numeric_columns']
            if len(num_cols) >= 2:
                c1, c2 = st.columns(2)
                x_var = c1.selectbox("Independent Variable (X)", num_cols, key='rx')
                y_var = c2.selectbox("Dependent Variable (Y)",   num_cols, index=1, key='ry')
                if x_var != y_var:
                    reg = self.sm.calculate_regression(x_var, y_var)
                    if reg:
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("Equation",  reg['equation'])
                        m2.metric("R²",        f"{reg['r_squared']:.4f}")
                        m3.metric("Slope",     f"{reg['slope']:.4f}")
                        m4.metric("P-Value",   f"{reg['p_value']:.4f}")
                        sig_text = ("Statistically significant (p < 0.05)"
                                    if reg['significant'] else "Not statistically significant (p ≥ 0.05)")
                        st.info(sig_text)
                        fig = self.viz.create_regression_chart(
                            self.dm.data, x_var, y_var, reg['slope'], reg['intercept'])
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error("Could not compute regression model.")
                else:
                    st.warning("Select different variables for X and Y.")
            else:
                st.warning("At least two numeric columns are required.")

        # ── Hypothesis Testing ──
        with tab4:
            self._sec("Statistical Hypothesis Testing")
            test_type = st.radio("Test", ["Normality — Shapiro-Wilk", "Independent T-Test"],
                                 horizontal=True)

            if test_type == "Normality — Shapiro-Wilk":
                st.markdown(
                    "Tests whether a column's distribution is consistent with normality. "
                    "**H₀:** Data is normally distributed. Reject if p ≤ 0.05."
                )
                num_cols = self.dm.get_data_info()['numeric_columns']
                if num_cols:
                    col_test = st.selectbox("Column to Test", num_cols)
                    if st.button("Run Normality Test"):
                        res = self.sm.perform_normality_test(col_test)
                        if res:
                            if 'warning' in res:
                                st.warning(res['warning'])
                            m1, m2 = st.columns(2)
                            m1.metric("Shapiro-Wilk Statistic", f"{res['statistic']:.4f}")
                            m2.metric("P-Value", f"{res['p_value']:.4f}")
                            if res['is_normal']:
                                st.success(
                                    f"p = {res['p_value']:.4f} > 0.05. Fail to reject H₀. "
                                    f"'{col_test}' is consistent with a normal distribution.")
                            else:
                                st.warning(
                                    f"p = {res['p_value']:.4f} ≤ 0.05. Reject H₀. "
                                    f"'{col_test}' deviates significantly from normality.")

            else:
                st.markdown(
                    "Compares the means of two independent groups. "
                    "**H₀:** The group means are equal. Reject if p ≤ 0.05."
                )
                cat_cols = self.dm.get_data_info()['categorical_columns']
                num_cols = self.dm.get_data_info()['numeric_columns']
                if cat_cols and num_cols:
                    c1, c2 = st.columns(2)
                    g_col = c1.selectbox("Grouping Column (2 groups)", cat_cols)
                    v_col = c2.selectbox("Value Column",               num_cols)
                    if st.button("Run T-Test"):
                        res = self.sm.perform_ttest(g_col, v_col)
                        if 'error' in res:
                            st.error(res['error'])
                        else:
                            if 'warnings' in res:
                                for w in res['warnings']:
                                    st.warning(w)
                            m1, m2, m3, m4 = st.columns(4)
                            m1.metric("Group A",    res['group1'])
                            m2.metric("Group B",    res['group2'])
                            m3.metric("T-Statistic", f"{res['statistic']:.4f}")
                            m4.metric("P-Value",    f"{res['p_value']:.4f}")
                            if res['significant']:
                                st.success(
                                    f"p = {res['p_value']:.4f} < 0.05. Significant difference "
                                    f"between '{res['group1']}' and '{res['group2']}'.")
                            else:
                                st.info(
                                    f"p = {res['p_value']:.4f} ≥ 0.05. No significant difference "
                                    "detected between the two groups.")
                else:
                    st.warning("Both categorical and numeric columns are required.")

        # ── Pareto ──
        with tab5:
            self._sec("Pareto / 80-20 Analysis")
            st.markdown(
                "Identifies which categories drive 80% of the total value — "
                "a core tool for resource prioritisation and decision-making."
            )
            cat_cols = self.dm.get_data_info()['categorical_columns']
            num_cols = self.dm.get_data_info()['numeric_columns']
            if cat_cols and num_cols:
                c1, c2 = st.columns(2)
                p_cat = c1.selectbox("Category Column", cat_cols, key='pcat')
                p_val = c2.selectbox("Value Column",    num_cols, key='pval')
                pareto_df = self.sm.get_pareto_analysis(p_cat, p_val)
                if not pareto_df.empty:
                    # Summary
                    top80 = pareto_df[pareto_df['In Top 80%']]
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Categories driving 80%",   len(top80))
                    m2.metric("Total categories",         len(pareto_df))
                    m3.metric("Top category share",       f"{pareto_df['Share (%)'].iloc[0]:.1f}%")

                    fig = self.viz.create_pareto_chart(pareto_df, p_cat, 'Total')
                    st.plotly_chart(fig, use_container_width=True)
                    st.dataframe(pareto_df, use_container_width=True, hide_index=True)
            else:
                st.warning("Both categorical and numeric columns are required.")

    # ──────────────────────────────────────────────────────────────
    # PAGE: FORECASTING
    # ──────────────────────────────────────────────────────────────

    def page_forecasting(self):
        if self.sm is None:
            st.info("Upload a dataset to run forecasting.")
            return

        self._sec("Linear Trend Forecasting")
        st.markdown(
            "Projects future values using ordinary least-squares linear regression. "
            "Best suited for datasets with a clear directional trend. "
            "Shaded area represents the **95% confidence interval**."
        )

        num_cols  = self.dm.get_data_info()['numeric_columns']
        date_cols = self.dm.identify_date_columns()

        tab_idx, tab_ts = st.tabs(["Row-Index Forecast", "Time-Series Forecast"])

        with tab_idx:
            if num_cols:
                c1, c2 = st.columns(2)
                col     = c1.selectbox("Column to Forecast", num_cols, key='fc_col')
                periods = c2.slider("Periods to Project", 5, 50, 10)
                fdata = self.sm.get_linear_forecast(col, periods)
                if fdata:
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Trend Direction",   fdata['direction'])
                    m2.metric("Change per Record", f"{fdata['change_per_row']:.4f}")
                    m3.metric("Projected End",     f"{fdata['forecast'][-1]:.3f}")
                    fig = self.viz.create_forecast_chart(fdata, col)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("Unable to compute forecast for selected column.")
            else:
                st.warning("No numeric columns available.")

        with tab_ts:
            if date_cols and num_cols:
                c1, c2, c3, c4 = st.columns(4)
                d_col    = c1.selectbox("Date Column",  date_cols, key='ts_dc')
                v_col    = c2.selectbox("Value Column", num_cols,  key='ts_vc')
                freq     = c3.selectbox("Frequency",
                                        ["D", "W", "M", "Q", "Y"],
                                        index=2,
                                        format_func=lambda x: {"D":"Daily","W":"Weekly","M":"Monthly","Q":"Quarterly","Y":"Yearly"}[x])
                periods  = c4.slider("Forecast Periods", 3, 24, 6)
                fdata = self.sm.get_time_series_forecast(d_col, v_col, freq, periods)
                if fdata:
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Trend",          fdata['direction'])
                    m2.metric("Historical Points", len(fdata['historical_y']))
                    m3.metric("Forecast End",   f"{fdata['forecast'][-1]:.3f}")
                    fig = self.viz.create_time_forecast_chart(fdata, v_col)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Could not generate time-series forecast. Check that the date column parses correctly.")
            else:
                if not date_cols:
                    st.warning("No date columns detected. Upload a dataset with a date/time column for time-series forecasting.")
                else:
                    st.warning("No numeric columns available.")

    # ──────────────────────────────────────────────────────────────
    # PAGE: ANOMALY DETECTION
    # ──────────────────────────────────────────────────────────────

    def page_anomaly(self):
        if self.sm is None:
            st.info("Upload a dataset to run anomaly detection.")
            return

        self._sec("Z-Score Anomaly Detection")
        st.markdown(
            "Flags records where values exceed **N standard deviations** from the column mean. "
            "Z > 3 is the standard threshold for statistical outliers."
        )

        num_cols  = self.dm.get_data_info()['numeric_columns']
        c1, c2    = st.columns([1, 3])
        threshold = c1.slider("Z-Score Threshold", 2.0, 5.0, 3.0, step=0.5)

        summary = self.sm.get_anomaly_summary(threshold)
        anom    = self.sm.get_zscore_anomalies(threshold)

        if summary.empty:
            st.success(f"No anomalies detected at Z > {threshold:.1f} across all numeric columns.")
        else:
            total = int(summary['Anomalies'].sum())
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Anomalous Records", total)
            m2.metric("Columns Affected",        len(summary))
            m3.metric("Max Z-Score",             f"{summary['Max Z-Score'].max():.2f}")

            st.markdown("---")
            self._sec("Anomaly Summary by Column")
            st.dataframe(summary, use_container_width=True, hide_index=True)

            st.markdown("---")
            self._sec("Anomaly Visualisation")
            col_pick = st.selectbox("Select Column to Visualise", list(anom.keys()))
            if col_pick:
                fig = self.viz.create_anomaly_chart(self.dm.data, col_pick, threshold)
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("---")
                self._sec(f"Flagged Records — {col_pick}")
                st.dataframe(anom[col_pick], use_container_width=True, height=300)

                csv = anom[col_pick].to_csv(index=False).encode('utf-8')
                st.download_button("Export Anomalies", data=csv,
                                   file_name=f'anomalies_{col_pick}.csv', mime='text/csv')

        # Interactive filtering
        st.markdown("---")
        self._sec("Threshold Sensitivity")
        st.markdown("Observe how the number of anomalies changes with the threshold.")
        rows = []
        for t in [2.0, 2.5, 3.0, 3.5, 4.0, 5.0]:
            s = self.sm.get_anomaly_summary(t)
            rows.append({'Threshold (σ)': t,
                         'Anomalous Records': int(s['Anomalies'].sum()) if not s.empty else 0,
                         'Columns Affected':  len(s)})
        sens_df = pd.DataFrame(rows)
        st.dataframe(sens_df, use_container_width=True, hide_index=True)

    # ──────────────────────────────────────────────────────────────
    # PAGE: RAW DATA
    # ──────────────────────────────────────────────────────────────

    def page_raw_data(self):
        if self.dm.data is None:
            st.info("Upload a dataset to view raw data.")
            return

        self._sec("Dataset Explorer & Export")
        all_cols = self.dm.get_data_info()['column_names']

        col1, col2 = st.columns([3, 1])
        with col1:
            show_cols = st.multiselect("Visible Columns", all_cols, default=all_cols)
        with col2:
            filter_col = st.selectbox("Filter by Column", ["None"] + all_cols)

        df_show = self.dm.data.copy()
        if filter_col != "None":
            if pd.api.types.is_numeric_dtype(df_show[filter_col]):
                mn = float(df_show[filter_col].min())
                mx = float(df_show[filter_col].max())
                rng = st.slider(f"Range: {filter_col}", mn, mx, (mn, mx))
                df_show = df_show[(df_show[filter_col] >= rng[0]) &
                                  (df_show[filter_col] <= rng[1])]
            else:
                vals = df_show[filter_col].unique()
                sel  = st.multiselect(f"Values: {filter_col}", vals, default=vals)
                df_show = df_show[df_show[filter_col].isin(sel)]

        st.markdown(
            f'<p style="font-size:12px;color:#64748b;margin-bottom:0.5rem;">'
            f'Showing <b>{len(df_show):,}</b> of <b>{len(self.dm.data):,}</b> rows</p>',
            unsafe_allow_html=True,
        )
        st.dataframe(df_show[show_cols], height=480, use_container_width=True)

        c1, c2 = st.columns(2)
        csv = df_show[show_cols].to_csv(index=False).encode('utf-8')
        c1.download_button("Download as CSV", data=csv,
                           file_name='export.csv', mime='text/csv')

        st.markdown("---")
        self._sec("Cleaning Report")
        report = self.dm.get_cleaning_report()
        if report:
            m1, m2, m3 = st.columns(3)
            m1.metric("Initial Rows",          report['initial_rows'])
            m2.metric("Duplicate Rows Removed", report['duplicates_removed'])
            m3.metric("Columns with Imputation", len(report['values_filled']))
            if report['values_filled']:
                with st.expander("Imputed Values Detail"):
                    for col, count in report['values_filled'].items():
                        st.write(f"**{col}**: {count} value(s) filled")
            if report['type_conversions']:
                with st.expander("Type Conversions"):
                    for conv in report['type_conversions']:
                        st.write(f"- {conv}")
        else:
            st.info("No cleaning report available.")

    # ──────────────────────────────────────────────────────────────
    # EMPTY STATE
    # ──────────────────────────────────────────────────────────────

    def page_empty(self):
        st.markdown("""
            <div class="empty-state">
                <p class="empty-title">No Dataset Loaded</p>
                <p class="empty-sub">
                    Upload a CSV or Excel file using the sidebar to begin.
                    The platform will automatically clean, profile, and analyse your data.
                </p>
                <div class="feat-grid">
                    <div class="feat-card">
                        <p class="feat-name">Executive Summary</p>
                        <p class="feat-desc">Auto-generated key findings, risks and data quality assessment on load.</p>
                    </div>
                    <div class="feat-card">
                        <p class="feat-name">Correlation Analysis</p>
                        <p class="feat-desc">Pearson correlation matrix and ranked relationship table.</p>
                    </div>
                    <div class="feat-card">
                        <p class="feat-name">Volatility Analysis</p>
                        <p class="feat-desc">Coefficient of Variation, skewness and kurtosis per column.</p>
                    </div>
                    <div class="feat-card">
                        <p class="feat-name">Linear Forecasting</p>
                        <p class="feat-desc">OLS trend projection with 95% confidence intervals — row-index and time-series modes.</p>
                    </div>
                    <div class="feat-card">
                        <p class="feat-name">Anomaly Detection</p>
                        <p class="feat-desc">Z-score flagging with threshold sensitivity analysis and one-click export.</p>
                    </div>
                    <div class="feat-card">
                        <p class="feat-name">Pareto / 80-20</p>
                        <p class="feat-desc">Identify the categories that drive 80% of your total value.</p>
                    </div>
                    <div class="feat-card">
                        <p class="feat-name">Hypothesis Testing</p>
                        <p class="feat-desc">Shapiro-Wilk normality and independent T-test with significance reporting.</p>
                    </div>
                    <div class="feat-card">
                        <p class="feat-name">Grouped Aggregation</p>
                        <p class="feat-desc">Compare segments by any metric and aggregation function.</p>
                    </div>
                </div>
                <p class="fmt-note">Supported formats: CSV &nbsp;·&nbsp; XLSX &nbsp;·&nbsp; XLS &nbsp;·&nbsp; Up to 200 MB</p>
            </div>
        """, unsafe_allow_html=True)

    # ──────────────────────────────────────────────────────────────
    # RUN
    # ──────────────────────────────────────────────────────────────

    def run(self):
        self.render_sidebar()
        # Sync sm from session state after sidebar potentially updated it
        self.sm = st.session_state.stats_manager

        page = st.session_state.get('page', 'Overview')
        self._topbar(page)

        if self.dm.data is None:
            self.page_empty()
            return

        if page == "Overview":
            self.page_overview()
        elif page == "Exploration":
            self.page_exploration()
        elif page == "Statistical Analysis":
            self.page_stats()
        elif page == "Forecasting":
            self.page_forecasting()
        elif page == "Anomaly Detection":
            self.page_anomaly()
        elif page == "Raw Data":
            self.page_raw_data()
