import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import List

class Visualizer:
    """
    Creates interactive Plotly visualizations.
    
    This class contains methods to generate various chart types
    with consistent styling and modern aesthetics.
    """
    
    # Color scheme — vibrant professional palette on white background
    PRIMARY_COLOR = '#2563eb'    # Royal blue
    SECONDARY_COLOR = '#16a34a'  # Emerald green
    ACCENT_COLOR = '#dc2626'     # Crimson red
    TERTIARY_COLOR = '#d97706'   # Amber
    PURPLE_COLOR = '#7c3aed'     # Violet
    TEAL_COLOR = '#0891b2'       # Teal
    BACKGROUND_COLOR = '#ffffff'
    PAPER_COLOR = '#ffffff'
    GRID_COLOR = '#e5e7eb'
    FONT_COLOR = '#111111'

    CHART_COLORS = ['#2563eb', '#16a34a', '#dc2626', '#d97706', '#7c3aed',
                    '#0891b2', '#db2777', '#65a30d', '#ea580c', '#0f766e']

    def __init__(self):
        """Initialize the Visualizer with default settings."""
        self.template = 'plotly_white'
        
    def _apply_theme(self, fig: go.Figure) -> go.Figure:
        """
        Apply consistent light theme to all figures.
        
        Args:
            fig: Plotly figure object
            
        Returns:
            go.Figure: Themed figure
        """
        fig.update_layout(
            template=self.template,
            paper_bgcolor=self.PAPER_COLOR,
            plot_bgcolor=self.BACKGROUND_COLOR,
            font=dict(family='Inter, sans-serif', color=self.FONT_COLOR, size=12),
            title_font=dict(family='Inter, sans-serif', color='#111111', size=15),
            margin=dict(l=50, r=40, t=70, b=50),
            hoverlabel=dict(
                bgcolor='#ffffff',
                bordercolor='#e2e6ea',
                font_size=12,
                font_family='Inter, sans-serif',
                font_color='#111111'
            ),
            xaxis=dict(
                gridcolor=self.GRID_COLOR,
                linecolor='#d1d5db',
                tickfont=dict(color='#374151'),
                title_font=dict(color='#374151')
            ),
            yaxis=dict(
                gridcolor=self.GRID_COLOR,
                linecolor='#d1d5db',
                tickfont=dict(color='#374151'),
                title_font=dict(color='#374151')
            ),
            legend=dict(
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#e2e6ea',
                borderwidth=1,
                font=dict(color='#374151')
            )
        )
        return fig
    
    def create_heatmap(self, corr_matrix: pd.DataFrame) -> go.Figure:
        """
        Create an interactive correlation heatmap.
        
        Args:
            corr_matrix: Correlation matrix dataframe
            
        Returns:
            go.Figure: Plotly heatmap figure
        """
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu_r',
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title='Correlation')
        ))
        
        fig.update_layout(
            title='Correlation Heatmap',
            xaxis_title='Features',
            yaxis_title='Features',
            height=600
        )
        
        return self._apply_theme(fig)
    
    def create_histogram(self, data: pd.DataFrame, column: str) -> go.Figure:
        """
        Create a histogram with statistical overlays.
        
        Args:
            data: Source dataframe
            column: Column name to visualize
            
        Returns:
            go.Figure: Plotly histogram figure
        """
        fig = go.Figure()
        
        # Add histogram
        fig.add_trace(go.Histogram(
            x=data[column],
            name='Distribution',
            marker=dict(
                color=self.PRIMARY_COLOR,
                line=dict(color='#ffffff', width=0.8)
            ),
            opacity=0.85
        ))
        
        # Add mean line
        mean_val = data[column].mean()
        fig.add_vline(
            x=mean_val,
            line_dash="dash",
            line_color=self.ACCENT_COLOR,
            line_width=2,
            annotation_text=f"Mean: {mean_val:.2f}",
            annotation_position="top"
        )
        
        # Add median line
        median_val = data[column].median()
        fig.add_vline(
            x=median_val,
            line_dash="dot",
            line_color=self.SECONDARY_COLOR,
            line_width=2,
            annotation_text=f"Median: {median_val:.2f}",
            annotation_position="bottom"
        )
        
        fig.update_layout(
            title=f'Distribution of {column}',
            xaxis_title=column,
            yaxis_title='Frequency',
            height=500,
            showlegend=True
        )
        
        return self._apply_theme(fig)
    
    def create_scatter(self, data: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
        """
        Create a scatter plot with trend line.
        
        Args:
            data: Source dataframe
            x_col: X-axis column name
            y_col: Y-axis column name
            
        Returns:
            go.Figure: Plotly scatter figure
        """
        # Create basic scatter plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data[x_col],
            y=data[y_col],
            mode='markers',
            name='Data Points',
            marker=dict(
                size=8,
                color=self.PRIMARY_COLOR,
                opacity=0.75,
                line=dict(width=1, color='#ffffff')
            )
        ))
        
        # Add manual trend line using numpy
        try:
            # Get common valid indices
            valid_idx = data[x_col].notna() & data[y_col].notna()
            x_vals = pd.to_numeric(data.loc[valid_idx, x_col], errors='coerce')
            y_vals = pd.to_numeric(data.loc[valid_idx, y_col], errors='coerce')
            
            # Calculate trend line using numpy polyfit
            if len(x_vals) > 1 and len(y_vals) > 1:
                z = np.polyfit(x_vals, y_vals, 1)
                p = np.poly1d(z)
                
                x_trend = np.linspace(x_vals.min(), x_vals.max(), 100)
                y_trend = p(x_trend)
                
                fig.add_trace(go.Scatter(
                    x=x_trend,
                    y=y_trend,
                    mode='lines',
                    name='Trend Line',
                    line=dict(color=self.ACCENT_COLOR, width=2.5, dash='dash')
                ))
        except Exception:
            pass  # Skip trend line if there's an error
        
        fig.update_layout(
            title=f'{y_col} vs {x_col}',
            xaxis_title=x_col,
            yaxis_title=y_col,
            height=500
        )
        
        return self._apply_theme(fig)
    
    def create_line_chart(self, data: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
        """
        Create a line chart for time-series or sequential data.
        
        Args:
            data: Source dataframe
            x_col: X-axis column name
            y_col: Y-axis column name
            
        Returns:
            go.Figure: Plotly line figure
        """
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data[x_col],
            y=data[y_col],
            mode='lines+markers',
            name=y_col,
            line=dict(color=self.PRIMARY_COLOR, width=2.5),
            marker=dict(size=6, color=self.PRIMARY_COLOR, line=dict(color='#ffffff', width=1))
        ))
        
        fig.update_layout(
            title=f'{y_col} Trend',
            xaxis_title=x_col,
            yaxis_title=y_col,
            height=500,
            hovermode='x unified'
        )
        
        return self._apply_theme(fig)
    
    def create_box_plot(self, data: pd.DataFrame, columns: List[str]) -> go.Figure:
        """
        Create box plots for outlier detection.
        
        Args:
            data: Source dataframe
            columns: List of column names to visualize
            
        Returns:
            go.Figure: Plotly box plot figure
        """
        fig = go.Figure()
        
        for idx, column in enumerate(columns):
            fig.add_trace(go.Box(
                y=data[column],
                name=column,
                marker_color=self.CHART_COLORS[idx % len(self.CHART_COLORS)],
                boxmean='sd',
                marker=dict(outliercolor=self.ACCENT_COLOR, size=5),
                line=dict(width=1.5)
            ))
        
        fig.update_layout(
            title='Box Plot - Outlier Detection',
            yaxis_title='Values',
            height=500,
            showlegend=True
        )
        
        return self._apply_theme(fig)
    
    def create_bar_chart(self, data: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
        """
        Create a bar chart for categorical comparisons.
        
        Args:
            data: Source dataframe
            x_col: X-axis column name (categorical)
            y_col: Y-axis column name (numeric)
            
        Returns:
            go.Figure: Plotly bar figure
        """
        # Aggregate data if needed
        aggregated = data.groupby(x_col)[y_col].mean().reset_index()
        
        fig = go.Figure(data=[
            go.Bar(
                x=aggregated[x_col],
                y=aggregated[y_col],
                marker=dict(
                    color=aggregated[y_col],
                    colorscale='Blues',
                    line=dict(color='#ffffff', width=0.8)
                ),
                text=np.round(aggregated[y_col], 2),
                textposition='outside',
                textfont=dict(color='#374151', size=11)
            )
        ])
        
        fig.update_layout(
            title=f'{y_col} by {x_col}',
            xaxis_title=x_col,
            yaxis_title=f'Average {y_col}',
            height=500
        )
        
        return self._apply_theme(fig)

    def create_horizontal_bar_chart(self, data: pd.DataFrame, x_col: str, y_col: str, title: str = "") -> go.Figure:
        """
        Create a horizontal bar chart for aggregated data.
        
        Args:
            data: Source dataframe
            x_col: X-axis column name (numeric values)
            y_col: Y-axis column name (categorical labels)
            title: Chart title
            
        Returns:
            go.Figure: Plotly horizontal bar figure
        """
        fig = go.Figure(data=[
            go.Bar(
                x=data[x_col],
                y=data[y_col],
                orientation='h',
                marker=dict(
                    color=data[x_col],
                    colorscale='Teal',
                    line=dict(color='#ffffff', width=0.8)
                ),
                text=np.round(data[x_col], 2),
                textposition='auto',
                textfont=dict(color='#374151', size=11)
            )
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
            height=500,
            yaxis={'categoryorder': 'total ascending'}  # Sort bars
        )
        
        return self._apply_theme(fig)

    def create_pie_chart(self, labels: List[str], values: List[float], title: str) -> go.Figure:
        """
        Create a pie chart.
        
        Args:
            labels: Label names
            values: Numerical values
            title: Chart title
            
        Returns:
            go.Figure: Plotly pie chart
        """
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.4,
            marker=dict(
                colors=self.CHART_COLORS,
                line=dict(color='#ffffff', width=2)
            ),
            textinfo='label+percent',
            textfont=dict(size=12, color='#111111')
        )])
        
        fig.update_layout(
            title=title,
            height=400,
            showlegend=True
        )
        
        return self._apply_theme(fig)

    def create_time_series_chart(self, data: pd.DataFrame, date_col: str, value_col: str) -> go.Figure:
        """
        Create an interactive time series chart.
        
        Args:
            data: Time series dataframe
            date_col: Date column name
            value_col: Value column name
            
        Returns:
            go.Figure: Plotly line chart with range slider
        """
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data[date_col],
            y=data[value_col],
            mode='lines',
            name=value_col,
            line=dict(color=self.PRIMARY_COLOR, width=2.5),
            fill='tozeroy',
            fillcolor='rgba(37, 99, 235, 0.08)'
        ))
        
        fig.update_layout(
            title=f'{value_col} Over Time',
            xaxis_title='Date',
            yaxis_title=value_col,
            height=450,
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        )
        
        return self._apply_theme(fig)
    
    def create_regression_chart(self, data: pd.DataFrame, x_col: str, y_col: str, slope: float, intercept: float) -> go.Figure:
        """
        Create scatter plot with regression line.
        
        Args:
            data: Source dataframe
            x_col: Independent variable
            y_col: Dependent variable
            slope: Regression slope
            intercept: Regression intercept
            
        Returns:
            go.Figure: Plotly figure
        """
        fig = go.Figure()
        
        # Scatter points
        fig.add_trace(go.Scatter(
            x=data[x_col],
            y=data[y_col],
            mode='markers',
            name='Data',
            marker=dict(
                color=self.PRIMARY_COLOR,
                opacity=0.65,
                size=8,
                line=dict(color='#ffffff', width=1)
            )
        ))
        
        # Regression line
        x_range = np.linspace(data[x_col].min(), data[x_col].max(), 100)
        y_range = slope * x_range + intercept
        
        fig.add_trace(go.Scatter(
            x=x_range,
            y=y_range,
            mode='lines',
            name='Regression Line',
            line=dict(color=self.ACCENT_COLOR, width=2.5)
        ))
        
        fig.update_layout(
            title=f'Regression Analysis: {y_col} vs {x_col}',
            xaxis_title=x_col,
            yaxis_title=y_col,
            height=500
        )
        
        return self._apply_theme(fig)
