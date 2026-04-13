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
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Initialize components
        if 'data_manager' not in st.session_state:
            st.session_state.data_manager = DataManager()
        if 'visualizer' not in st.session_state:
            st.session_state.visualizer = Visualizer()
        if 'stats_manager' not in st.session_state:
            st.session_state.stats_manager = None
            
        self.data_manager = st.session_state.data_manager
        self.visualizer = st.session_state.visualizer
        self.stats_manager = st.session_state.stats_manager
        
        # Apply custom CSS
        self._apply_custom_css()
        
    def _apply_custom_css(self):
        """Apply custom CSS styling."""
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

            /* ── Global ── */
            html, body, .stApp {
                background-color: #f5f6fa !important;
                color: #1a1a2e !important;
                font-family: 'Inter', sans-serif !important;
            }

            /* ── Sidebar ── */
            [data-testid="stSidebar"] {
                background-color: #ffffff !important;
                border-right: 1px solid #e2e6ea !important;
            }
            [data-testid="stSidebar"] .stMarkdown,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] p {
                color: #1a1a2e !important;
            }

            /* ── Sidebar header ── */
            [data-testid="stSidebar"] h1 {
                font-size: 1.3rem !important;
                font-weight: 700 !important;
                letter-spacing: 0.02em !important;
                color: #1a1a2e !important;
                padding-bottom: 0.25rem;
            }

            /* ── Buttons — solid black ── */
            .stButton > button {
                background-color: #111111 !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 6px !important;
                padding: 0.45rem 1.2rem !important;
                font-weight: 600 !important;
                font-size: 0.85rem !important;
                letter-spacing: 0.03em !important;
                transition: background 0.2s ease, transform 0.1s ease !important;
            }
            .stButton > button:hover {
                background-color: #333333 !important;
                transform: translateY(-1px) !important;
            }
            .stButton > button:active {
                transform: translateY(0) !important;
            }

            /* ── Download button ── */
            [data-testid="stDownloadButton"] > button {
                background-color: #111111 !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 6px !important;
                font-weight: 600 !important;
            }
            [data-testid="stDownloadButton"] > button:hover {
                background-color: #333333 !important;
            }

            /* ── Metric cards ── */
            [data-testid="stMetric"] {
                background-color: #ffffff !important;
                border: 1px solid #e2e6ea !important;
                border-radius: 10px !important;
                padding: 1rem 1.25rem !important;
                box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
            }
            [data-testid="stMetricLabel"] {
                color: #6b7280 !important;
                font-size: 0.78rem !important;
                font-weight: 500 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.06em !important;
            }
            [data-testid="stMetricValue"] {
                color: #111111 !important;
                font-size: 1.65rem !important;
                font-weight: 700 !important;
            }

            /* ── Section headings ── */
            h1, h2, h3, h4 {
                color: #111111 !important;
                font-weight: 700 !important;
            }
            h2 { font-size: 1.4rem !important; }
            h3 { font-size: 1.1rem !important; }

            /* ── Tabs ── */
            [data-testid="stTabs"] [role="tab"] {
                font-weight: 600 !important;
                color: #6b7280 !important;
                font-size: 0.85rem !important;
                letter-spacing: 0.02em !important;
            }
            [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
                color: #111111 !important;
                border-bottom: 2px solid #111111 !important;
            }

            /* ── Dataframe / Table ── */
            [data-testid="stDataFrame"] {
                border: 1px solid #e2e6ea !important;
                border-radius: 8px !important;
                overflow: hidden !important;
            }

            /* ── Input / Select widgets ── */
            .stSelectbox > div > div,
            .stMultiSelect > div > div,
            .stNumberInput > div > div > input {
                background-color: #ffffff !important;
                border: 1px solid #d1d5db !important;
                border-radius: 6px !important;
                color: #111111 !important;
            }

            /* ── Expander ── */
            [data-testid="stExpander"] {
                background-color: #ffffff !important;
                border: 1px solid #e2e6ea !important;
                border-radius: 8px !important;
            }

            /* ── Info / Warning / Success boxes ── */
            [data-testid="stNotification"],
            .stAlert {
                border-radius: 8px !important;
            }

            /* ── Horizontal divider ── */
            hr {
                border-color: #e2e6ea !important;
                margin: 1.5rem 0 !important;
            }

            /* ── Main content area ── */
            .main .block-container {
                padding-top: 2rem !important;
                padding-bottom: 2rem !important;
                max-width: 1400px !important;
            }

            /* ── Page title banner ── */
            .dashboard-header {
                background: #ffffff;
                border: 1px solid #e2e6ea;
                border-radius: 10px;
                padding: 1.5rem 2rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 1px 4px rgba(0,0,0,0.06);
            }
            .dashboard-header h1 {
                margin: 0 !important;
                font-size: 1.6rem !important;
                font-weight: 700 !important;
                color: #111111 !important;
            }
            .dashboard-header p {
                margin: 0.25rem 0 0 0 !important;
                color: #6b7280 !important;
                font-size: 0.9rem !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
    def render_sidebar(self):
        """Render the sidebar for data upload and settings."""
        with st.sidebar:
            st.markdown("### 📊 Data Dashboard")
            st.caption("Professional Analytics Platform")
            st.markdown("---")
            
            # File Upload
            st.subheader("Data Upload")
            uploaded_file = st.file_uploader(
                "Upload CSV or Excel file", 
                type=['csv', 'xlsx', 'xls']
            )
            
            if uploaded_file is not None:
                if self.data_manager.load_data(uploaded_file):
                    self.data_manager.clean_data()
                    # Initialize StatsManager with the loaded data
                    self.stats_manager = StatsManager(self.data_manager.data)
                    st.session_state.stats_manager = self.stats_manager
                    st.success("Data loaded successfully!")
                    
            st.markdown("---")
            
    def render_viz_settings(self):
        """
        Render visualization settings in sidebar.
        
        Returns:
            tuple: (selected_columns, chart_type)
        """
        selected_columns = None
        chart_type = None
        
        if self.data_manager.data is not None:
            with st.sidebar:
                st.markdown("## Visualization Settings")
                
                numeric_cols = self.data_manager.get_data_info()['numeric_columns']
                all_cols = self.data_manager.get_data_info()['column_names']
                
                chart_type = st.selectbox(
                    "Select Chart Type",
                    ["Histogram", "Scatter Plot", "Line Chart", "Box Plot", "Bar Chart"],
                    help="Choose the visualization type"
                )
                
                if chart_type == "Histogram":
                    selected_columns = st.selectbox("Select Column", numeric_cols)
                    
                elif chart_type == "Scatter Plot":
                    col1, col2 = st.columns(2)
                    with col1:
                        x_col = st.selectbox("X-axis", numeric_cols, key='scatter_x')
                    with col2:
                        y_col = st.selectbox("Y-axis", numeric_cols, key='scatter_y')
                    selected_columns = (x_col, y_col)
                    
                elif chart_type == "Line Chart":
                    col1, col2 = st.columns(2)
                    with col1:
                        x_col = st.selectbox("X-axis", all_cols, key='line_x')
                    with col2:
                        y_col = st.selectbox("Y-axis", numeric_cols, key='line_y')
                    selected_columns = (x_col, y_col)
                    
                elif chart_type == "Box Plot":
                    selected_columns = st.multiselect(
                        "Select Columns (max 5)",
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
                        x_col = st.selectbox("Category (X)", categorical_cols, key='bar_x')
                    with col2:
                        y_col = st.selectbox("Value (Y)", numeric_cols, key='bar_y')
                    selected_columns = (x_col, y_col)
            
                st.markdown("---")
        
        with st.sidebar:
            st.markdown("### About")
            st.info("""
                **Data Analysis Dashboard**
                
                Upload your dataset and explore it with:
                - Key metrics
                - Correlation analysis
                - Interactive visualizations
                
                Built with Streamlit & Plotly
            """)
            
        return selected_columns, chart_type
    
    def render_data_overview(self):
        """
        Render comprehensive data overview section (Metrics + Master Table).
        """
        if self.data_manager.data is None or self.stats_manager is None:
            return
            
        st.markdown("## Dataset Overview")
        
        # Dataset Health Score
        health = self.stats_manager.calculate_health_score()
        if health:
            col_health, col_spacer = st.columns([1, 3])
            with col_health:
                # Determine color based on rating
                if health['rating'] in ['Excellent', 'Good']:
                    rating_color = "🟢"
                elif health['rating'] == 'Fair':
                    rating_color = "🟡"
                else:
                    rating_color = "🔴"
                
                st.metric(
                    "Dataset Health", 
                    f"{health['score']:.0f}/100"
                )
                st.markdown(f"{rating_color} **{health['rating']}**")
        
        # Key Metrics Cards
        data_info = self.data_manager.get_data_info()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", f"{data_info['rows']:,}")
        with col2:
            st.metric("Total Columns", f"{data_info['columns']}")
        with col3:
            st.metric("Numeric Columns", f"{len(data_info['numeric_columns'])}")
        with col4:
            st.metric("Categorical Columns", f"{len(data_info['categorical_columns'])}")
            
        st.markdown("---")
        
        # Data Cleaning Summary
        cleaning_report = self.data_manager.get_cleaning_report()
        if cleaning_report and (cleaning_report['duplicates_removed'] > 0 or 
                               cleaning_report['values_filled'] or 
                               cleaning_report['type_conversions']):
            with st.expander("Data Cleaning Summary", expanded=False):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Duplicate Rows Removed", cleaning_report['duplicates_removed'])
                with col_b:
                    st.metric("Columns with Filled Values", len(cleaning_report['values_filled']))
                
                if cleaning_report['values_filled']:
                    st.write("**Values Filled:**")
                    for col, count in cleaning_report['values_filled'].items():
                        st.write(f"- {col}: {count} value(s)")
                
                if cleaning_report['type_conversions']:
                    st.write("**Type Conversions:**")
                    for conversion in cleaning_report['type_conversions']:
                        st.write(f"- {conversion}")

        # 2. Master Summary (Chart + Table)
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.markdown("### Data Types")
            type_counts = self.data_manager.data.dtypes.astype(str).value_counts()
            fig = self.visualizer.create_pie_chart(
                labels=type_counts.index.tolist(),
                values=type_counts.values.tolist(),
                title=""
            )
            fig.update_layout(height=350, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            st.markdown("### Comprehensive Column Analysis")
            master_df = self.stats_manager.get_comprehensive_summary()
            
            if not master_df.empty:
                # Format Percentage
                master_df['Missing (%)'] = master_df['Missing (%)'].map('{:.1f}%'.format)
                
                st.dataframe(
                    master_df, 
                    use_container_width=True, 
                    height=350, 
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

    def render_time_series_analysis(self):
        """
        Render time series analysis section if date columns exist.
        """
        date_cols = self.data_manager.identify_date_columns()
        
        if not date_cols or self.stats_manager is None:
            return
            
        st.markdown("## Time Series Analysis")
        st.info("Automated trend analysis based on detected date columns.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date_col = st.selectbox("Select Date Column", date_cols)
        
        numeric_cols = self.data_manager.get_data_info()['numeric_columns']
        if not numeric_cols:
            st.warning("No numeric columns to analyze over time.")
            return
            
        with col2:
            val_col = st.selectbox("Select Value to Track", numeric_cols)
            
        with col3:
            freq = st.selectbox("Frequency", ["D", "W", "M", "Q", "Y"], format_func=lambda x: {"D": "Daily", "W": "Weekly", "M": "Monthly", "Q": "Quarterly", "Y": "Yearly"}[x])
            
        ts_data = self.stats_manager.get_time_series_data(date_col, val_col, freq)
        
        if not ts_data.empty:
            fig = self.visualizer.create_time_series_chart(ts_data, date_col, f"{val_col}")
            st.plotly_chart(fig, use_container_width=True)
            
        st.markdown("---")

    def render_decision_support(self):
        """
        Render decision support tools section.
        """
        if self.stats_manager is None:
            return

        st.markdown("## Decision Support Tools")
        
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Outlier Detection", "Data Filtering", "Grouped Analysis", "Top Relationships", "Regression Analysis", "Hypothesis Testing"])
        
        with tab1:
            st.markdown("### Statistical Outliers (IQR Method)")
            st.info("Outliers are data points that differ significantly from other observations. They may indicate variability in measurement or experimental errors.")
            
            outliers = self.stats_manager.get_outliers()
            
            if outliers:
                col_select = st.selectbox("Select Column to Inspect", list(outliers.keys()))
                
                if col_select:
                    st.warning(f"Found {len(outliers[col_select])} potential outliers in '{col_select}'")
                    st.dataframe(outliers[col_select], use_container_width=True)
            else:
                st.success("No statistical outliers detected in numeric columns.")
            
            # Add outlier insight
            insight = self.stats_manager.generate_outlier_insight()
            st.info(insight)
                
        with tab2:
            st.markdown("### Interactive Data Filtering")
            
            if self.data_manager.data is not None:
                numeric_cols = self.data_manager.get_data_info()['numeric_columns']
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    filter_col = st.selectbox("Filter Column", numeric_cols, key='filter_col')
                with col2:
                    condition = st.selectbox("Condition", [">", "<", ">=", "<=", "==", "!="])
                with col3:
                    val = st.number_input("Value", value=0.0)
                
                # Apply filter
                query = f"`{filter_col}` {condition} {val}"
                try:
                    filtered_data = self.data_manager.data.query(query)
                    st.markdown(f"**Results: {len(filtered_data)} rows match condition `{filter_col} {condition} {val}`**")
                    st.dataframe(filtered_data, use_container_width=True)
                except Exception as e:
                    st.error(f"Error filtering data: {e}")

        with tab3:
            st.markdown("### Grouped Analysis")
            st.info("Aggregate data by categories to compare performance or distribution.")
            
            if self.data_manager.data is not None:
                cat_cols = self.data_manager.get_data_info()['categorical_columns']
                num_cols = self.data_manager.get_data_info()['numeric_columns']
                
                if cat_cols and num_cols:
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        group_col = st.selectbox("Group By", cat_cols)
                    with c2:
                        val_col = st.selectbox("Analyze Value", num_cols)
                    with c3:
                        agg_func = st.selectbox("Aggregation", ["mean", "sum", "count", "min", "max"])
                        
                    grouped_df = self.stats_manager.get_grouped_stats(group_col, val_col, agg_func)
                    
                    if not grouped_df.empty:
                        col_left, col_right = st.columns([1, 2])
                        with col_left:
                            st.dataframe(grouped_df, use_container_width=True, hide_index=True)
                        with col_right:
                            # Horizontal bar chart for better readability of categories
                            fig = self.visualizer.create_horizontal_bar_chart(
                                grouped_df, 
                                x_col=grouped_df.columns[1], 
                                y_col=grouped_df.columns[0],
                                title=f"{grouped_df.columns[1]} by {grouped_df.columns[0]}"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Need both categorical and numeric columns for grouped analysis.")

        with tab4:
            st.markdown("### Top Relationships")
            st.info("Identify the strongest positive and negative correlations in your dataset.")
            
            top_corr = self.stats_manager.get_top_correlations()
            if not top_corr.empty:
                st.dataframe(top_corr, use_container_width=True, hide_index=True)
                # Add correlation insight
                insight = self.stats_manager.generate_correlation_insight()
                st.info(insight)
            else:
                st.info("Not enough numeric data to calculate correlations.")

        with tab5:
            st.markdown("### Regression Analysis")
            st.info("Model the relationship between two variables using Linear Regression.")
            
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
                            st.success(f"**Model:** {reg_results['equation']}")
                            st.metric("R-Squared (Fit Quality)", f"{reg_results['r_squared']:.4f}")
                            
                            fig = self.visualizer.create_regression_chart(
                                self.data_manager.data, x_var, y_var, 
                                reg_results['slope'], reg_results['intercept']
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.error("Could not calculate regression model.")
                    else:
                        st.warning("Please select different variables for X and Y.")
                else:
                    st.warning("Need at least two numeric columns for regression analysis.")

        with tab6:
            st.markdown("### Hypothesis Testing")
            st.info("Perform statistical tests to validate assumptions about your data.")
            
            test_type = st.radio("Select Test", ["Normality Test (Shapiro-Wilk)", "Independent T-Test"])
            
            if test_type == "Normality Test (Shapiro-Wilk)":
                st.markdown("#### Normality Test")
                st.write("Checks if a distribution is Gaussian (Normal).")
                
                numeric_cols = self.data_manager.get_data_info()['numeric_columns']
                if numeric_cols:
                    col_to_test = st.selectbox("Select Column", numeric_cols, key='norm_col')
                    if st.button("Run Normality Test"):
                        results = self.stats_manager.perform_normality_test(col_to_test)
                        if results:
                            # Display warning if present
                            if 'warning' in results:
                                st.warning(results['warning'])
                            
                            st.write(f"**Statistic:** {results['statistic']:.4f}")
                            st.write(f"**P-Value:** {results['p_value']:.4f}")
                            if results['is_normal']:
                                st.success(f"P-Value > 0.05. The data in '{col_to_test}' looks Normal (Gaussian).")
                            else:
                                st.warning(f"P-Value <= 0.05. The data in '{col_to_test}' does NOT look Normal.")
                else:
                    st.warning("No numeric columns available.")
                    
            elif test_type == "Independent T-Test":
                st.markdown("#### Independent T-Test")
                st.write("Compares the means of two independent groups.")
                
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
                            # Display warnings if present
                            if 'warnings' in results:
                                for warning in results['warnings']:
                                    st.warning(warning)
                            
                            st.write(f"**Comparison:** {results['group1']} vs {results['group2']}")
                            st.write(f"**Statistic:** {results['statistic']:.4f}")
                            st.write(f"**P-Value:** {results['p_value']:.4f}")
                            if results['significant']:
                                st.success("P-Value < 0.05. There is a SIGNIFICANT difference between the groups.")
                            else:
                                st.info("P-Value >= 0.05. There is NO significant difference between the groups.")
                else:
                    st.warning("Need both categorical and numeric columns.")
    
    def render_dynamic_charts(self, selected_columns, chart_type):
        """
        Render user-selected charts dynamically.
        
        Args:
            selected_columns: Selected column(s) for visualization
            chart_type: Type of chart to display
        """
        if selected_columns is None or self.data_manager.data is None:
            return
        
        st.markdown("## Dynamic Visualizations")
        
        try:
            if chart_type == "Histogram" and selected_columns:
                fig = self.visualizer.create_histogram(self.data_manager.data, selected_columns)
                st.plotly_chart(fig, use_container_width=True)
                # Add distribution insight
                if self.stats_manager:
                    insight = self.stats_manager.generate_distribution_insight(selected_columns)
                    st.info(insight)
                
            elif chart_type == "Scatter Plot" and selected_columns:
                fig = self.visualizer.create_scatter(self.data_manager.data, selected_columns[0], selected_columns[1])
                st.plotly_chart(fig, use_container_width=True)
                
            elif chart_type == "Line Chart" and selected_columns:
                fig = self.visualizer.create_line_chart(self.data_manager.data, selected_columns[0], selected_columns[1])
                st.plotly_chart(fig, use_container_width=True)
                
            elif chart_type == "Box Plot" and selected_columns:
                fig = self.visualizer.create_box_plot(self.data_manager.data, selected_columns)
                st.plotly_chart(fig, use_container_width=True)
                
            elif chart_type == "Bar Chart" and selected_columns:
                fig = self.visualizer.create_bar_chart(self.data_manager.data, selected_columns[0], selected_columns[1])
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")

    def run(self):
        """Run the dashboard application."""
        self.render_sidebar()
        
        selected_columns, chart_type = self.render_viz_settings()

        # Professional page header
        st.markdown("""
            <div class="dashboard-header">
                <h1>📊 Data Analysis Dashboard</h1>
                <p>Upload a dataset to unlock automated insights, statistical analysis, and interactive visualisations.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Render main dashboard content
        if self.data_manager.data is not None:
            # Render comprehensive data overview (Metrics + Master Table)
            self.render_data_overview()
            
            st.markdown("---")
            
            # Render Time Series Analysis (if applicable)
            # self.render_time_series_analysis()
            
            # Render decision support tools
            self.render_decision_support()
            
            st.markdown("---")
            
            # Render dynamic charts
            self.render_dynamic_charts(selected_columns, chart_type)
            
            # Show raw data in expander
            # Show raw data with advanced options
            st.markdown("## Raw Data & Export")
            with st.expander("View & Filter Data", expanded=False):
                # Advanced Filtering
                st.markdown("### Advanced Filters")
                
                # Column selection for display
                all_cols = self.data_manager.get_data_info()['column_names']
                show_cols = st.multiselect("Select Columns to View", all_cols, default=all_cols)
                
                # Row filtering
                df_to_show = self.data_manager.data.copy()
                
                col1, col2 = st.columns(2)
                with col1:
                    filter_col = st.selectbox("Filter by Column", ["None"] + all_cols, key='raw_filter_col')
                
                if filter_col != "None":
                    with col2:
                        if pd.api.types.is_numeric_dtype(df_to_show[filter_col]):
                            min_val = float(df_to_show[filter_col].min())
                            max_val = float(df_to_show[filter_col].max())
                            val_range = st.slider(f"Range for {filter_col}", min_val, max_val, (min_val, max_val))
                            df_to_show = df_to_show[(df_to_show[filter_col] >= val_range[0]) & (df_to_show[filter_col] <= val_range[1])]
                        else:
                            unique_vals = df_to_show[filter_col].unique()
                            selected_vals = st.multiselect(f"Select values for {filter_col}", unique_vals, default=unique_vals)
                            df_to_show = df_to_show[df_to_show[filter_col].isin(selected_vals)]
                
                # Display Data
                st.markdown(f"**Showing {len(df_to_show)} rows**")
                st.dataframe(df_to_show[show_cols], height=400, use_container_width=True)
                
                # Export Button
                csv = df_to_show[show_cols].to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Filtered Data (CSV)",
                    data=csv,
                    file_name='filtered_data.csv',
                    mime='text/csv',
                )
        else:
            # Welcome screen
            st.markdown("""
                <div style="background:#ffffff;border:1px solid #e2e6ea;border-radius:12px;padding:3rem 2.5rem;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,0.06);margin-top:1rem;">
                    <div style="font-size:3.5rem;margin-bottom:1rem;">📂</div>
                    <h2 style="color:#111111;font-size:1.6rem;font-weight:700;margin-bottom:0.5rem;">No dataset loaded yet</h2>
                    <p style="color:#6b7280;font-size:1rem;max-width:500px;margin:0 auto 2rem;">Upload a CSV or Excel file using the sidebar to begin your analysis.</p>
                    <div style="display:flex;justify-content:center;gap:2rem;flex-wrap:wrap;margin-top:1.5rem;">
                        <div style="text-align:left;background:#f5f6fa;border-radius:8px;padding:1rem 1.5rem;min-width:180px;">
                            <div style="font-size:1.4rem;">🧹</div>
                            <div style="font-weight:600;color:#111111;margin-top:0.4rem;">Auto Cleaning</div>
                            <div style="color:#6b7280;font-size:0.82rem;margin-top:0.2rem;">Duplicates &amp; missing values handled automatically</div>
                        </div>
                        <div style="text-align:left;background:#f5f6fa;border-radius:8px;padding:1rem 1.5rem;min-width:180px;">
                            <div style="font-size:1.4rem;">📈</div>
                            <div style="font-weight:600;color:#111111;margin-top:0.4rem;">Statistical Tests</div>
                            <div style="color:#6b7280;font-size:0.82rem;margin-top:0.2rem;">Normality, T-tests, and correlation analysis</div>
                        </div>
                        <div style="text-align:left;background:#f5f6fa;border-radius:8px;padding:1rem 1.5rem;min-width:180px;">
                            <div style="font-size:1.4rem;">🎨</div>
                            <div style="font-weight:600;color:#111111;margin-top:0.4rem;">Interactive Charts</div>
                            <div style="color:#6b7280;font-size:0.82rem;margin-top:0.2rem;">Histograms, scatter plots, heatmaps &amp; more</div>
                        </div>
                        <div style="text-align:left;background:#f5f6fa;border-radius:8px;padding:1rem 1.5rem;min-width:180px;">
                            <div style="font-size:1.4rem;">🤝</div>
                            <div style="font-weight:600;color:#111111;margin-top:0.4rem;">Decision Support</div>
                            <div style="color:#6b7280;font-size:0.82rem;margin-top:0.2rem;">Outlier detection, filters, regression &amp; grouping</div>
                        </div>
                    </div>
                    <p style="color:#9ca3af;font-size:0.8rem;margin-top:2rem;">Supported formats: CSV · XLSX · XLS</p>
                </div>
            """, unsafe_allow_html=True)
