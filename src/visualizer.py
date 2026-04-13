import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Dict, Any


class Visualizer:
    """
    Creates professional, enterprise-grade Plotly visualizations.
    """

    # ── Palette ──────────────────────────────────────────────────
    BLUE     = '#2563eb'
    GREEN    = '#16a34a'
    RED      = '#dc2626'
    AMBER    = '#d97706'
    VIOLET   = '#7c3aed'
    TEAL     = '#0891b2'
    PINK     = '#db2777'
    LIME     = '#65a30d'
    ORANGE   = '#ea580c'
    CYAN     = '#0284c7'

    PALETTE  = ['#2563eb', '#16a34a', '#dc2626', '#d97706', '#7c3aed',
                '#0891b2', '#db2777', '#65a30d', '#ea580c', '#0284c7']

    BG       = '#ffffff'
    PAPER    = '#ffffff'
    GRID     = '#f1f5f9'
    FONT     = '#1e293b'
    MUTED    = '#64748b'

    def __init__(self):
        self.template = 'plotly_white'

    # ── Theme ─────────────────────────────────────────────────────

    def _base(self, fig: go.Figure, height: int = 420) -> go.Figure:
        fig.update_layout(
            template=self.template,
            paper_bgcolor=self.PAPER,
            plot_bgcolor=self.BG,
            height=height,
            font=dict(family='Inter, system-ui, sans-serif', color=self.FONT, size=12),
            title_font=dict(size=14, color='#0f172a', family='Inter, system-ui, sans-serif'),
            margin=dict(l=55, r=25, t=55, b=50),
            hoverlabel=dict(
                bgcolor='#ffffff',
                bordercolor='#e2e8f0',
                font_size=12,
                font_family='Inter, system-ui, sans-serif',
                font_color='#0f172a',
                namelength=-1,
            ),
            xaxis=dict(
                gridcolor=self.GRID, linecolor='#e2e8f0',
                tickfont=dict(color=self.MUTED, size=11),
                title_font=dict(color='#475569', size=12),
                showgrid=True, zeroline=False,
            ),
            yaxis=dict(
                gridcolor=self.GRID, linecolor='#e2e8f0',
                tickfont=dict(color=self.MUTED, size=11),
                title_font=dict(color='#475569', size=12),
                showgrid=True, zeroline=False,
            ),
            legend=dict(
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#e2e8f0', borderwidth=1,
                font=dict(color='#475569', size=11),
            ),
        )
        return fig

    # ── Heatmap ───────────────────────────────────────────────────

    def create_heatmap(self, corr_matrix: pd.DataFrame) -> go.Figure:
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu_r',
            zmid=0, zmin=-1, zmax=1,
            text=np.round(corr_matrix.values, 2),
            texttemplate='%{text}',
            textfont=dict(size=10, color='#0f172a'),
            colorbar=dict(
                title='r', tickfont=dict(color=self.MUTED, size=10),
                thickness=12, len=0.8,
            ),
            hovertemplate='%{y} — %{x}<br>r = %{z:.3f}<extra></extra>',
        ))
        fig.update_layout(
            title='Correlation Matrix',
            xaxis=dict(tickangle=-35, tickfont=dict(size=10)),
            yaxis=dict(tickfont=dict(size=10)),
        )
        return self._base(fig, height=520)

    # ── Histogram ─────────────────────────────────────────────────

    def create_histogram(self, data: pd.DataFrame, column: str) -> go.Figure:
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=data[column], name='Distribution',
            marker=dict(color=self.BLUE, line=dict(color='#ffffff', width=0.6)),
            opacity=0.88,
            hovertemplate='Value: %{x}<br>Count: %{y}<extra></extra>',
        ))
        mean_val   = data[column].mean()
        median_val = data[column].median()
        fig.add_vline(x=mean_val,   line_dash='dash', line_color=self.RED,
                      line_width=2,
                      annotation_text=f'Mean: {mean_val:.2f}',
                      annotation_font=dict(color=self.RED, size=11))
        fig.add_vline(x=median_val, line_dash='dot', line_color=self.GREEN,
                      line_width=2,
                      annotation_text=f'Median: {median_val:.2f}',
                      annotation_position='bottom right',
                      annotation_font=dict(color=self.GREEN, size=11))
        fig.update_layout(title=f'Distribution — {column}',
                          xaxis_title=column, yaxis_title='Frequency', showlegend=False)
        return self._base(fig)

    # ── Scatter ───────────────────────────────────────────────────

    def create_scatter(self, data: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data[x_col], y=data[y_col],
            mode='markers', name='Observations',
            marker=dict(size=7, color=self.BLUE, opacity=0.7,
                        line=dict(color='#ffffff', width=0.8)),
            hovertemplate=f'{x_col}: %{{x}}<br>{y_col}: %{{y}}<extra></extra>',
        ))
        try:
            valid = data[[x_col, y_col]].dropna()
            x_v   = pd.to_numeric(valid[x_col], errors='coerce')
            y_v   = pd.to_numeric(valid[y_col], errors='coerce')
            mask  = x_v.notna() & y_v.notna()
            if mask.sum() > 1:
                z  = np.polyfit(x_v[mask], y_v[mask], 1)
                p  = np.poly1d(z)
                xs = np.linspace(x_v[mask].min(), x_v[mask].max(), 200)
                fig.add_trace(go.Scatter(
                    x=xs, y=p(xs), mode='lines', name='Trend',
                    line=dict(color=self.RED, width=2, dash='dash'),
                ))
        except Exception:
            pass
        fig.update_layout(title=f'{y_col} vs {x_col}',
                          xaxis_title=x_col, yaxis_title=y_col)
        return self._base(fig)

    # ── Line Chart ────────────────────────────────────────────────

    def create_line_chart(self, data: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data[x_col], y=data[y_col],
            mode='lines+markers', name=y_col,
            line=dict(color=self.BLUE, width=2.5),
            marker=dict(size=5, color=self.BLUE, line=dict(color='#ffffff', width=1)),
        ))
        fig.update_layout(title=f'{y_col} Trend', xaxis_title=x_col, yaxis_title=y_col,
                          hovermode='x unified')
        return self._base(fig)

    # ── Box Plot ──────────────────────────────────────────────────

    def create_box_plot(self, data: pd.DataFrame, columns: List[str]) -> go.Figure:
        fig = go.Figure()
        for idx, col in enumerate(columns):
            fig.add_trace(go.Box(
                y=data[col], name=col,
                marker_color=self.PALETTE[idx % len(self.PALETTE)],
                boxmean='sd',
                marker=dict(size=4, outliercolor=self.RED),
                line=dict(width=1.5),
            ))
        fig.update_layout(title='Distribution Comparison — Box Plot',
                          yaxis_title='Value', showlegend=False)
        return self._base(fig)

    # ── Bar Chart ─────────────────────────────────────────────────

    def create_bar_chart(self, data: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
        agg = data.groupby(x_col)[y_col].mean().reset_index()
        fig = go.Figure(go.Bar(
            x=agg[x_col], y=agg[y_col],
            marker=dict(color=agg[y_col], colorscale='Blues',
                        line=dict(color='#ffffff', width=0.6)),
            text=np.round(agg[y_col], 2), textposition='outside',
            textfont=dict(color='#475569', size=11),
        ))
        fig.update_layout(title=f'Average {y_col} by {x_col}',
                          xaxis_title=x_col, yaxis_title=f'Average {y_col}')
        return self._base(fig)

    # ── Horizontal Bar ────────────────────────────────────────────

    def create_horizontal_bar_chart(self, data: pd.DataFrame, x_col: str,
                                    y_col: str, title: str = '') -> go.Figure:
        fig = go.Figure(go.Bar(
            x=data[x_col], y=data[y_col], orientation='h',
            marker=dict(color=data[x_col], colorscale='Blues',
                        line=dict(color='#ffffff', width=0.6)),
            text=np.round(data[x_col], 2), textposition='auto',
            textfont=dict(color='#475569', size=11),
        ))
        fig.update_layout(title=title, xaxis_title=x_col, yaxis_title=y_col,
                          yaxis=dict(categoryorder='total ascending'))
        return self._base(fig)

    # ── Pie / Donut ───────────────────────────────────────────────

    def create_pie_chart(self, labels: List[str], values: List[float],
                         title: str) -> go.Figure:
        fig = go.Figure(go.Pie(
            labels=labels, values=values, hole=0.45,
            marker=dict(colors=self.PALETTE, line=dict(color='#ffffff', width=2)),
            textinfo='label+percent',
            textfont=dict(size=12),
            hovertemplate='%{label}<br>Count: %{value}<br>Share: %{percent}<extra></extra>',
        ))
        fig.update_layout(title=title, showlegend=True,
                          legend=dict(orientation='h', y=-0.1))
        return self._base(fig, height=380)

    # ── Time Series ───────────────────────────────────────────────

    def create_time_series_chart(self, data: pd.DataFrame, date_col: str,
                                  value_col: str) -> go.Figure:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data[date_col], y=data[value_col],
            mode='lines', name=value_col,
            line=dict(color=self.BLUE, width=2.5),
            fill='tozeroy', fillcolor='rgba(37,99,235,0.07)',
        ))
        fig.update_layout(
            title=f'{value_col} Over Time', xaxis_title='Date', yaxis_title=value_col,
            xaxis=dict(
                rangeselector=dict(buttons=[
                    dict(count=1, label='1M', step='month', stepmode='backward'),
                    dict(count=3, label='3M', step='month', stepmode='backward'),
                    dict(count=6, label='6M', step='month', stepmode='backward'),
                    dict(count=1, label='1Y', step='year', stepmode='backward'),
                    dict(step='all', label='All'),
                ]),
                rangeslider=dict(visible=True, thickness=0.05),
                type='date',
            ),
        )
        return self._base(fig, height=480)

    # ── Regression ───────────────────────────────────────────────

    def create_regression_chart(self, data: pd.DataFrame, x_col: str, y_col: str,
                                  slope: float, intercept: float) -> go.Figure:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data[x_col], y=data[y_col], mode='markers', name='Observations',
            marker=dict(color=self.BLUE, opacity=0.65, size=7,
                        line=dict(color='#ffffff', width=0.8)),
        ))
        xs = np.linspace(data[x_col].min(), data[x_col].max(), 200)
        ys = slope * xs + intercept
        fig.add_trace(go.Scatter(
            x=xs, y=ys, mode='lines', name='Regression Line',
            line=dict(color=self.RED, width=2.5),
        ))
        fig.update_layout(title=f'Linear Regression — {y_col} vs {x_col}',
                          xaxis_title=x_col, yaxis_title=y_col)
        return self._base(fig)

    # ── Forecast Chart (new) ──────────────────────────────────────

    def create_forecast_chart(self, forecast_data: Dict[str, Any],
                               column: str) -> go.Figure:
        """Render historical + forecast with confidence interval band."""
        fig = go.Figure()

        hx = forecast_data['historical_x']
        hy = forecast_data['historical_y']
        fy = forecast_data['fitted_y']
        fx = forecast_data['future_x']
        fc = forecast_data['forecast']
        cu = forecast_data['ci_upper']
        cl = forecast_data['ci_lower']

        # CI band
        fig.add_trace(go.Scatter(
            x=list(fx) + list(reversed(fx)),
            y=list(cu) + list(reversed(cl)),
            fill='toself', fillcolor='rgba(37,99,235,0.1)',
            line=dict(width=0), name='95% Confidence',
            showlegend=True,
            hoverinfo='skip',
        ))
        # Historical
        fig.add_trace(go.Scatter(
            x=hx, y=hy, mode='lines', name='Historical',
            line=dict(color=self.BLUE, width=2.5),
        ))
        # Fitted
        fig.add_trace(go.Scatter(
            x=hx, y=fy, mode='lines', name='Trend Fit',
            line=dict(color=self.MUTED, width=1.5, dash='dot'),
        ))
        # Forecast
        fig.add_trace(go.Scatter(
            x=fx, y=fc, mode='lines+markers', name='Forecast',
            line=dict(color=self.RED, width=2.5, dash='dash'),
            marker=dict(size=6, color=self.RED),
        ))
        direction = forecast_data.get('direction', '')
        fig.update_layout(
            title=f'Linear Trend Forecast — {column} ({direction})',
            xaxis_title='Record Index', yaxis_title=column,
            hovermode='x unified',
        )
        return self._base(fig, height=440)

    def create_time_forecast_chart(self, forecast_data: Dict[str, Any],
                                    value_col: str) -> go.Figure:
        """Time-indexed forecast chart."""
        fig = go.Figure()
        hd = forecast_data['historical_dates']
        hy = forecast_data['historical_y']
        fd = forecast_data['future_dates']
        fc = forecast_data['forecast']
        cu = forecast_data['ci_upper']
        cl = forecast_data['ci_lower']
        fy = forecast_data['fitted_y']

        fig.add_trace(go.Scatter(
            x=list(fd) + list(reversed(fd)),
            y=list(cu) + list(reversed(cl)),
            fill='toself', fillcolor='rgba(220,38,38,0.08)',
            line=dict(width=0), name='95% CI', hoverinfo='skip',
        ))
        fig.add_trace(go.Scatter(
            x=hd, y=hy, mode='lines', name='Historical',
            line=dict(color=self.BLUE, width=2.5),
        ))
        fig.add_trace(go.Scatter(
            x=hd, y=fy, mode='lines', name='Trend',
            line=dict(color=self.MUTED, width=1.5, dash='dot'),
        ))
        fig.add_trace(go.Scatter(
            x=fd, y=fc, mode='lines+markers', name='Forecast',
            line=dict(color=self.RED, width=2.5, dash='dash'),
            marker=dict(size=6, color=self.RED),
        ))
        fig.update_layout(
            title=f'Time Series Forecast — {value_col}',
            xaxis_title='Date', yaxis_title=value_col,
            hovermode='x unified',
        )
        return self._base(fig, height=440)

    # ── Pareto Chart (new) ────────────────────────────────────────

    def create_pareto_chart(self, data: pd.DataFrame,
                             cat_col: str, val_col: str,
                             cum_col: str = 'Cumulative (%)') -> go.Figure:
        """80/20 Pareto — bar + cumulative line."""
        fig = make_subplots(specs=[[{'secondary_y': True}]])

        fig.add_trace(go.Bar(
            x=data[cat_col], y=data[val_col],
            name='Total Value',
            marker=dict(color=self.PALETTE[:len(data)],
                        line=dict(color='#ffffff', width=0.6)),
            text=data['Share (%)'].map('{:.1f}%'.format),
            textposition='outside',
            textfont=dict(size=10, color='#475569'),
        ), secondary_y=False)

        fig.add_trace(go.Scatter(
            x=data[cat_col], y=data[cum_col],
            mode='lines+markers', name='Cumulative %',
            line=dict(color=self.RED, width=2.5),
            marker=dict(size=6, color=self.RED),
        ), secondary_y=True)

        fig.add_hline(y=80, line_dash='dash', line_color=self.AMBER, line_width=1.5,
                      annotation_text='80%', annotation_font=dict(color=self.AMBER))

        fig.update_layout(
            title=f'Pareto Analysis — {val_col} by {cat_col}',
            paper_bgcolor=self.PAPER, plot_bgcolor=self.BG,
            font=dict(family='Inter, system-ui, sans-serif', color=self.FONT),
            height=440,
            margin=dict(l=55, r=55, t=55, b=60),
            legend=dict(font=dict(size=11, color='#475569'),
                        bgcolor='rgba(255,255,255,0.9)', bordercolor='#e2e8f0'),
            xaxis=dict(tickangle=-30, gridcolor=self.GRID, linecolor='#e2e8f0',
                       tickfont=dict(size=10)),
        )
        fig.update_yaxes(title_text='Total Value',    secondary_y=False,
                         gridcolor=self.GRID, tickfont=dict(color=self.MUTED))
        fig.update_yaxes(title_text='Cumulative (%)', secondary_y=True,
                         range=[0, 110], gridcolor='rgba(0,0,0,0)',
                         tickfont=dict(color=self.RED), ticksuffix='%')
        return fig

    # ── Anomaly Scatter (new) ─────────────────────────────────────

    def create_anomaly_chart(self, data: pd.DataFrame, column: str,
                              threshold: float = 3.0) -> go.Figure:
        """Z-score anomaly chart — normal points vs flagged anomalies."""
        from scipy import stats as sc_stats
        col_data = data[column].dropna()
        z_scores = np.abs(sc_stats.zscore(col_data))
        idx      = col_data.index

        normal_mask = z_scores <= threshold
        anom_mask   = z_scores > threshold

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=idx[normal_mask], y=col_data[normal_mask],
            mode='markers', name='Normal',
            marker=dict(size=6, color=self.BLUE, opacity=0.65,
                        line=dict(color='#ffffff', width=0.5)),
        ))
        if anom_mask.any():
            fig.add_trace(go.Scatter(
                x=idx[anom_mask], y=col_data[anom_mask],
                mode='markers', name=f'Anomaly (|z| > {threshold})',
                marker=dict(size=10, color=self.RED, symbol='x',
                            line=dict(color=self.RED, width=1.5)),
            ))
        # Mean ± threshold*std lines
        mean_v = col_data.mean()
        std_v  = col_data.std()
        for mult, label, color in [
            (threshold, f'+{threshold}σ', self.AMBER),
            (-threshold, f'-{threshold}σ', self.AMBER),
        ]:
            fig.add_hline(y=mean_v + mult * std_v,
                          line_dash='dash', line_color=color, line_width=1.5,
                          annotation_text=label,
                          annotation_font=dict(color=color, size=10))
        fig.add_hline(y=mean_v, line_dash='dot', line_color=self.GREEN,
                      line_width=1, annotation_text='Mean',
                      annotation_font=dict(color=self.GREEN, size=10))
        fig.update_layout(title=f'Anomaly Detection — {column}',
                          xaxis_title='Record Index', yaxis_title=column)
        return self._base(fig)

    # ── Variance / CV Chart (new) ─────────────────────────────────

    def create_cv_chart(self, var_df: pd.DataFrame) -> go.Figure:
        """Horizontal bar chart of Coefficient of Variation per column."""
        df = var_df[var_df['CV (%)'] != 'N/A'].copy()
        df['CV (%)'] = pd.to_numeric(df['CV (%)'], errors='coerce').dropna()
        df = df.sort_values('CV (%)', ascending=True)

        colors = [self.RED if v > 50 else (self.AMBER if v > 20 else self.GREEN)
                  for v in df['CV (%)']]
        fig = go.Figure(go.Bar(
            x=df['CV (%)'], y=df['Column'], orientation='h',
            marker=dict(color=colors, line=dict(color='#ffffff', width=0.5)),
            text=df['CV (%)'].map('{:.1f}%'.format), textposition='outside',
            textfont=dict(size=11, color='#475569'),
        ))
        fig.add_vline(x=50, line_dash='dash', line_color=self.RED,
                      annotation_text='High (50%)',
                      annotation_font=dict(color=self.RED, size=10))
        fig.add_vline(x=20, line_dash='dot', line_color=self.AMBER,
                      annotation_text='Moderate (20%)',
                      annotation_font=dict(color=self.AMBER, size=10))
        fig.update_layout(title='Coefficient of Variation by Column',
                          xaxis_title='CV (%)', yaxis_title='')
        return self._base(fig, height=max(300, len(df) * 35 + 80))

    # ── Health Gauge (new) ────────────────────────────────────────

    def create_health_gauge(self, score: float, rating: str) -> go.Figure:
        color = ('#16a34a' if score >= 90 else '#2563eb' if score >= 70
                 else '#d97706' if score >= 50 else '#dc2626')
        fig = go.Figure(go.Indicator(
            mode='gauge+number+delta',
            value=score,
            delta={'reference': 70, 'valueformat': '.1f',
                   'increasing': {'color': self.GREEN},
                   'decreasing': {'color': self.RED}},
            number={'suffix': '/100', 'font': {'size': 28, 'color': '#0f172a'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1,
                         'tickcolor': self.MUTED, 'tickfont': {'size': 10}},
                'bar': {'color': color, 'thickness': 0.25},
                'bgcolor': '#f1f5f9',
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 50],  'color': '#fee2e2'},
                    {'range': [50, 70], 'color': '#fef3c7'},
                    {'range': [70, 90], 'color': '#dbeafe'},
                    {'range': [90, 100],'color': '#dcfce7'},
                ],
                'threshold': {
                    'line': {'color': '#0f172a', 'width': 3},
                    'thickness': 0.75, 'value': score,
                },
            },
            title={'text': f'Data Quality — {rating}',
                   'font': {'size': 13, 'color': '#475569'}},
        ))
        fig.update_layout(paper_bgcolor=self.PAPER, height=220,
                          margin=dict(l=20, r=20, t=40, b=20),
                          font=dict(family='Inter, system-ui, sans-serif'))
        return fig
