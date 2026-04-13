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
*,*::before,*::after{box-sizing:border-box}
html,body,.stApp{background:#f8fafc!important;color:#0f172a!important;font-family:'Inter',system-ui,sans-serif!important;font-size:14px!important;-webkit-font-smoothing:antialiased!important}

/* ── Sidebar ── */
[data-testid="stSidebar"]{background:#0f172a!important;border-right:none!important;min-width:220px!important}
[data-testid="stSidebar"] *{color:#cbd5e1!important}
[data-testid="stSidebar"] h3{color:#f1f5f9!important}
[data-testid="stSidebar"] .stMarkdown p,[data-testid="stSidebar"] label,[data-testid="stSidebar"] .stCaption{color:#94a3b8!important;font-size:12px!important}
[data-testid="stSidebar"] .stSelectbox label,[data-testid="stSidebar"] .stMultiSelect label,[data-testid="stSidebar"] .stRadio label{color:#94a3b8!important;font-size:11px!important;text-transform:uppercase!important;letter-spacing:.07em!important;font-weight:600!important}
[data-testid="stSidebar"] .stRadio>div{gap:2px!important}
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p{font-size:13px!important;font-weight:500!important;color:#94a3b8!important;text-transform:none!important;letter-spacing:0!important}
[data-testid="stSidebar"] .stSelectbox>div>div{background:#1e293b!important;border:1px solid #334155!important;border-radius:5px!important;color:#e2e8f0!important}
[data-testid="stSidebar"] .stMultiSelect>div>div{background:#1e293b!important;border:1px solid #334155!important;border-radius:5px!important}
[data-testid="stSidebar"] [data-testid="stFileUploader"]{background:#1e293b!important;border:1.5px dashed #334155!important;border-radius:8px!important;padding:.5rem!important}

/* ── Main ── */
.main .block-container{padding:1.5rem 2rem 3rem!important;max-width:1500px!important}

/* ── Topbar ── */
.topbar{display:flex;align-items:center;justify-content:space-between;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:1rem 1.5rem;margin-bottom:1.25rem}
.topbar-title{font-size:1.1rem;font-weight:700;color:#0f172a;margin:0}
.topbar-sub{font-size:.75rem;color:#64748b;margin:2px 0 0}
.topbar-right{display:flex;align-items:center;gap:.6rem}
.badge{display:inline-block;font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;padding:.22rem .6rem;border-radius:4px}
.badge-dark{background:#0f172a;color:#fff}
.badge-blue{background:#dbeafe;color:#1d4ed8}
.badge-green{background:#dcfce7;color:#15803d}
.badge-red{background:#fee2e2;color:#b91c1c}
.badge-amber{background:#fef3c7;color:#b45309}

/* ── Section label ── */
.sec-label{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#94a3b8;margin:0 0 .75rem;padding-bottom:.5rem;border-bottom:1px solid #e2e8f0}

/* ── Cards ── */
.card{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:1.25rem 1.4rem;margin-bottom:1rem}

/* ── KPI ── */
.kpi-row{display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem}
.kpi-card{flex:1;min-width:140px;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:1.1rem 1.25rem}
.kpi-label{font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.09em;color:#94a3b8;margin:0 0 .35rem}
.kpi-value{font-size:1.7rem;font-weight:800;color:#0f172a;letter-spacing:-.02em;margin:0;line-height:1.15}
.kpi-sub{font-size:.72rem;color:#64748b;margin:4px 0 0}

/* ── Findings ── */
.finding{border-left:3px solid #2563eb;background:#f8fafc;border-radius:0 8px 8px 0;padding:.75rem 1rem;margin-bottom:.6rem}
.finding-warn{border-left-color:#d97706}
.finding-ok{border-left-color:#16a34a}
.finding-bad{border-left-color:#dc2626}
.finding-title{font-size:.84rem;font-weight:600;color:#0f172a;margin:0 0 3px}
.finding-detail{font-size:.78rem;color:#475569;margin:0;line-height:1.55}

/* ── Edit action card ── */
.edit-card{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:1.1rem 1.25rem;margin-bottom:.75rem}
.edit-card-title{font-size:.78rem;font-weight:700;color:#0f172a;margin:0 0 .25rem;text-transform:uppercase;letter-spacing:.06em}
.edit-card-sub{font-size:.74rem;color:#64748b;margin:0 0 .75rem;line-height:1.5}

/* ── Edit log ── */
.log-entry{font-size:.75rem;color:#475569;padding:.3rem .6rem;border-left:2px solid #e2e8f0;margin-bottom:3px;font-family:'Courier New',monospace}

/* ── Metrics ── */
[data-testid="stMetric"]{background:#fff!important;border:1px solid #e2e8f0!important;border-radius:8px!important;padding:.9rem 1.1rem!important}
[data-testid="stMetricLabel"]{font-size:.66rem!important;font-weight:700!important;text-transform:uppercase!important;letter-spacing:.08em!important;color:#94a3b8!important}
[data-testid="stMetricValue"]{font-size:1.55rem!important;font-weight:800!important;color:#0f172a!important;letter-spacing:-.02em!important}

/* ── Buttons ── */
.stButton>button{background:#0f172a!important;color:#fff!important;border:none!important;border-radius:5px!important;padding:.4rem 1rem!important;font-size:.78rem!important;font-weight:600!important;letter-spacing:.04em!important;text-transform:uppercase!important;transition:background .15s!important}
.stButton>button:hover{background:#1e293b!important}
[data-testid="stDownloadButton"]>button{background:#0f172a!important;color:#fff!important;border:none!important;border-radius:5px!important;font-size:.78rem!important;font-weight:600!important;letter-spacing:.04em!important;text-transform:uppercase!important}
[data-testid="stDownloadButton"]>button:hover{background:#1e293b!important}

/* Danger button (red) */
button[kind="secondary"]{background:#dc2626!important;color:#fff!important}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"]{border-bottom:1px solid #e2e8f0!important}
[data-testid="stTabs"] [role="tab"]{font-size:.75rem!important;font-weight:600!important;text-transform:uppercase!important;letter-spacing:.05em!important;color:#94a3b8!important;padding:.55rem .9rem!important;border-radius:0!important;border-bottom:2px solid transparent!important}
[data-testid="stTabs"] [role="tab"][aria-selected="true"]{color:#0f172a!important;border-bottom:2px solid #0f172a!important;background:transparent!important}

/* ── Tables ── */
[data-testid="stDataFrame"]{border:1px solid #e2e8f0!important;border-radius:8px!important;overflow:hidden!important}

/* ── Form controls ── */
.stSelectbox>label,.stMultiSelect>label,.stNumberInput>label,.stRadio>label,.stSlider>label{font-size:.72rem!important;font-weight:600!important;text-transform:uppercase!important;letter-spacing:.06em!important;color:#64748b!important}
.stSelectbox>div>div,.stMultiSelect>div>div{background:#fff!important;border:1px solid #cbd5e1!important;border-radius:5px!important;color:#0f172a!important;font-size:13px!important}

/* ── Expander ── */
[data-testid="stExpander"]{background:#fff!important;border:1px solid #e2e8f0!important;border-radius:8px!important}
[data-testid="stExpander"] summary{font-size:.77rem!important;font-weight:600!important;text-transform:uppercase!important;letter-spacing:.06em!important;color:#475569!important}

/* ── Alerts ── */
.stAlert{border-radius:7px!important;font-size:.82rem!important}
hr{border:none!important;border-top:1px solid #e2e8f0!important;margin:1.5rem 0!important}

/* ── Empty state ── */
.empty-state{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:4.5rem 2.5rem;text-align:center;margin-top:1rem}
.empty-title{font-size:1.15rem;font-weight:700;color:#0f172a;margin:0 0 .5rem}
.empty-sub{font-size:.85rem;color:#64748b;margin:0 auto 2.5rem;max-width:420px;line-height:1.65}
.feat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:1rem;text-align:left;margin-bottom:2rem}
.feat-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:1rem 1.1rem}
.feat-name{font-size:.8rem;font-weight:700;color:#0f172a;margin:0 0 4px}
.feat-desc{font-size:.73rem;color:#64748b;margin:0;line-height:1.55}
.fmt-note{font-size:.7rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.07em}

/* ── Progress bar fix ── */
.stProgress>div>div>div{background:#2563eb!important}
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
        "Anomaly Detection",
        "Data Manager",
        "Raw Data",
    ]

    def __init__(self):
        st.set_page_config(page_title="DataInsight Pro", layout="wide",
                           initial_sidebar_state="expanded")
        st.markdown(CSS, unsafe_allow_html=True)

        if 'data_manager'  not in st.session_state:
            st.session_state.data_manager  = DataManager()
        if 'visualizer'    not in st.session_state:
            st.session_state.visualizer    = Visualizer()
        if 'stats_manager' not in st.session_state:
            st.session_state.stats_manager = None
        if 'page'          not in st.session_state:
            st.session_state.page          = "Overview"

        self.dm  = st.session_state.data_manager
        self.viz = st.session_state.visualizer
        self.sm  = st.session_state.stats_manager

    # ── utils ─────────────────────────────────────────────────────

    def _refresh_sm(self):
        """Rebuild StatsManager after a dataset edit."""
        if self.dm.data is not None:
            self.sm = StatsManager(self.dm.data)
            st.session_state.stats_manager = self.sm

    def _kpi(self, label, value, sub=''):
        return (f'<div class="kpi-card"><p class="kpi-label">{label}</p>'
                f'<p class="kpi-value">{value}</p>'
                + (f'<p class="kpi-sub">{sub}</p>' if sub else '') + '</div>')

    def _badge(self, text, kind='dark'):
        return f'<span class="badge badge-{kind}">{text}</span>'

    def _finding(self, title, detail, kind='info'):
        cls = {'info': '', 'warning': 'finding-warn',
               'success': 'finding-ok', 'error': 'finding-bad'}.get(kind, '')
        return (f'<div class="finding {cls}"><p class="finding-title">{title}</p>'
                f'<p class="finding-detail">{detail}</p></div>')

    def _sec(self, text):
        st.markdown(f'<p class="sec-label">{text}</p>', unsafe_allow_html=True)

    def _edit_card(self, title, description):
        st.markdown(f'<div class="edit-card"><p class="edit-card-title">{title}</p>'
                    f'<p class="edit-card-sub">{description}</p>', unsafe_allow_html=True)

    def _close_edit_card(self):
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Sidebar ───────────────────────────────────────────────────

    def render_sidebar(self):
        with st.sidebar:
            st.markdown("""
                <div style="padding:1.25rem 1rem 1rem;border-bottom:1px solid #1e293b;margin-bottom:1rem;">
                    <p style="font-size:1rem;font-weight:800;color:#f1f5f9;margin:0;letter-spacing:-.01em;">DataInsight Pro</p>
                    <p style="font-size:.7rem;color:#475569;margin:3px 0 0;text-transform:uppercase;letter-spacing:.08em;">Decision Analytics Platform</p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown('<p style="font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#475569;margin:0 0 .5rem;">Navigation</p>', unsafe_allow_html=True)
            page = st.radio("nav", self.PAGES, label_visibility="collapsed", key="page_radio")
            st.session_state.page = page

            st.markdown('<div style="border-top:1px solid #1e293b;margin:1rem 0;"></div>', unsafe_allow_html=True)

            st.markdown('<p style="font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#475569;margin:0 0 .5rem;">Data Source</p>', unsafe_allow_html=True)
            uploaded = st.file_uploader("Upload", type=['csv', 'xlsx', 'xls'],
                                        label_visibility="collapsed")
            if uploaded is not None:
                if self.dm.load_data(uploaded):
                    self.dm.clean_data()
                    self._refresh_sm()
                    st.success("Dataset loaded.")

            if self.dm.data is not None:
                info = self.dm.get_data_info()
                st.markdown(f'<p style="font-size:11px;color:#475569;margin-top:.5rem;">{info["rows"]:,} rows · {info["columns"]} columns</p>', unsafe_allow_html=True)

                if page == "Exploration":
                    st.markdown('<div style="border-top:1px solid #1e293b;margin:1rem 0;"></div>', unsafe_allow_html=True)
                    st.markdown('<p style="font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#475569;margin:0 0 .5rem;">Dashboard Filter</p>', unsafe_allow_html=True)
                    num_cols = info['numeric_columns']
                    cat_cols = info['categorical_columns']
                    # Optional: pin a categorical column as the primary group dimension
                    if cat_cols:
                        st.session_state['dash_group'] = st.selectbox(
                            "Group Dimension", ["None"] + cat_cols, key='dash_grp')
                    else:
                        st.session_state['dash_group'] = "None"
                    if num_cols:
                        st.session_state['dash_kpi'] = st.selectbox(
                            "Primary KPI", num_cols, key='dash_kpi_sel')
                    else:
                        st.session_state['dash_kpi'] = None

    # ── Topbar ────────────────────────────────────────────────────

    def _topbar(self, page):
        health_badge = row_badge = ''
        if self.sm is not None:
            h = self.sm.calculate_health_score()
            if h:
                kind = ('green' if h['rating'] in ('Excellent', 'Good')
                        else 'amber' if h['rating'] == 'Fair' else 'red')
                health_badge = self._badge(f"Health: {h['score']:.0f}/100 — {h['rating']}", kind)
        if self.dm.data is not None:
            info = self.dm.get_data_info()
            row_badge = self._badge(f"{info['rows']:,} rows · {info['columns']} cols", 'blue')
        st.markdown(
            f'<div class="topbar"><div><p class="topbar-title">DataInsight Pro</p>'
            f'<p class="topbar-sub">Decision Analytics Platform · {page}</p></div>'
            f'<div class="topbar-right">{row_badge} {health_badge}</div></div>',
            unsafe_allow_html=True)

    # ──────────────────────────────────────────────────────────────
    # PAGE: OVERVIEW
    # ──────────────────────────────────────────────────────────────

    def page_overview(self):
        self._sec("Executive Summary")
        if self.sm is None:
            st.info("Upload a dataset to view the executive summary and key findings.")
            return

        findings = self.sm.generate_executive_summary()
        st.markdown(''.join(self._finding(f['title'], f['detail'], f['type']) for f in findings),
                    unsafe_allow_html=True)
        st.markdown("---")

        self._sec("Key Performance Indicators")
        info   = self.dm.get_data_info()
        health = self.sm.calculate_health_score()
        h_val  = f"{health['score']:.0f}" if health else 'N/A'
        h_sub  = health['rating']          if health else ''
        total_missing = self.dm.data.isnull().sum().sum()
        total_dups    = int(self.dm.data.duplicated().sum())
        pct_missing   = total_missing / (info['rows'] * info['columns']) * 100

        st.markdown(
            '<div class="kpi-row">'
            + self._kpi("Total Records",      f"{info['rows']:,}")
            + self._kpi("Columns",            f"{info['columns']}")
            + self._kpi("Numeric Fields",     f"{len(info['numeric_columns'])}")
            + self._kpi("Categorical Fields", f"{len(info['categorical_columns'])}")
            + self._kpi("Quality Score",      f"{h_val}/100", h_sub)
            + self._kpi("Missing Cells",      f"{total_missing:,}", f"{pct_missing:.1f}% of cells")
            + self._kpi("Duplicate Rows",     f"{total_dups:,}")
            + '</div>', unsafe_allow_html=True)
        st.markdown("---")

        col_g, col_c = st.columns([1, 2])
        with col_g:
            self._sec("Data Quality Gauge")
            if health:
                st.plotly_chart(self.viz.create_health_gauge(health['score'], health['rating']),
                                use_container_width=True)
                comp = health['components']
                for name, val in [("Completeness", comp['missing_score']),
                                   ("No Duplicates", comp['duplicate_score']),
                                   ("No Outliers",   comp['outlier_score']),
                                   ("Consistency",   comp['consistency_score'])]:
                    color = '#16a34a' if val >= 80 else '#d97706' if val >= 50 else '#dc2626'
                    st.markdown(
                        f'<div style="display:flex;align-items:center;justify-content:space-between;'
                        f'padding:5px 0;border-bottom:1px solid #f1f5f9;">'
                        f'<span style="font-size:12px;color:#475569;">{name}</span>'
                        f'<span style="font-size:12px;font-weight:700;color:{color};">{val:.0f}%</span>'
                        f'</div>', unsafe_allow_html=True)
        with col_c:
            self._sec("Top Variable Relationships")
            top_corr = self.sm.get_top_correlations(n=8)
            if not top_corr.empty:
                st.dataframe(top_corr, use_container_width=True, hide_index=True, height=260)
                st.info(self.sm.generate_correlation_insight())
            else:
                st.info("No numeric columns for correlation.")
        st.markdown("---")

        self._sec("Volatility & Variability Analysis")
        var_df = self.sm.get_variance_analysis()
        if not var_df.empty:
            c1, c2 = st.columns([2, 1])
            with c1:
                st.dataframe(var_df, use_container_width=True, hide_index=True, height=280)
            with c2:
                st.plotly_chart(self.viz.create_cv_chart(var_df), use_container_width=True)

    # ──────────────────────────────────────────────────────────────
    # PAGE: EXPLORATION  (auto-generated BI dashboard)
    # ──────────────────────────────────────────────────────────────

    def page_exploration(self):
        if self.sm is None:
            st.info("Upload a dataset to generate the dashboard.")
            return

        info      = self.dm.get_data_info()
        num_cols  = info['numeric_columns']
        cat_cols  = info['categorical_columns']
        date_cols = self.dm.identify_date_columns()
        df        = self.dm.data
        group_col = st.session_state.get('dash_group', 'None')
        kpi_col   = st.session_state.get('dash_kpi', num_cols[0] if num_cols else None)

        import plotly.graph_objects as go

        # ── SECTION 1: KPI Strip ──────────────────────────────────
        self._sec("Key Metrics")
        kpi_html = '<div class="kpi-row">'
        for col in num_cols[:8]:
            val  = df[col].sum()
            mean = df[col].mean()
            label = 'Total' if col.lower() not in ('age','year','rate','ratio','score','pct','percent') else 'Average'
            display = df[col].sum() if label == 'Total' else mean
            if abs(display) >= 1_000_000:
                fmt = f"{display/1_000_000:.2f}M"
            elif abs(display) >= 1_000:
                fmt = f"{display/1_000:.1f}K"
            else:
                fmt = f"{display:,.2f}"
            kpi_html += self._kpi(col[:22], fmt, f"Mean: {mean:,.2f}")
        kpi_html += '</div>'
        st.markdown(kpi_html, unsafe_allow_html=True)

        st.markdown("---")

        # ── SECTION 2: Primary KPI breakdown by group ─────────────
        if kpi_col and group_col and group_col != 'None':
            self._sec(f"{kpi_col} Breakdown by {group_col}")
            top_cats = df[group_col].value_counts().head(20).index
            grp_df   = (df[df[group_col].isin(top_cats)]
                        .groupby(group_col)[kpi_col]
                        .sum()
                        .reset_index()
                        .sort_values(kpi_col, ascending=False))
            c1, c2 = st.columns(2)
            with c1:
                fig = go.Figure(go.Bar(
                    x=grp_df[group_col], y=grp_df[kpi_col],
                    marker=dict(color=grp_df[kpi_col], colorscale='Blues',
                                line=dict(color='#ffffff', width=0.6)),
                    text=grp_df[kpi_col].map(lambda v: f"{v:,.0f}"),
                    textposition='outside',
                    textfont=dict(color='#475569', size=10),
                ))
                fig.update_layout(
                    title=f"Total {kpi_col} by {group_col}",
                    xaxis_title=group_col, yaxis_title=kpi_col,
                    paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
                    font=dict(family='Inter, system-ui, sans-serif', color='#0f172a'),
                    height=380, margin=dict(l=50, r=20, t=50, b=60),
                    xaxis=dict(tickangle=-30, gridcolor='#f1f5f9'),
                    yaxis=dict(gridcolor='#f1f5f9'),
                )
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                total = grp_df[kpi_col].sum()
                labels = grp_df[group_col].tolist()[:12]
                values = grp_df[kpi_col].tolist()[:12]
                fig2 = self.viz.create_pie_chart(labels, values, f"{kpi_col} Share by {group_col}")
                fig2.update_layout(height=380)
                st.plotly_chart(fig2, use_container_width=True)
            st.markdown("---")

        # ── SECTION 3: Numeric distributions (histograms, 3-up) ───
        if num_cols:
            self._sec("Numeric Distributions")
            cols_to_show = num_cols[:9]
            rows = [cols_to_show[i:i+3] for i in range(0, len(cols_to_show), 3)]
            for row_cols in rows:
                grid = st.columns(len(row_cols))
                for col_widget, col_name in zip(grid, row_cols):
                    with col_widget:
                        try:
                            fig = self.viz.create_histogram(df, col_name)
                            fig.update_layout(height=280, margin=dict(l=40, r=15, t=45, b=40),
                                              showlegend=False)
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception:
                            pass
            st.markdown("---")

        # ── SECTION 4: Box plot comparison ────────────────────────
        if len(num_cols) >= 2:
            self._sec("Distribution Spread — Box Plot")
            box_cols = num_cols[:10]
            try:
                fig = self.viz.create_box_plot(df, box_cols)
                fig.update_layout(height=360)
                st.plotly_chart(fig, use_container_width=True)
            except Exception:
                pass
            st.markdown("---")

        # ── SECTION 5: Categorical breakdowns ─────────────────────
        if cat_cols:
            self._sec("Category Distributions")
            show_cats = [c for c in cat_cols if df[c].nunique() <= 40][:6]
            if show_cats:
                rows = [show_cats[i:i+2] for i in range(0, len(show_cats), 2)]
                for row_cats in rows:
                    grid = st.columns(len(row_cats))
                    for col_widget, cat_name in zip(grid, row_cats):
                        with col_widget:
                            try:
                                top20 = df[cat_name].value_counts().head(20)
                                if top20.nunique() <= 7:
                                    fig = self.viz.create_pie_chart(
                                        top20.index.tolist(),
                                        top20.values.tolist(),
                                        cat_name)
                                    fig.update_layout(height=320, margin=dict(t=40, b=30, l=10, r=10))
                                else:
                                    sorted_df = top20.reset_index()
                                    sorted_df.columns = ['Value', 'Count']
                                    fig = self.viz.create_horizontal_bar_chart(
                                        sorted_df.sort_values('Count'),
                                        x_col='Count', y_col='Value',
                                        title=cat_name)
                                    fig.update_layout(height=320, margin=dict(l=100, r=20, t=45, b=30))
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception:
                                pass
            if num_cols and cat_cols:
                self._sec("Numeric × Category Heatmap")
                try:
                    pivot_cat = show_cats[0] if show_cats else cat_cols[0]
                    pivot_nums = num_cols[:8]
                    pivot_df = df.groupby(pivot_cat)[pivot_nums].mean()
                    # Normalise each column 0-1 for visual comparison
                    normed = (pivot_df - pivot_df.min()) / (pivot_df.max() - pivot_df.min() + 1e-9)
                    fig = self.viz.create_heatmap(normed)
                    fig.update_layout(
                        title=f"Normalised KPIs by {pivot_cat} (0 = min, 1 = max)",
                        height=max(300, len(pivot_df) * 28 + 100))
                    st.plotly_chart(fig, use_container_width=True)
                except Exception:
                    pass
            st.markdown("---")

        # ── SECTION 6: Time series ────────────────────────────────
        if date_cols and num_cols:
            self._sec("Time Series Trends")
            date_col = date_cols[0]
            show_ts  = num_cols[:4]
            try:
                ts_cols = st.columns(min(2, len(show_ts)))
                for i, (col_w, ts_col) in enumerate(zip(ts_cols * 4, show_ts[:4])):
                    with col_w:
                        ts_data = self.sm.get_time_series_data(date_col, ts_col, freq='M')
                        if not ts_data.empty:
                            fig = self.viz.create_time_series_chart(ts_data, date_col, ts_col)
                            fig.update_layout(height=300)
                            st.plotly_chart(fig, use_container_width=True)
            except Exception:
                pass
            st.markdown("---")

        # ── SECTION 7: Scatter matrix (top 4 numeric) ─────────────
        if len(num_cols) >= 2:
            self._sec("Scatter Relationships")
            scatter_cols = num_cols[:4]
            if len(scatter_cols) >= 2:
                pairs = [(scatter_cols[i], scatter_cols[j])
                         for i in range(len(scatter_cols))
                         for j in range(i+1, len(scatter_cols))][:6]
                rows = [pairs[i:i+3] for i in range(0, len(pairs), 3)]
                for row_pairs in rows:
                    grid = st.columns(len(row_pairs))
                    for col_w, (xc, yc) in zip(grid, row_pairs):
                        with col_w:
                            try:
                                fig = self.viz.create_scatter(df, xc, yc)
                                fig.update_layout(height=280, margin=dict(l=50, r=15, t=45, b=40))
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception:
                                pass
            st.markdown("---")

        # ── SECTION 8: Correlation heatmap ────────────────────────
        if len(num_cols) >= 3:
            self._sec("Correlation Matrix")
            try:
                corr = self.sm.get_correlations()
                if corr is not None:
                    fig = self.viz.create_heatmap(corr)
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
            except Exception:
                pass

    # ──────────────────────────────────────────────────────────────
    # PAGE: STATISTICAL ANALYSIS
    # ──────────────────────────────────────────────────────────────

    def page_stats(self):
        if self.sm is None:
            st.info("Upload a dataset to run statistical analyses.")
            return

        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "Outlier Analysis",
            "Segment Comparison",
            "Value Frequency",
            "Cross-Tabulation",
            "Regression",
            "Hypothesis Tests",
            "Pareto 80/20",
        ])

        # ── Outlier Analysis ──────────────────────────────────────
        with tab1:
            self._sec("IQR Outlier Analysis — Inspect & Remove")
            st.markdown("Outliers: values outside **Q1 − 1.5×IQR** or **Q3 + 1.5×IQR**.")
            outliers = self.sm.get_outliers()
            if outliers:
                col_select = st.selectbox("Column", list(outliers.keys()), key='out_col')
                if col_select:
                    df_out = outliers[col_select]
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Outlier Rows",  f"{len(df_out):,}")
                    m2.metric("Total Rows",    f"{len(self.dm.data):,}")
                    m3.metric("Min Outlier",   f"{df_out[col_select].min():.4f}")
                    m4.metric("Max Outlier",   f"{df_out[col_select].max():.4f}")
                    st.dataframe(df_out, use_container_width=True, height=280)

                    c1, c2 = st.columns(2)
                    csv = df_out.to_csv(index=False).encode('utf-8')
                    c1.download_button("Export Outliers", data=csv,
                                       file_name=f'outliers_{col_select}.csv', mime='text/csv')
                    if c2.button(f"Delete {len(df_out):,} Outlier Rows from '{col_select}'", key='del_iqr'):
                        count, msg = self.dm.remove_iqr_outliers(col_select)
                        self._refresh_sm()
                        if count:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.info(msg)
            else:
                st.success("No IQR outliers detected in any numeric column.")
            st.info(self.sm.generate_outlier_insight())

        # ── Segment Comparison ────────────────────────────────────
        with tab2:
            self._sec("Segment Comparison — Multi-Metric KPI Table")
            st.markdown(
                "Compare multiple numeric KPIs across segments of a categorical column. "
                "Reveals performance differences between groups at a glance."
            )
            cat_cols = self.dm.get_data_info()['categorical_columns']
            num_cols = self.dm.get_data_info()['numeric_columns']
            if cat_cols and num_cols:
                c1, c2 = st.columns([1, 2])
                seg_col   = c1.selectbox("Segment By",  cat_cols, key='seg_col')
                seg_vals  = c2.multiselect("Value Columns", num_cols,
                                           default=num_cols[:min(4, len(num_cols))],
                                           max_selections=8)
                agg_fn    = st.radio("Aggregation", ["mean", "sum", "median", "count"],
                                     horizontal=True, key='seg_agg')
                if seg_vals:
                    pivot = self.dm.data.groupby(seg_col)[seg_vals].agg(agg_fn).round(3)
                    pivot = pivot.reset_index()
                    pivot.columns.name = None
                    st.dataframe(pivot, use_container_width=True, hide_index=True)

                    # Visual: bar per metric
                    metric_pick = st.selectbox("Chart Metric", seg_vals, key='seg_chart')
                    fig = self.viz.create_horizontal_bar_chart(
                        pivot.sort_values(metric_pick, ascending=True),
                        x_col=metric_pick, y_col=seg_col,
                        title=f"{agg_fn.capitalize()} of {metric_pick} by {seg_col}")
                    st.plotly_chart(fig, use_container_width=True)

                    csv = pivot.to_csv(index=False).encode('utf-8')
                    st.download_button("Export Segment Table", data=csv,
                                       file_name='segment_comparison.csv', mime='text/csv')
                else:
                    st.info("Select at least one value column.")
            else:
                st.warning("Requires both categorical and numeric columns.")

        # ── Value Frequency ───────────────────────────────────────
        with tab3:
            self._sec("Value Frequency Analysis")
            st.markdown(
                "Inspect the distribution of categorical and low-cardinality columns. "
                "Identify dominant values, rare categories, and potential data entry issues."
            )
            all_cols = self.dm.get_data_info()['column_names']
            freq_col = st.selectbox("Column", all_cols, key='freq_col')
            top_n    = st.slider("Show Top N", 5, 50, 15)
            counts = self.dm.data[freq_col].value_counts().head(top_n).reset_index()
            counts.columns = ['Value', 'Count']
            counts['Share (%)'] = (counts['Count'] / len(self.dm.data) * 100).round(2)
            counts['Cumulative (%)'] = counts['Share (%)'].cumsum().round(2)

            c1, c2, c3 = st.columns(3)
            c1.metric("Unique Values", self.dm.data[freq_col].nunique())
            c2.metric("Most Frequent", str(counts.iloc[0]['Value'])[:30])
            c3.metric("Top-1 Share",   f"{counts.iloc[0]['Share (%)']:.1f}%")

            col_left, col_right = st.columns([1, 2])
            with col_left:
                st.dataframe(counts, use_container_width=True, hide_index=True, height=340)
            with col_right:
                fig = self.viz.create_horizontal_bar_chart(
                    counts.sort_values('Count', ascending=True),
                    x_col='Count', y_col='Value',
                    title=f"Top {top_n} values — {freq_col}")
                st.plotly_chart(fig, use_container_width=True)

        # ── Cross-Tabulation ──────────────────────────────────────
        with tab4:
            self._sec("Cross-Tabulation / Pivot")
            st.markdown(
                "Build a frequency or aggregation pivot table from two categorical dimensions. "
                "Useful for understanding group overlap and co-occurrence patterns."
            )
            cat_cols = self.dm.get_data_info()['categorical_columns']
            num_cols = self.dm.get_data_info()['numeric_columns']
            if len(cat_cols) >= 2:
                c1, c2 = st.columns(2)
                row_col = c1.selectbox("Row Dimension",    cat_cols, key='ct_row')
                col_col = c2.selectbox("Column Dimension", cat_cols, index=1, key='ct_col')
                ct_mode = st.radio("Mode", ["Frequency Count", "Aggregated Value"],
                                   horizontal=True, key='ct_mode')
                if row_col != col_col:
                    if ct_mode == "Frequency Count":
                        ct = pd.crosstab(self.dm.data[row_col], self.dm.data[col_col])
                        st.dataframe(ct, use_container_width=True)
                        fig = self.viz.create_heatmap(ct.astype(float))
                        fig.update_layout(title=f"Cross-Tab Heatmap: {row_col} vs {col_col}")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        if num_cols:
                            val_col = st.selectbox("Value Column", num_cols, key='ct_val')
                            agg_fn  = st.selectbox("Aggregation",
                                                   ["mean", "sum", "count", "min", "max"], key='ct_agg')
                            ct = self.dm.data.pivot_table(values=val_col, index=row_col,
                                                           columns=col_col, aggfunc=agg_fn)
                            st.dataframe(ct.round(3), use_container_width=True)
                            fig = self.viz.create_heatmap(ct.fillna(0).astype(float))
                            fig.update_layout(title=f"{agg_fn.capitalize()} of {val_col}: {row_col} vs {col_col}")
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning("Aggregation requires at least one numeric column.")
                else:
                    st.warning("Row and Column dimensions must be different.")
            else:
                st.warning("At least two categorical columns are required.")

        # ── Regression ────────────────────────────────────────────
        with tab5:
            self._sec("Linear Regression Analysis")
            num_cols = self.dm.get_data_info()['numeric_columns']
            if len(num_cols) >= 2:
                c1, c2 = st.columns(2)
                x_var = c1.selectbox("Independent Variable (X)", num_cols, key='rx')
                y_var = c2.selectbox("Dependent Variable (Y)",   num_cols, index=1, key='ry')
                if x_var != y_var:
                    reg = self.sm.calculate_regression(x_var, y_var)
                    if reg:
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("Equation", reg['equation'])
                        m2.metric("R²",       f"{reg['r_squared']:.4f}")
                        m3.metric("Slope",    f"{reg['slope']:.4f}")
                        m4.metric("P-Value",  f"{reg['p_value']:.4f}")
                        st.info("Statistically significant (p < 0.05)" if reg['significant']
                                else "Not significant (p >= 0.05)")
                        fig = self.viz.create_regression_chart(
                            self.dm.data, x_var, y_var, reg['slope'], reg['intercept'])
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Select different variables for X and Y.")
            else:
                st.warning("At least two numeric columns required.")

        # ── Hypothesis Tests ──────────────────────────────────────
        with tab6:
            self._sec("Statistical Hypothesis Testing")
            test_type = st.radio("Test", ["Normality — Shapiro-Wilk", "Independent T-Test"],
                                 horizontal=True, key='hyp_test')
            num_cols = self.dm.get_data_info()['numeric_columns']
            cat_cols = self.dm.get_data_info()['categorical_columns']
            if test_type == "Normality — Shapiro-Wilk":
                st.markdown("H₀: Data is normally distributed. Reject if p ≤ 0.05.")
                if num_cols:
                    col_test = st.selectbox("Column", num_cols, key='norm_col')
                    if st.button("Run Test", key='run_norm'):
                        res = self.sm.perform_normality_test(col_test)
                        if res:
                            if 'warning' in res:
                                st.warning(res['warning'])
                            m1, m2 = st.columns(2)
                            m1.metric("Statistic", f"{res['statistic']:.4f}")
                            m2.metric("P-Value",   f"{res['p_value']:.4f}")
                            if res['is_normal']:
                                st.success(f"p={res['p_value']:.4f} > 0.05. Fail to reject H₀. '{col_test}' is consistent with normality.")
                            else:
                                st.warning(f"p={res['p_value']:.4f} ≤ 0.05. Reject H₀. '{col_test}' deviates from normality.")
            else:
                st.markdown("H₀: Group means are equal. Reject if p ≤ 0.05.")
                if cat_cols and num_cols:
                    c1, c2 = st.columns(2)
                    g_col = c1.selectbox("Grouping Column (2 groups)", cat_cols, key='tt_grp')
                    v_col = c2.selectbox("Value Column",               num_cols, key='tt_val')
                    if st.button("Run T-Test", key='run_ttest'):
                        res = self.sm.perform_ttest(g_col, v_col)
                        if 'error' in res:
                            st.error(res['error'])
                        else:
                            if 'warnings' in res:
                                for w in res['warnings']:
                                    st.warning(w)
                            m1, m2, m3, m4 = st.columns(4)
                            m1.metric("Group A",      res['group1'])
                            m2.metric("Group B",      res['group2'])
                            m3.metric("T-Statistic",  f"{res['statistic']:.4f}")
                            m4.metric("P-Value",      f"{res['p_value']:.4f}")
                            if res['significant']:
                                st.success(f"Significant difference between '{res['group1']}' and '{res['group2']}' (p={res['p_value']:.4f}).")
                            else:
                                st.info(f"No significant difference (p={res['p_value']:.4f}).")
                else:
                    st.warning("Requires categorical and numeric columns.")

        # ── Pareto ────────────────────────────────────────────────
        with tab7:
            self._sec("Pareto / 80-20 Analysis")
            cat_cols = self.dm.get_data_info()['categorical_columns']
            num_cols = self.dm.get_data_info()['numeric_columns']
            if cat_cols and num_cols:
                c1, c2 = st.columns(2)
                p_cat = c1.selectbox("Category", cat_cols, key='pcat')
                p_val = c2.selectbox("Value",    num_cols, key='pval')
                pareto_df = self.sm.get_pareto_analysis(p_cat, p_val)
                if not pareto_df.empty:
                    top80 = pareto_df[pareto_df['In Top 80%']]
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Categories driving 80%", len(top80))
                    m2.metric("Total categories",        len(pareto_df))
                    m3.metric("Top category share",      f"{pareto_df['Share (%)'].iloc[0]:.1f}%")
                    st.plotly_chart(self.viz.create_pareto_chart(pareto_df, p_cat, 'Total'),
                                    use_container_width=True)
                    st.dataframe(pareto_df, use_container_width=True, hide_index=True)
            else:
                st.warning("Requires categorical and numeric columns.")

    # ──────────────────────────────────────────────────────────────
    # PAGE: ANOMALY DETECTION
    # ──────────────────────────────────────────────────────────────

    def page_anomaly(self):
        if self.sm is None:
            st.info("Upload a dataset to run anomaly detection.")
            return

        self._sec("Z-Score Anomaly Detection — Inspect & Remove")
        st.markdown("Flags records where |z-score| exceeds the threshold. Standard threshold: 3σ.")

        num_cols  = self.dm.get_data_info()['numeric_columns']
        threshold = st.slider("Z-Score Threshold", 2.0, 5.0, 3.0, step=0.5)
        summary   = self.sm.get_anomaly_summary(threshold)
        anom      = self.sm.get_zscore_anomalies(threshold)

        if summary.empty:
            st.success(f"No anomalies detected at Z > {threshold:.1f} across all numeric columns.")
        else:
            total = int(summary['Anomalies'].sum())
            m1, m2, m3 = st.columns(3)
            m1.metric("Anomalous Records", f"{total:,}")
            m2.metric("Columns Affected",  len(summary))
            m3.metric("Max Z-Score",       f"{summary['Max Z-Score'].max():.2f}")

            st.markdown("---")
            self._sec("Anomaly Summary by Column")
            st.dataframe(summary, use_container_width=True, hide_index=True)

            st.markdown("---")
            self._sec("Inspect & Remove by Column")
            col_pick = st.selectbox("Column", list(anom.keys()), key='anom_col')
            if col_pick:
                fig = self.viz.create_anomaly_chart(self.dm.data, col_pick, threshold)
                st.plotly_chart(fig, use_container_width=True)

                df_anom = anom[col_pick]
                st.dataframe(df_anom, use_container_width=True, height=260)

                c1, c2 = st.columns(2)
                csv = df_anom.to_csv(index=False).encode('utf-8')
                c1.download_button("Export Anomalies", data=csv,
                                   file_name=f'anomalies_{col_pick}.csv', mime='text/csv')
                if c2.button(f"Delete {len(df_anom):,} Anomalous Rows from '{col_pick}'",
                             key='del_anom'):
                    count, msg = self.dm.remove_zscore_anomalies(col_pick, threshold)
                    self._refresh_sm()
                    if count:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.info(msg)

        st.markdown("---")
        self._sec("Threshold Sensitivity")
        rows = []
        for t in [2.0, 2.5, 3.0, 3.5, 4.0, 5.0]:
            s = self.sm.get_anomaly_summary(t)
            rows.append({'Threshold (σ)': t,
                         'Anomalous Records': int(s['Anomalies'].sum()) if not s.empty else 0,
                         'Columns Affected':  len(s)})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ──────────────────────────────────────────────────────────────
    # PAGE: DATA MANAGER
    # ──────────────────────────────────────────────────────────────

    def page_data_manager(self):
        if self.dm.data is None:
            st.info("Upload a dataset to use the data manager.")
            return

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Missing Values",
            "Duplicates",
            "Outlier Removal",
            "Column Manager",
            "Custom Filter",
        ])

        info     = self.dm.get_data_info()
        num_cols = info['numeric_columns']
        all_cols = info['column_names']

        # ── Missing Values ────────────────────────────────────────
        with tab1:
            self._sec("Missing Value Analysis & Imputation")
            miss_df = self.dm.get_missing_summary()

            if miss_df.empty:
                st.success("No missing values in any column.")
            else:
                total_miss = int(self.dm.data.isnull().sum().sum())
                m1, m2 = st.columns(2)
                m1.metric("Total Missing Cells",    f"{total_miss:,}")
                m2.metric("Columns with Missing",   len(miss_df))

                # Missing value bar chart
                fig = self.viz.create_horizontal_bar_chart(
                    miss_df.sort_values('Missing (%)').rename(
                        columns={'Missing (%)': 'Missing%', 'Column': 'Col'}),
                    x_col='Missing%', y_col='Col',
                    title="Missing (%) by Column")
                miss_df_display = miss_df.copy()
                miss_df_display['Missing (%)'] = miss_df_display['Missing (%)'].map('{:.2f}%'.format)
                col_l, col_r = st.columns([1, 2])
                col_l.dataframe(miss_df_display, use_container_width=True, hide_index=True)
                col_r.plotly_chart(fig, use_container_width=True)

                st.markdown("---")
                self._sec("Fill Missing Values — Per Column")
                c1, c2, c3 = st.columns(3)
                fill_col    = c1.selectbox("Column", miss_df['Column'].tolist(), key='fill_col')
                fill_method = c2.selectbox("Method",
                    ["mean", "median", "mode", "zero", "forward_fill", "backward_fill"],
                    key='fill_method')
                if c3.button("Apply Fill", key='apply_fill'):
                    n, msg = self.dm.fill_missing(fill_col, fill_method)
                    self._refresh_sm()
                    st.success(msg) if n > 0 else st.info(msg)
                    st.rerun()

                st.markdown("---")
                self._sec("Fill All Missing Values at Once")
                c1, c2 = st.columns(2)
                all_method = c1.selectbox("Method (All Columns)",
                    ["mean", "median", "mode", "zero", "forward_fill", "backward_fill"],
                    key='all_fill_method')
                if c2.button(f"Fill All {total_miss:,} Missing Cells", key='fill_all'):
                    n, msg = self.dm.fill_all_missing(all_method)
                    self._refresh_sm()
                    st.success(msg)
                    st.rerun()

                st.markdown("---")
                self._sec("Drop Rows with Missing Values")
                c1, c2, c3 = st.columns(3)
                drop_col = c1.selectbox("Column (or All)", ["All Columns"] + all_cols, key='drop_miss_col')
                col_arg  = None if drop_col == "All Columns" else drop_col
                preview_count = (self.dm.data.isnull().any(axis=1).sum()
                                 if col_arg is None
                                 else self.dm.data[col_arg].isnull().sum())
                c2.metric("Rows to Drop", f"{preview_count:,}")
                if c3.button(f"Drop {preview_count:,} Rows", key='drop_miss'):
                    n, msg = self.dm.remove_missing_rows(col_arg)
                    self._refresh_sm()
                    st.success(msg)
                    st.rerun()

        # ── Duplicates ────────────────────────────────────────────
        with tab2:
            self._sec("Duplicate Row Manager")
            dups = self.dm.get_duplicate_rows()
            dup_count = len(dups)

            m1, m2, m3 = st.columns(3)
            m1.metric("Duplicate Rows",   f"{dup_count:,}")
            m2.metric("Total Rows",       f"{len(self.dm.data):,}")
            m3.metric("Duplicate Rate",   f"{dup_count / len(self.dm.data) * 100:.2f}%")

            if dup_count > 0:
                st.dataframe(dups.head(200), use_container_width=True, height=280)
                c1, c2 = st.columns(2)
                csv = dups.to_csv(index=False).encode('utf-8')
                c1.download_button("Export Duplicates", data=csv,
                                   file_name='duplicates.csv', mime='text/csv')
                if c2.button(f"Delete All {dup_count:,} Duplicate Rows", key='del_dups'):
                    n, msg = self.dm.remove_duplicates()
                    self._refresh_sm()
                    st.success(msg)
                    st.rerun()
            else:
                st.success("No duplicate rows found in the dataset.")

        # ── Outlier Removal ───────────────────────────────────────
        with tab3:
            self._sec("Bulk Outlier Removal")
            st.markdown(
                "Select a column and method, preview the outlier count, "
                "then delete those rows from the working dataset."
            )
            if num_cols:
                c1, c2 = st.columns(2)
                out_col    = c1.selectbox("Column",  num_cols, key='dm_out_col')
                out_method = c2.selectbox("Method",
                    ["IQR (Q1-1.5×IQR, Q3+1.5×IQR)", "Z-Score (|z| > threshold)"],
                    key='out_method')

                if out_method.startswith("IQR"):
                    Q1  = self.dm.data[out_col].quantile(0.25)
                    Q3  = self.dm.data[out_col].quantile(0.75)
                    IQR = Q3 - Q1
                    lb  = Q1 - 1.5 * IQR
                    ub  = Q3 + 1.5 * IQR
                    preview = int(((self.dm.data[out_col] < lb) |
                                   (self.dm.data[out_col] > ub)).sum())
                    st.info(f"IQR bounds: [{lb:.4f}, {ub:.4f}] — {preview:,} rows will be removed.")
                    if st.button(f"Delete {preview:,} IQR Outlier Rows", key='dm_del_iqr'):
                        n, msg = self.dm.remove_iqr_outliers(out_col)
                        self._refresh_sm()
                        st.success(msg)
                        st.rerun()
                else:
                    z_thresh = st.slider("Z-Score Threshold", 2.0, 5.0, 3.0, key='dm_z')
                    from scipy import stats as sc
                    col_clean = self.dm.data[out_col].dropna()
                    z_scores  = np.abs(sc.zscore(col_clean))
                    preview   = int((z_scores > z_thresh).sum())
                    st.info(f"|z| > {z_thresh:.1f} — {preview:,} rows will be removed.")
                    if st.button(f"Delete {preview:,} Anomalous Rows", key='dm_del_z'):
                        n, msg = self.dm.remove_zscore_anomalies(out_col, z_thresh)
                        self._refresh_sm()
                        st.success(msg)
                        st.rerun()

                # Distribution preview
                fig = self.viz.create_histogram(self.dm.data, out_col)
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No numeric columns available.")

        # ── Column Manager ────────────────────────────────────────
        with tab4:
            self._sec("Column Manager — Rename, Drop, Cast")
            col_df = pd.DataFrame({
                'Column': all_cols,
                'Type':   [str(self.dm.data[c].dtype) for c in all_cols],
                'Missing': [int(self.dm.data[c].isnull().sum()) for c in all_cols],
                'Unique':  [self.dm.data[c].nunique() for c in all_cols],
            })
            st.dataframe(col_df, use_container_width=True, hide_index=True)

            st.markdown("---")
            c1, c2, c3 = st.columns(3)

            # Rename
            with c1:
                st.markdown('<p class="sec-label">Rename Column</p>', unsafe_allow_html=True)
                rn_old = st.selectbox("Column to Rename", all_cols, key='rn_old')
                rn_new = st.text_input("New Name", key='rn_new')
                if st.button("Rename", key='btn_rename'):
                    ok, msg = self.dm.rename_column(rn_old, rn_new)
                    self._refresh_sm()
                    st.success(msg) if ok else st.error(msg)
                    st.rerun()

            # Drop
            with c2:
                st.markdown('<p class="sec-label">Drop Column</p>', unsafe_allow_html=True)
                drop_col_pick = st.selectbox("Column to Drop", all_cols, key='drop_col')
                if st.button("Drop Column", key='btn_drop_col'):
                    ok, msg = self.dm.drop_column(drop_col_pick)
                    self._refresh_sm()
                    st.success(msg) if ok else st.error(msg)
                    st.rerun()

            # Cast type
            with c3:
                st.markdown('<p class="sec-label">Cast Data Type</p>', unsafe_allow_html=True)
                cast_col  = st.selectbox("Column", all_cols, key='cast_col')
                cast_type = st.selectbox("Target Type", ["numeric", "string", "datetime"], key='cast_type')
                if st.button("Apply Cast", key='btn_cast'):
                    ok, msg = self.dm.cast_column(cast_col, cast_type)
                    self._refresh_sm()
                    st.success(msg) if ok else st.error(msg)
                    st.rerun()

        # ── Custom Filter / Row Removal ───────────────────────────
        with tab5:
            self._sec("Custom Row Removal by Condition")
            st.markdown(
                "Remove rows matching a user-defined condition. "
                "Use this to filter out specific values, date ranges, or business-rule violations."
            )
            if num_cols:
                c1, c2, c3 = st.columns(3)
                cond_col = c1.selectbox("Column", num_cols, key='cond_col')
                operator = c2.selectbox("Operator", ["<", "<=", ">", ">=", "==", "!="], key='cond_op')
                value    = c3.number_input("Value", value=0.0, key='cond_val')

                matching = int(getattr(self.dm.data[cond_col],
                                       {'<': '__lt__', '<=': '__le__', '>': '__gt__',
                                        '>=': '__ge__', '==': '__eq__', '!=': '__ne__'}[operator])(value).sum())
                st.info(f"Rows matching '{cond_col} {operator} {value}': **{matching:,}**")
                if st.button(f"Remove {matching:,} Matching Rows", key='btn_cond_remove'):
                    n, msg = self.dm.remove_rows_by_condition(cond_col, operator, value)
                    self._refresh_sm()
                    st.success(msg)
                    st.rerun()
            else:
                st.warning("No numeric columns available for condition filtering.")

        # ── Edit Log & Reset ─────────────────────────────────────
        st.markdown("---")
        c1, c2 = st.columns([3, 1])
        with c1:
            self._sec("Edit Log")
            if self.dm.edit_log:
                for entry in reversed(self.dm.edit_log):
                    st.markdown(f'<div class="log-entry">{entry}</div>', unsafe_allow_html=True)
            else:
                st.caption("No edits applied yet.")
        with c2:
            self._sec("Reset Dataset")
            st.markdown("Revert all edits and restore the original uploaded data.")
            if st.button("Reset to Original", key='btn_reset'):
                msg = self.dm.reset_to_original()
                self._refresh_sm()
                st.success(msg)
                st.rerun()
            # Export current state
            csv = self.dm.data.to_csv(index=False).encode('utf-8')
            st.download_button("Export Current Data", data=csv,
                               file_name='data_edited.csv', mime='text/csv')

    # ──────────────────────────────────────────────────────────────
    # PAGE: RAW DATA
    # ──────────────────────────────────────────────────────────────

    def page_raw_data(self):
        if self.dm.data is None:
            st.info("Upload a dataset to view raw data.")
            return
        self._sec("Dataset Explorer & Export")
        all_cols = self.dm.get_data_info()['column_names']
        c1, c2   = st.columns([3, 1])
        with c1:
            show_cols = st.multiselect("Visible Columns", all_cols, default=all_cols)
        with c2:
            filter_col = st.selectbox("Filter by", ["None"] + all_cols)

        df_show = self.dm.data.copy()
        if filter_col != "None":
            if pd.api.types.is_numeric_dtype(df_show[filter_col]):
                mn = float(df_show[filter_col].min())
                mx = float(df_show[filter_col].max())
                rng = st.slider(f"Range: {filter_col}", mn, mx, (mn, mx))
                df_show = df_show[(df_show[filter_col] >= rng[0]) & (df_show[filter_col] <= rng[1])]
            else:
                vals = list(df_show[filter_col].unique())
                sel  = st.multiselect(f"Values: {filter_col}", vals, default=vals)
                df_show = df_show[df_show[filter_col].isin(sel)]

        st.markdown(
            f'<p style="font-size:12px;color:#64748b;margin-bottom:.5rem;">'
            f'Showing <b>{len(df_show):,}</b> of <b>{len(self.dm.data):,}</b> rows</p>',
            unsafe_allow_html=True)
        st.dataframe(df_show[show_cols], height=500, use_container_width=True)

        c1, c2 = st.columns(2)
        c1.download_button("Download as CSV", data=df_show[show_cols].to_csv(index=False).encode(),
                           file_name='export.csv', mime='text/csv')

        st.markdown("---")
        self._sec("Data Cleaning Report")
        report = self.dm.get_cleaning_report()
        if report:
            m1, m2, m3 = st.columns(3)
            m1.metric("Initial Rows",          report['initial_rows'])
            m2.metric("Duplicates Removed",    report['duplicates_removed'])
            m3.metric("Columns with Imputation", len(report['values_filled']))
            if report['values_filled']:
                with st.expander("Imputed Values"):
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
            <p class="empty-sub">Upload a CSV or Excel file using the sidebar to begin. The platform will automatically clean, profile, and analyse your data.</p>
            <div class="feat-grid">
                <div class="feat-card"><p class="feat-name">Executive Summary</p><p class="feat-desc">Auto-generated key findings, data quality score, and risk flags on upload.</p></div>
                <div class="feat-card"><p class="feat-name">Segment Comparison</p><p class="feat-desc">Compare multiple KPIs across any categorical segment — side-by-side pivot table.</p></div>
                <div class="feat-card"><p class="feat-name">Value Frequency</p><p class="feat-desc">Inspect category distributions, dominant values, and rare-category flags.</p></div>
                <div class="feat-card"><p class="feat-name">Cross-Tabulation</p><p class="feat-desc">Frequency and aggregation pivot tables for two dimensions.</p></div>
                <div class="feat-card"><p class="feat-name">Anomaly Detection</p><p class="feat-desc">Z-score flagging with adjustable threshold. Delete anomalous rows in one click.</p></div>
                <div class="feat-card"><p class="feat-name">Outlier Removal</p><p class="feat-desc">IQR and Z-score outlier detection with one-click deletion and export.</p></div>
                <div class="feat-card"><p class="feat-name">Missing Value Manager</p><p class="feat-desc">Fill or drop missing values by column or all at once, with multiple imputation strategies.</p></div>
                <div class="feat-card"><p class="feat-name">Column Manager</p><p class="feat-desc">Rename, drop, and cast column types interactively.</p></div>
                <div class="feat-card"><p class="feat-name">Custom Row Filter</p><p class="feat-desc">Remove rows matching any numeric condition (e.g. revenue &lt; 0).</p></div>
                <div class="feat-card"><p class="feat-name">Pareto 80/20</p><p class="feat-desc">Identify which categories drive 80% of total value.</p></div>
                <div class="feat-card"><p class="feat-name">Regression & Testing</p><p class="feat-desc">OLS regression with R², slope, and p-value. Shapiro-Wilk and T-Test.</p></div>
                <div class="feat-card"><p class="feat-name">Edit Log & Reset</p><p class="feat-desc">Full audit trail of every edit. One-click reset to original dataset.</p></div>
            </div>
            <p class="fmt-note">Supported formats: CSV &nbsp;·&nbsp; XLSX &nbsp;·&nbsp; XLS &nbsp;·&nbsp; Up to 200 MB</p>
        </div>
        """, unsafe_allow_html=True)

    # ──────────────────────────────────────────────────────────────
    # RUN
    # ──────────────────────────────────────────────────────────────

    def run(self):
        self.render_sidebar()
        self.sm = st.session_state.stats_manager
        page    = st.session_state.get('page', 'Overview')
        self._topbar(page)

        if self.dm.data is None:
            self.page_empty()
            return

        dispatch = {
            "Overview":             self.page_overview,
            "Exploration":          self.page_exploration,
            "Statistical Analysis": self.page_stats,
            "Anomaly Detection":    self.page_anomaly,
            "Data Manager":         self.page_data_manager,
            "Raw Data":             self.page_raw_data,
        }
        dispatch.get(page, self.page_overview)()
