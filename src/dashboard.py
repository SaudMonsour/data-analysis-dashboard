import streamlit as st
import pandas as pd
from src.data_manager import DataManager
from src.stats_manager import StatsManager
from src.visualizer import Visualizer


class DashboardApp:
    """
    Main application class managing the Streamlit dashboard.
    """

    def __init__(self):
        """Initialize the dashboard components."""
        st.set_page_config(
            page_title="Data Analysis Dashboard",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        if 'data_manager' not in st.session_state:
            st.session_state.data_manager = DataManager()
        if 'visualizer' not in st.session_state:
            st.session_state.visualizer = Visualizer()
        if 'stats_manager' not in st.session_state:
            st.session_state.stats_manager = None

        self.data_manager = st.session_state.data_manager
        self.visualizer = st.session_state.visualizer
        self.stats_manager = st.session_state.stats_manager

        self._apply_custom_css()

    def _apply_custom_css(self):
        """Apply professional enterprise CSS styling."""
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

            /* ───────────────────────────────────────────
               GLOBAL RESET & BASE
            ─────────────────────────────────────────── */
            *, *::before, *::after { box-sizing: border-box; }

            html, body, .stApp {
                background-color: #f0f2f5 !important;
                color: #111827 !important;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont,
                             'Segoe UI', sans-serif !important;
                font-size: 14px !important;
                line-height: 1.6 !important;
                -webkit-font-smoothing: antialiased !important;
            }

            /* ───────────────────────────────────────────
               SIDEBAR
            ─────────────────────────────────────────── */
            [data-testid="stSidebar"] {
                background-color: #ffffff !important;
                border-right: 1px solid #e5e7eb !important;
                padding-top: 0 !important;
            }
            [data-testid="stSidebar"] > div:first-child {
                padding-top: 0 !important;
            }
            [data-testid="stSidebar"] .stMarkdown p,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] .stCaption,
            [data-testid="stSidebar"] p {
                color: #374151 !important;
                font-size: 13px !important;
            }
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 {
                color: #111827 !important;
                font-size: 13px !important;
                font-weight: 600 !important;
                letter-spacing: 0.07em !important;
                text-transform: uppercase !important;
                margin-bottom: 0.5rem !important;
            }

            /* Sidebar brand strip */
            .sidebar-brand {
                background: #111827;
                padding: 1.1rem 1.25rem;
                margin: 0 -1rem 1.25rem -1rem;
            }
            .sidebar-brand-name {
                font-size: 0.92rem;
                font-weight: 700;
                color: #ffffff;
                letter-spacing: 0.04em;
                text-transform: uppercase;
                margin: 0;
            }
            .sidebar-brand-tag {
                font-size: 0.72rem;
                color: #9ca3af;
                margin: 2px 0 0 0;
                letter-spacing: 0.04em;
            }

            /* ───────────────────────────────────────────
               MAIN CONTENT AREA
            ─────────────────────────────────────────── */
            .main .block-container {
                padding: 1.75rem 2rem 3rem 2rem !important;
                max-width: 1440px !important;
            }

            /* ───────────────────────────────────────────
               TOPBAR / PAGE HEADER
            ─────────────────────────────────────────── */
            .page-header {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 1.25rem 1.75rem;
                margin-bottom: 1.5rem;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .page-header-title {
                font-size: 1.25rem;
                font-weight: 700;
                color: #111827;
                margin: 0;
                letter-spacing: -0.01em;
            }
            .page-header-sub {
                font-size: 0.8rem;
                color: #6b7280;
                margin: 3px 0 0 0;
            }
            .page-header-badge {
                background: #111827;
                color: #ffffff;
                font-size: 0.7rem;
                font-weight: 600;
                padding: 0.25rem 0.65rem;
                border-radius: 4px;
                letter-spacing: 0.06em;
                text-transform: uppercase;
            }

            /* ───────────────────────────────────────────
               SECTION HEADINGS
            ─────────────────────────────────────────── */
            .section-label {
                font-size: 0.7rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                color: #6b7280;
                margin: 0 0 0.75rem 0;
                padding-bottom: 0.5rem;
                border-bottom: 1px solid #e5e7eb;
            }
            h1, h2, h3, h4 {
                color: #111827 !important;
                font-weight: 700 !important;
                letter-spacing: -0.01em !important;
            }
            h2 { font-size: 1.15rem !important; }
            h3 { font-size: 0.95rem !important; }

            /* ───────────────────────────────────────────
               METRIC CARDS
            ─────────────────────────────────────────── */
            [data-testid="stMetric"] {
                background-color: #ffffff !important;
                border: 1px solid #e5e7eb !important;
                border-radius: 8px !important;
                padding: 1.1rem 1.25rem !important;
            }
            [data-testid="stMetricLabel"] {
                color: #6b7280 !important;
                font-size: 0.7rem !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.08em !important;
            }
            [data-testid="stMetricValue"] {
                color: #111827 !important;
                font-size: 1.75rem !important;
                font-weight: 800 !important;
                letter-spacing: -0.02em !important;
            }
            [data-testid="stMetricDelta"] {
                font-size: 0.75rem !important;
                font-weight: 500 !important;
            }

            /* ───────────────────────────────────────────
               BUTTONS
            ─────────────────────────────────────────── */
            .stButton > button {
                background-color: #111827 !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 5px !important;
                padding: 0.42rem 1.1rem !important;
                font-size: 0.8rem !important;
                font-weight: 600 !important;
                letter-spacing: 0.04em !important;
                text-transform: uppercase !important;
                transition: background 0.15s ease !important;
                cursor: pointer !important;
            }
            .stButton > button:hover {
                background-color: #1f2937 !important;
            }
            .stButton > button:active {
                background-color: #374151 !important;
            }
            [data-testid="stDownloadButton"] > button {
                background-color: #111827 !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 5px !important;
                font-size: 0.8rem !important;
                font-weight: 600 !important;
                letter-spacing: 0.04em !important;
                text-transform: uppercase !important;
            }
            [data-testid="stDownloadButton"] > button:hover {
                background-color: #1f2937 !important;
            }

            /* ───────────────────────────────────────────
               TABS
            ─────────────────────────────────────────── */
            [data-testid="stTabs"] [role="tablist"] {
                border-bottom: 1px solid #e5e7eb !important;
                gap: 0 !important;
            }
            [data-testid="stTabs"] [role="tab"] {
                font-size: 0.78rem !important;
                font-weight: 600 !important;
                letter-spacing: 0.04em !important;
                text-transform: uppercase !important;
                color: #9ca3af !important;
                padding: 0.6rem 1rem !important;
                border-radius: 0 !important;
                border-bottom: 2px solid transparent !important;
                transition: color 0.15s ease !important;
            }
            [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
                color: #111827 !important;
                border-bottom: 2px solid #111827 !important;
                background: transparent !important;
            }
            [data-testid="stTabs"] [role="tab"]:hover {
                color: #374151 !important;
            }

            /* ───────────────────────────────────────────
               DATA TABLE
            ─────────────────────────────────────────── */
            [data-testid="stDataFrame"] {
                border: 1px solid #e5e7eb !important;
                border-radius: 6px !important;
                overflow: hidden !important;
            }
            [data-testid="stDataFrame"] thead tr th {
                background-color: #f9fafb !important;
                color: #374151 !important;
                font-size: 0.72rem !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.06em !important;
            }

            /* ───────────────────────────────────────────
               FORM CONTROLS
            ─────────────────────────────────────────── */
            .stSelectbox > label,
            .stMultiSelect > label,
            .stNumberInput > label,
            .stRadio > label,
            .stSlider > label {
                font-size: 0.75rem !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.06em !important;
                color: #6b7280 !important;
            }
            .stSelectbox > div > div,
            .stMultiSelect > div > div {
                background-color: #ffffff !important;
                border: 1px solid #d1d5db !important;
                border-radius: 5px !important;
                color: #111827 !important;
                font-size: 13px !important;
            }
            .stFileUploader {
                border: 1.5px dashed #d1d5db !important;
                border-radius: 8px !important;
                background: #f9fafb !important;
                padding: 0.5rem !important;
            }

            /* ───────────────────────────────────────────
               EXPANDER
            ─────────────────────────────────────────── */
            [data-testid="stExpander"] {
                background-color: #ffffff !important;
                border: 1px solid #e5e7eb !important;
                border-radius: 6px !important;
            }
            [data-testid="stExpander"] summary {
                font-size: 0.8rem !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.06em !important;
                color: #374151 !important;
            }

            /* ───────────────────────────────────────────
               ALERTS / NOTIFICATIONS
            ─────────────────────────────────────────── */
            .stAlert {
                border-radius: 6px !important;
                font-size: 0.82rem !important;
            }

            /* ───────────────────────────────────────────
               DIVIDER
            ─────────────────────────────────────────── */
            hr {
                border: none !important;
                border-top: 1px solid #e5e7eb !important;
                margin: 1.75rem 0 !important;
            }

            /* ───────────────────────────────────────────
               SIDEBAR DIVIDER
            ─────────────────────────────────────────── */
            [data-testid="stSidebar"] hr {
                border-top: 1px solid #f3f4f6 !important;
                margin: 0.75rem 0 !important;
            }

            /* ───────────────────────────────────────────
               WELCOME / EMPTY STATE
            ─────────────────────────────────────────── */
            .empty-state {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 10px;
                padding: 4rem 2.5rem;
                text-align: center;
            }
            .empty-state-icon {
                width: 52px;
                height: 52px;
                background: #f3f4f6;
                border-radius: 12px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 1.25rem;
            }
            .empty-state-title {
                font-size: 1.15rem;
                font-weight: 700;
                color: #111827;
                margin: 0 0 0.5rem 0;
            }
            .empty-state-sub {
                font-size: 0.85rem;
                color: #6b7280;
                margin: 0 auto;
                max-width: 380px;
            }
            .feature-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 1rem;
                margin-top: 2.5rem;
                text-align: left;
            }
            .feature-card {
                background: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 1.1rem 1.25rem;
            }
            .feature-card-label {
                font-size: 0.8rem;
                font-weight: 700;
                color: #111827;
                margin: 0 0 0.3rem 0;
                letter-spacing: -0.01em;
            }
            .feature-card-desc {
                font-size: 0.75rem;
                color: #6b7280;
                margin: 0;
                line-height: 1.5;
            }
            .format-note {
                font-size: 0.72rem;
                color: #9ca3af;
                margin-top: 2rem;
                letter-spacing: 0.04em;
                text-transform: uppercase;
            }

            /* ───────────────────────────────────────────
               CARD WRAPPER (generic white panel)
            ─────────────────────────────────────────── */
            .panel {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 1.25rem 1.5rem;
                margin-bottom: 1rem;
            }
            </style>
        """, unsafe_allow_html=True)

    # ──────────────────────────────────────────────────────────────
    # SIDEBAR
    # ──────────────────────────────────────────────────────────────

    def render_sidebar(self):
        """Render the sidebar for data upload and settings."""
        with st.sidebar:
            st.markdown("""
                <div class="sidebar-brand">
                    <p class="sidebar-brand-name">DataInsight Pro</p>
                    <p class="sidebar-brand-tag">Analytics Dashboard</p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown('<p class="section-label">Data Source</p>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Upload a CSV or Excel file",
                type=['csv', 'xlsx', 'xls'],
                label_visibility="collapsed"
            )

            if uploaded_file is not None:
                if self.data_manager.load_data(uploaded_file):
                    self.data_manager.clean_data()
                    self.stats_manager = StatsManager(self.data_manager.data)
                    st.session_state.stats_manager = self.stats_manager
                    st.success("Dataset loaded successfully.")

            st.markdown("---")

    def render_viz_settings(self):
        """Render visualization settings in sidebar."""
        selected_columns = None
        chart_type = None

        if self.data_manager.data is not None:
            with st.sidebar:
                st.markdown('<p class="section-label">Visualization</p>', unsafe_allow_html=True)

                numeric_cols = self.data_manager.get_data_info()['numeric_columns']
                all_cols = self.data_manager.get_data_info()['column_names']

                chart_type = st.selectbox(
                    "Chart Type",
                    ["Histogram", "Scatter Plot", "Line Chart", "Box Plot", "Bar Chart"]
                )

                if chart_type == "Histogram":
                    selected_columns = st.selectbox("Column", numeric_cols)

                elif chart_type == "Scatter Plot":
                    col1, col2 = st.columns(2)
                    with col1:
                        x_col = st.selectbox("X Axis", numeric_cols, key='scatter_x')
                    with col2:
                        y_col = st.selectbox("Y Axis", numeric_cols, key='scatter_y')
                    selected_columns = (x_col, y_col)

                elif chart_type == "Line Chart":
                    col1, col2 = st.columns(2)
                    with col1:
                        x_col = st.selectbox("X Axis", all_cols, key='line_x')
                    with col2:
                        y_col = st.selectbox("Y Axis", numeric_cols, key='line_y')
                    selected_columns = (x_col, y_col)

                elif chart_type == "Box Plot":
                    selected_columns = st.multiselect(
                        "Columns (max 5)",
                        numeric_cols,
                        default=numeric_cols[:min(3, len(numeric_cols))],
                        max_selections=5
                    )

                elif chart_type == "Bar Chart":
                    col1, col2 = st.columns(2)
                    categorical_cols = self.data_manager.get_data_info()['categorical_columns']
                    if not categorical_cols:
                        categorical_cols = all_cols
                    with col1:
                        x_col = st.selectbox("Category", categorical_cols, key='bar_x')
                    with col2:
                        y_col = st.selectbox("Value", numeric_cols, key='bar_y')
                    selected_columns = (x_col, y_col)

                st.markdown("---")

        with st.sidebar:
            st.markdown('<p class="section-label" style="margin-top:0.5rem;">About</p>', unsafe_allow_html=True)
            st.markdown(
                '<p style="font-size:12px;color:#6b7280;line-height:1.6;">'
                'Upload a dataset to explore key metrics, statistical tests, '
                'correlation analysis and interactive charts.'
                '</p>',
                unsafe_allow_html=True
            )

        return selected_columns, chart_type

    # ──────────────────────────────────────────────────────────────
    # DATA OVERVIEW
    # ──────────────────────────────────────────────────────────────

    def render_data_overview(self):
        """Render dataset overview section."""
        if self.data_manager.data is None or self.stats_manager is None:
            return

        st.markdown('<p class="section-label">Dataset Overview</p>', unsafe_allow_html=True)

        # Health score + KPI row
        health = self.stats_manager.calculate_health_score()
        data_info = self.data_manager.get_data_info()

        cols = st.columns(5)
        with cols[0]:
            if health:
                st.metric("Health Score", f"{health['score']:.0f} / 100", delta=health['rating'])
        with cols[1]:
            st.metric("Rows", f"{data_info['rows']:,}")
        with cols[2]:
            st.metric("Columns", f"{data_info['columns']}")
        with cols[3]:
            st.metric("Numeric", f"{len(data_info['numeric_columns'])}")
        with cols[4]:
            st.metric("Categorical", f"{len(data_info['categorical_columns'])}")

        st.markdown("---")

        # Cleaning summary
        cleaning_report = self.data_manager.get_cleaning_report()
        if cleaning_report and (cleaning_report['duplicates_removed'] > 0 or
                                cleaning_report['values_filled'] or
                                cleaning_report['type_conversions']):
            with st.expander("Data Cleaning Report"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Duplicate Rows Removed", cleaning_report['duplicates_removed'])
                with col_b:
                    st.metric("Columns with Imputed Values", len(cleaning_report['values_filled']))
                if cleaning_report['values_filled']:
                    st.write("**Imputed Values**")
                    for col, count in cleaning_report['values_filled'].items():
                        st.write(f"- {col}: {count} value(s)")
                if cleaning_report['type_conversions']:
                    st.write("**Type Conversions**")
                    for conversion in cleaning_report['type_conversions']:
                        st.write(f"- {conversion}")

        # Data types pie + column summary
        c1, c2 = st.columns([1, 2])

        with c1:
            st.markdown('<p class="section-label">Column Types</p>', unsafe_allow_html=True)
            type_counts = self.data_manager.data.dtypes.astype(str).value_counts()
            fig = self.visualizer.create_pie_chart(
                labels=type_counts.index.tolist(),
                values=type_counts.values.tolist(),
                title=""
            )
            fig.update_layout(height=320, margin=dict(t=10, b=10, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown('<p class="section-label">Column Summary</p>', unsafe_allow_html=True)
            master_df = self.stats_manager.get_comprehensive_summary()
            if not master_df.empty:
                master_df['Missing (%)'] = master_df['Missing (%)'].map('{:.1f}%'.format)
                st.dataframe(
                    master_df,
                    use_container_width=True,
                    height=320,
                    hide_index=True,
                    column_config={
                        "Missing (%)": st.column_config.ProgressColumn(
                            "Missing (%)",
                            format="%s",
                            min_value=0,
                            max_value=100,
                        ),
                    }
                )

    # ──────────────────────────────────────────────────────────────
    # TIME SERIES
    # ──────────────────────────────────────────────────────────────

    def render_time_series_analysis(self):
        """Render time series analysis section if date columns exist."""
        date_cols = self.data_manager.identify_date_columns()
        if not date_cols or self.stats_manager is None:
            return

        st.markdown('<p class="section-label">Time Series Analysis</p>', unsafe_allow_html=True)
        st.info("Automated trend analysis based on detected date columns.")

        col1, col2, col3 = st.columns(3)
        with col1:
            date_col = st.selectbox("Date Column", date_cols)
        numeric_cols = self.data_manager.get_data_info()['numeric_columns']
        if not numeric_cols:
            st.warning("No numeric columns available for time series analysis.")
            return
        with col2:
            val_col = st.selectbox("Metric", numeric_cols)
        with col3:
            freq = st.selectbox(
                "Frequency",
                ["D", "W", "M", "Q", "Y"],
                format_func=lambda x: {"D": "Daily", "W": "Weekly", "M": "Monthly",
                                       "Q": "Quarterly", "Y": "Yearly"}[x]
            )

        ts_data = self.stats_manager.get_time_series_data(date_col, val_col, freq)
        if not ts_data.empty:
            fig = self.visualizer.create_time_series_chart(ts_data, date_col, val_col)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

    # ──────────────────────────────────────────────────────────────
    # DECISION SUPPORT
    # ──────────────────────────────────────────────────────────────

    def render_decision_support(self):
        """Render decision support tools section."""
        if self.stats_manager is None:
            return

        st.markdown('<p class="section-label">Decision Support Tools</p>', unsafe_allow_html=True)

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "Outlier Detection",
            "Data Filtering",
            "Grouped Analysis",
            "Top Relationships",
            "Regression",
            "Hypothesis Testing"
        ])

        # ── Outlier Detection ──
        with tab1:
            st.markdown("#### Outlier Detection — IQR Method")
            st.info(
                "Outliers are data points that deviate significantly from the rest of the "
                "distribution. They may indicate measurement errors or genuine anomalies."
            )
            outliers = self.stats_manager.get_outliers()
            if outliers:
                col_select = st.selectbox("Select Column", list(outliers.keys()))
                if col_select:
                    st.warning(f"{len(outliers[col_select])} potential outlier(s) found in '{col_select}'.")
                    st.dataframe(outliers[col_select], use_container_width=True)
            else:
                st.success("No statistical outliers detected in numeric columns.")
            insight = self.stats_manager.generate_outlier_insight()
            st.info(insight)

        # ── Data Filtering ──
        with tab2:
            st.markdown("#### Interactive Data Filtering")
            if self.data_manager.data is not None:
                numeric_cols = self.data_manager.get_data_info()['numeric_columns']
                col1, col2, col3 = st.columns(3)
                with col1:
                    filter_col = st.selectbox("Column", numeric_cols, key='filter_col')
                with col2:
                    condition = st.selectbox("Condition", [">", "<", ">=", "<=", "==", "!="])
                with col3:
                    val = st.number_input("Value", value=0.0)
                query = f"`{filter_col}` {condition} {val}"
                try:
                    filtered_data = self.data_manager.data.query(query)
                    st.markdown(
                        f"**{len(filtered_data):,} rows** match: `{filter_col} {condition} {val}`"
                    )
                    st.dataframe(filtered_data, use_container_width=True)
                except Exception as e:
                    st.error(f"Filter error: {e}")

        # ── Grouped Analysis ──
        with tab3:
            st.markdown("#### Grouped Analysis")
            st.info("Aggregate data by category to compare performance or distribution across groups.")
            if self.data_manager.data is not None:
                cat_cols = self.data_manager.get_data_info()['categorical_columns']
                num_cols = self.data_manager.get_data_info()['numeric_columns']
                if cat_cols and num_cols:
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        group_col = st.selectbox("Group By", cat_cols)
                    with c2:
                        val_col = st.selectbox("Metric", num_cols)
                    with c3:
                        agg_func = st.selectbox("Aggregation", ["mean", "sum", "count", "min", "max"])
                    grouped_df = self.stats_manager.get_grouped_stats(group_col, val_col, agg_func)
                    if not grouped_df.empty:
                        col_left, col_right = st.columns([1, 2])
                        with col_left:
                            st.dataframe(grouped_df, use_container_width=True, hide_index=True)
                        with col_right:
                            fig = self.visualizer.create_horizontal_bar_chart(
                                grouped_df,
                                x_col=grouped_df.columns[1],
                                y_col=grouped_df.columns[0],
                                title=f"{grouped_df.columns[1]} by {grouped_df.columns[0]}"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Both categorical and numeric columns are required for grouped analysis.")

        # ── Top Relationships ──
        with tab4:
            st.markdown("#### Top Relationships — Pearson Correlation")
            st.info("Identifies the strongest positive and negative linear relationships in your dataset.")
            top_corr = self.stats_manager.get_top_correlations()
            if not top_corr.empty:
                st.dataframe(top_corr, use_container_width=True, hide_index=True)
                insight = self.stats_manager.generate_correlation_insight()
                st.info(insight)
            else:
                st.info("Insufficient numeric data to calculate correlations.")

        # ── Regression ──
        with tab5:
            st.markdown("#### Linear Regression Analysis")
            st.info("Models the linear relationship between two variables and quantifies fit quality.")
            if self.data_manager.data is not None:
                numeric_cols = self.data_manager.get_data_info()['numeric_columns']
                if len(numeric_cols) >= 2:
                    c1, c2 = st.columns(2)
                    with c1:
                        x_var = st.selectbox("Independent Variable (X)", numeric_cols, key='reg_x')
                    with c2:
                        y_var = st.selectbox("Dependent Variable (Y)", numeric_cols, index=1, key='reg_y')
                    if x_var != y_var:
                        reg_results = self.stats_manager.calculate_regression(x_var, y_var)
                        if reg_results:
                            m1, m2 = st.columns(2)
                            with m1:
                                st.metric("Equation", reg_results['equation'])
                            with m2:
                                st.metric("R-Squared", f"{reg_results['r_squared']:.4f}")
                            fig = self.visualizer.create_regression_chart(
                                self.data_manager.data, x_var, y_var,
                                reg_results['slope'], reg_results['intercept']
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.error("Unable to compute regression model for selected variables.")
                    else:
                        st.warning("Please select different variables for X and Y.")
                else:
                    st.warning("At least two numeric columns are required for regression analysis.")

        # ── Hypothesis Testing ──
        with tab6:
            st.markdown("#### Hypothesis Testing")
            st.info("Statistical tests to validate assumptions or compare groups in your data.")
            test_type = st.radio(
                "Select Test",
                ["Normality Test (Shapiro-Wilk)", "Independent T-Test"],
                horizontal=True
            )

            if test_type == "Normality Test (Shapiro-Wilk)":
                st.markdown("**Normality Test** — determines whether data follows a Gaussian distribution.")
                numeric_cols = self.data_manager.get_data_info()['numeric_columns']
                if numeric_cols:
                    col_to_test = st.selectbox("Column", numeric_cols, key='norm_col')
                    if st.button("Run Normality Test"):
                        results = self.stats_manager.perform_normality_test(col_to_test)
                        if results:
                            if 'warning' in results:
                                st.warning(results['warning'])
                            c1, c2 = st.columns(2)
                            with c1:
                                st.metric("Test Statistic", f"{results['statistic']:.4f}")
                            with c2:
                                st.metric("P-Value", f"{results['p_value']:.4f}")
                            if results['is_normal']:
                                st.success(
                                    f"P-Value > 0.05. The distribution of '{col_to_test}' "
                                    "is consistent with normality."
                                )
                            else:
                                st.warning(
                                    f"P-Value <= 0.05. The distribution of '{col_to_test}' "
                                    "deviates significantly from normality."
                                )
                else:
                    st.warning("No numeric columns available.")

            elif test_type == "Independent T-Test":
                st.markdown("**Independent T-Test** — compares the means of two independent groups.")
                cat_cols = self.data_manager.get_data_info()['categorical_columns']
                num_cols = self.data_manager.get_data_info()['numeric_columns']
                if cat_cols and num_cols:
                    c1, c2 = st.columns(2)
                    with c1:
                        group_col = st.selectbox("Grouping Column (2 groups)", cat_cols, key='ttest_group')
                    with c2:
                        val_col = st.selectbox("Value Column", num_cols, key='ttest_val')
                    if st.button("Run T-Test"):
                        results = self.stats_manager.perform_ttest(group_col, val_col)
                        if 'error' in results:
                            st.error(results['error'])
                        else:
                            if 'warnings' in results:
                                for warning in results['warnings']:
                                    st.warning(warning)
                            m1, m2, m3 = st.columns(3)
                            with m1:
                                st.metric("Comparison", f"{results['group1']} vs {results['group2']}")
                            with m2:
                                st.metric("Test Statistic", f"{results['statistic']:.4f}")
                            with m3:
                                st.metric("P-Value", f"{results['p_value']:.4f}")
                            if results['significant']:
                                st.success(
                                    "P-Value < 0.05. There is a statistically significant "
                                    "difference between the two groups."
                                )
                            else:
                                st.info(
                                    "P-Value >= 0.05. No statistically significant "
                                    "difference was detected between the groups."
                                )
                else:
                    st.warning("Both categorical and numeric columns are required for the T-Test.")

    # ──────────────────────────────────────────────────────────────
    # DYNAMIC CHARTS
    # ──────────────────────────────────────────────────────────────

    def render_dynamic_charts(self, selected_columns, chart_type):
        """Render user-selected charts."""
        if selected_columns is None or self.data_manager.data is None:
            return

        st.markdown('<p class="section-label">Dynamic Visualizations</p>', unsafe_allow_html=True)

        try:
            if chart_type == "Histogram" and selected_columns:
                fig = self.visualizer.create_histogram(self.data_manager.data, selected_columns)
                st.plotly_chart(fig, use_container_width=True)
                if self.stats_manager:
                    insight = self.stats_manager.generate_distribution_insight(selected_columns)
                    st.info(insight)

            elif chart_type == "Scatter Plot" and selected_columns:
                fig = self.visualizer.create_scatter(
                    self.data_manager.data, selected_columns[0], selected_columns[1]
                )
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Line Chart" and selected_columns:
                fig = self.visualizer.create_line_chart(
                    self.data_manager.data, selected_columns[0], selected_columns[1]
                )
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Box Plot" and selected_columns:
                fig = self.visualizer.create_box_plot(self.data_manager.data, selected_columns)
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Bar Chart" and selected_columns:
                fig = self.visualizer.create_bar_chart(
                    self.data_manager.data, selected_columns[0], selected_columns[1]
                )
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Chart error: {e}")

    # ──────────────────────────────────────────────────────────────
    # MAIN RUN
    # ──────────────────────────────────────────────────────────────

    def run(self):
        """Run the dashboard application."""
        self.render_sidebar()
        selected_columns, chart_type = self.render_viz_settings()

        # Page header
        st.markdown("""
            <div class="page-header">
                <div>
                    <p class="page-header-title">Data Analysis Dashboard</p>
                    <p class="page-header-sub">
                        Upload a dataset to unlock automated insights, statistical analysis,
                        and interactive visualisations.
                    </p>
                </div>
                <span class="page-header-badge">Analytics</span>
            </div>
        """, unsafe_allow_html=True)

        if self.data_manager.data is not None:
            self.render_data_overview()
            st.markdown("---")
            self.render_decision_support()
            st.markdown("---")
            self.render_dynamic_charts(selected_columns, chart_type)

            # Raw data / export
            st.markdown('<p class="section-label">Raw Data &amp; Export</p>', unsafe_allow_html=True)
            with st.expander("View and Filter Dataset"):
                all_cols = self.data_manager.get_data_info()['column_names']
                show_cols = st.multiselect("Visible Columns", all_cols, default=all_cols)
                df_to_show = self.data_manager.data.copy()

                col1, col2 = st.columns(2)
                with col1:
                    filter_col = st.selectbox("Filter by Column", ["None"] + all_cols, key='raw_filter_col')

                if filter_col != "None":
                    with col2:
                        if pd.api.types.is_numeric_dtype(df_to_show[filter_col]):
                            min_val = float(df_to_show[filter_col].min())
                            max_val = float(df_to_show[filter_col].max())
                            val_range = st.slider(
                                f"Range for {filter_col}", min_val, max_val, (min_val, max_val)
                            )
                            df_to_show = df_to_show[
                                (df_to_show[filter_col] >= val_range[0]) &
                                (df_to_show[filter_col] <= val_range[1])
                            ]
                        else:
                            unique_vals = df_to_show[filter_col].unique()
                            selected_vals = st.multiselect(
                                f"Values for {filter_col}", unique_vals, default=unique_vals
                            )
                            df_to_show = df_to_show[df_to_show[filter_col].isin(selected_vals)]

                st.markdown(f"Showing **{len(df_to_show):,}** rows")
                st.dataframe(df_to_show[show_cols], height=400, use_container_width=True)

                csv = df_to_show[show_cols].to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name='export.csv',
                    mime='text/csv',
                )

        else:
            # Empty / welcome state
            st.markdown("""
                <div class="empty-state">
                    <div class="empty-state-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none"
                             xmlns="http://www.w3.org/2000/svg">
                            <path d="M4 4h16v4H4V4zm0 6h16v10H4V10zm4 2v6m4-6v6m4-6v6"
                                  stroke="#6b7280" stroke-width="1.5" stroke-linecap="round"
                                  stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <p class="empty-state-title">No dataset loaded</p>
                    <p class="empty-state-sub">
                        Upload a CSV or Excel file using the sidebar panel on the left
                        to begin your analysis.
                    </p>
                    <div class="feature-grid">
                        <div class="feature-card">
                            <p class="feature-card-label">Automated Cleaning</p>
                            <p class="feature-card-desc">Duplicate removal and missing value
                            imputation with a full change log.</p>
                        </div>
                        <div class="feature-card">
                            <p class="feature-card-label">Dataset Health Score</p>
                            <p class="feature-card-desc">Quality rating based on completeness,
                            duplicates and outlier prevalence.</p>
                        </div>
                        <div class="feature-card">
                            <p class="feature-card-label">Statistical Testing</p>
                            <p class="feature-card-desc">Normality tests, T-tests and
                            Pearson correlation analysis.</p>
                        </div>
                        <div class="feature-card">
                            <p class="feature-card-label">Interactive Charts</p>
                            <p class="feature-card-desc">Histograms, scatter plots, regression,
                            heatmaps and more.</p>
                        </div>
                        <div class="feature-card">
                            <p class="feature-card-label">Decision Support</p>
                            <p class="feature-card-desc">Outlier detection, group comparison
                            and dynamic filtering tools.</p>
                        </div>
                        <div class="feature-card">
                            <p class="feature-card-label">Export</p>
                            <p class="feature-card-desc">Download filtered or cleaned datasets
                            as CSV with one click.</p>
                        </div>
                    </div>
                    <p class="format-note">Supported formats: CSV &nbsp;·&nbsp; XLSX &nbsp;·&nbsp; XLS</p>
                </div>
            """, unsafe_allow_html=True)
