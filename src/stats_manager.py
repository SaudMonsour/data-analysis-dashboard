import pandas as pd
import numpy as np
from scipy import stats
from typing import Optional, Dict, Any, List


class StatsManager:
    """
    Handles statistical calculations, hypothesis testing, and advanced analytics.
    """

    def __init__(self, data: pd.DataFrame):
        self.data = data

    # ──────────────────────────────────────────────────────────────
    # BASIC & ADVANCED STATS
    # ──────────────────────────────────────────────────────────────

    def get_basic_stats(self) -> Dict[str, Any]:
        if self.data is None:
            return {}
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        return {
            'mean':   self.data[numeric_cols].mean().to_dict(),
            'median': self.data[numeric_cols].median().to_dict(),
            'std':    self.data[numeric_cols].std().to_dict(),
            'min':    self.data[numeric_cols].min().to_dict(),
            'max':    self.data[numeric_cols].max().to_dict(),
        }

    def get_advanced_stats(self) -> Dict[str, Any]:
        if self.data is None:
            return {}
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if numeric_cols.empty:
            return {}
        d = {
            'skewness': self.data[numeric_cols].skew().to_dict(),
            'kurtosis': self.data[numeric_cols].kurtosis().to_dict(),
            '25%':      self.data[numeric_cols].quantile(0.25).to_dict(),
            '75%':      self.data[numeric_cols].quantile(0.75).to_dict(),
        }
        d['iqr'] = {c: d['75%'][c] - d['25%'][c] for c in numeric_cols}
        return d

    # ──────────────────────────────────────────────────────────────
    # OUTLIERS (IQR)
    # ──────────────────────────────────────────────────────────────

    def get_outliers(self) -> Dict[str, pd.DataFrame]:
        if self.data is None:
            return {}
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        outliers = {}
        for col in numeric_cols:
            Q1 = self.data[col].quantile(0.25)
            Q3 = self.data[col].quantile(0.75)
            IQR = Q3 - Q1
            lb = Q1 - 1.5 * IQR
            ub = Q3 + 1.5 * IQR
            mask = (self.data[col] < lb) | (self.data[col] > ub)
            if mask.any():
                df = self.data[mask].copy()
                df['Outlier_Reason'] = np.where(
                    df[col] < lb,
                    f'Low (< {lb:.2f})',
                    f'High (> {ub:.2f})'
                )
                outliers[col] = df
        return outliers

    def _count_outlier_cells(self) -> int:
        return sum(df.shape[0] for df in self.get_outliers().values())

    # ──────────────────────────────────────────────────────────────
    # Z-SCORE ANOMALY DETECTION (new)
    # ──────────────────────────────────────────────────────────────

    def get_zscore_anomalies(self, threshold: float = 3.0) -> Dict[str, pd.DataFrame]:
        """
        Detect anomalies using Z-score method.
        Returns rows where |z| > threshold for each numeric column.
        """
        if self.data is None:
            return {}
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        anomalies = {}
        for col in numeric_cols:
            col_data = self.data[col].dropna()
            if len(col_data) < 3:
                continue
            z_scores = np.abs(stats.zscore(col_data))
            mask = z_scores > threshold
            if mask.any():
                df = self.data.loc[col_data.index[mask]].copy()
                df['Z_Score'] = np.round(z_scores[mask], 3)
                anomalies[col] = df.sort_values('Z_Score', ascending=False)
        return anomalies

    def get_anomaly_summary(self, threshold: float = 3.0) -> pd.DataFrame:
        """
        Summary table: column, count, max z-score, min/max value of anomalies.
        """
        anomalies = self.get_zscore_anomalies(threshold)
        rows = []
        for col, df in anomalies.items():
            rows.append({
                'Column':      col,
                'Anomalies':   len(df),
                'Max Z-Score': round(df['Z_Score'].max(), 2),
                'Min Value':   round(df[col].min(), 4),
                'Max Value':   round(df[col].max(), 4),
                'Risk':        'High' if df['Z_Score'].max() > 5 else 'Medium',
            })
        return pd.DataFrame(rows).sort_values('Anomalies', ascending=False) if rows else pd.DataFrame()

    # ──────────────────────────────────────────────────────────────
    # CORRELATIONS
    # ──────────────────────────────────────────────────────────────

    def get_correlations(self) -> Optional[pd.DataFrame]:
        if self.data is None:
            return None
        numeric_data = self.data.select_dtypes(include=[np.number])
        return numeric_data.corr() if not numeric_data.empty else None

    def get_top_correlations(self, n: int = 8) -> pd.DataFrame:
        corr_matrix = self.get_correlations()
        if corr_matrix is None:
            return pd.DataFrame()
        pairs = corr_matrix.abs().unstack()
        pairs = pairs[pairs < 1.0].sort_values(ascending=False).iloc[::2]
        results = []
        for (col1, col2) in pairs.head(n).index:
            coef = corr_matrix.loc[col1, col2]
            results.append({
                'Variable A': col1,
                'Variable B': col2,
                'Correlation (r)': round(coef, 4),
                'Strength': 'Strong' if abs(coef) > 0.7 else ('Moderate' if abs(coef) > 0.3 else 'Weak'),
                'Direction': 'Positive' if coef > 0 else 'Negative',
            })
        return pd.DataFrame(results)

    # ──────────────────────────────────────────────────────────────
    # GROUPED STATS
    # ──────────────────────────────────────────────────────────────

    def get_grouped_stats(self, group_col: str, value_col: str, agg_func: str) -> pd.DataFrame:
        if self.data is None:
            return pd.DataFrame()
        try:
            grouped = self.data.groupby(group_col)[value_col].agg(agg_func).reset_index()
            grouped.columns = [group_col, f"{agg_func.capitalize()} of {value_col}"]
            return grouped.sort_values(by=grouped.columns[1], ascending=False)
        except Exception:
            return pd.DataFrame()

    # ──────────────────────────────────────────────────────────────
    # PARETO ANALYSIS (new)
    # ──────────────────────────────────────────────────────────────

    def get_pareto_analysis(self, category_col: str, value_col: str) -> pd.DataFrame:
        """
        80/20 Pareto analysis: which categories drive 80% of the total value?
        Returns sorted dataframe with cumulative percentage columns.
        """
        if self.data is None:
            return pd.DataFrame()
        try:
            grouped = self.data.groupby(category_col)[value_col].sum().reset_index()
            grouped.columns = [category_col, 'Total']
            grouped = grouped.sort_values('Total', ascending=False).reset_index(drop=True)
            total = grouped['Total'].sum()
            grouped['Share (%)'] = (grouped['Total'] / total * 100).round(2)
            grouped['Cumulative (%)'] = grouped['Share (%)'].cumsum().round(2)
            grouped['In Top 80%'] = grouped['Cumulative (%)'] <= 80
            return grouped
        except Exception:
            return pd.DataFrame()

    # ──────────────────────────────────────────────────────────────
    # VARIANCE / CV ANALYSIS (new)
    # ──────────────────────────────────────────────────────────────

    def get_variance_analysis(self) -> pd.DataFrame:
        """
        Coefficient of Variation and volatility analysis for all numeric columns.
        CV = (std / mean) * 100.  High CV = high relative variability.
        """
        if self.data is None:
            return pd.DataFrame()
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        rows = []
        for col in numeric_cols:
            col_data = self.data[col].dropna()
            if len(col_data) == 0:
                continue
            mean = col_data.mean()
            std  = col_data.std()
            cv   = (std / abs(mean) * 100) if mean != 0 else np.nan
            skew = col_data.skew()
            kurt = col_data.kurtosis()
            rows.append({
                'Column':           col,
                'Mean':             round(mean, 4),
                'Std Dev':          round(std, 4),
                'CV (%)':           round(cv, 2) if not np.isnan(cv) else 'N/A',
                'Skewness':         round(skew, 4),
                'Kurtosis':         round(kurt, 4),
                'Volatility':       'High' if (not np.isnan(cv) and cv > 50) else ('Moderate' if (not np.isnan(cv) and cv > 20) else 'Low'),
            })
        return pd.DataFrame(rows)

    # ──────────────────────────────────────────────────────────────
    # FORECASTING (new)
    # ──────────────────────────────────────────────────────────────

    def get_linear_forecast(self, column: str, periods: int = 10) -> Dict[str, Any]:
        """
        Simple linear trend forecast for a numeric column (row index as x).
        Returns historical values + projected values with confidence interval.
        """
        if self.data is None or column not in self.data.columns:
            return {}
        try:
            col_data = self.data[column].dropna().reset_index(drop=True)
            x = np.arange(len(col_data))
            slope, intercept = np.polyfit(x, col_data, 1)

            # Residual std for confidence interval
            y_fit = slope * x + intercept
            residuals = col_data.values - y_fit
            resid_std = np.std(residuals)

            # Forecast
            future_x = np.arange(len(col_data), len(col_data) + periods)
            forecast  = slope * future_x + intercept
            ci_upper  = forecast + 1.96 * resid_std
            ci_lower  = forecast - 1.96 * resid_std

            direction = 'Upward' if slope > 0 else 'Downward' if slope < 0 else 'Flat'

            return {
                'historical_x':   list(x),
                'historical_y':   col_data.tolist(),
                'fitted_y':       y_fit.tolist(),
                'future_x':       list(future_x),
                'forecast':       forecast.tolist(),
                'ci_upper':       ci_upper.tolist(),
                'ci_lower':       ci_lower.tolist(),
                'slope':          slope,
                'intercept':      intercept,
                'direction':      direction,
                'change_per_row': slope,
            }
        except Exception:
            return {}

    def get_time_series_forecast(self, date_col: str, value_col: str,
                                  freq: str = 'M', periods: int = 6) -> Dict[str, Any]:
        """
        Time-series aware linear forecast.
        """
        if self.data is None:
            return {}
        try:
            df = self.data[[date_col, value_col]].dropna().copy()
            df[date_col] = pd.to_datetime(df[date_col])
            df = df.set_index(date_col).resample(freq).mean().dropna()

            x = np.arange(len(df))
            y = df[value_col].values
            slope, intercept = np.polyfit(x, y, 1)

            y_fit     = slope * x + intercept
            resid_std = np.std(y - y_fit)

            last_date  = df.index[-1]
            freq_map   = {'D': 'D', 'W': 'W', 'M': 'MS', 'Q': 'QS', 'Y': 'YS'}
            future_idx = pd.date_range(start=last_date, periods=periods + 1,
                                       freq=freq_map.get(freq, 'MS'))[1:]
            future_x   = np.arange(len(df), len(df) + periods)
            forecast   = slope * future_x + intercept
            ci_upper   = forecast + 1.96 * resid_std
            ci_lower   = forecast - 1.96 * resid_std

            return {
                'historical_dates': df.index.tolist(),
                'historical_y':     y.tolist(),
                'fitted_y':         y_fit.tolist(),
                'future_dates':     future_idx.tolist(),
                'forecast':         forecast.tolist(),
                'ci_upper':         ci_upper.tolist(),
                'ci_lower':         ci_lower.tolist(),
                'slope':            slope,
                'direction':        'Upward' if slope > 0 else 'Downward' if slope < 0 else 'Flat',
            }
        except Exception:
            return {}

    # ──────────────────────────────────────────────────────────────
    # COLUMN DETAILS & COMPREHENSIVE SUMMARY
    # ──────────────────────────────────────────────────────────────

    def get_column_details(self) -> pd.DataFrame:
        if self.data is None:
            return pd.DataFrame()
        details = []
        for col in self.data.columns:
            try:
                top_val = self.data[col].mode().iloc[0] if not self.data[col].mode().empty else 'N/A'
                freq    = self.data[col].value_counts().iloc[0] if not self.data[col].value_counts().empty else 0
            except Exception:
                top_val, freq = 'Error', 0
            details.append({
                'Column':        col,
                'Type':          str(self.data[col].dtype),
                'Unique Values': self.data[col].nunique(),
                'Missing Values':self.data[col].isnull().sum(),
                'Missing (%)':   (self.data[col].isnull().sum() / len(self.data)) * 100,
                'Top Value':     str(top_val)[:50],
                'Freq':          freq,
                'Memory (KB)':   self.data[col].memory_usage(deep=True) / 1024,
            })
        return pd.DataFrame(details)

    def get_comprehensive_summary(self) -> pd.DataFrame:
        if self.data is None:
            return pd.DataFrame()
        meta_df = self.get_column_details()
        if meta_df.empty:
            return pd.DataFrame()
        stats_dict = self.get_basic_stats()
        for key in ('Mean', 'Min', 'Max', 'Std Dev'):
            meta_df[key] = '-'
        if stats_dict:
            for col in stats_dict['mean']:
                idx = meta_df[meta_df['Column'] == col].index
                if not idx.empty:
                    i = idx[0]
                    meta_df.at[i, 'Mean']    = f"{stats_dict['mean'][col]:.2f}"
                    meta_df.at[i, 'Min']     = f"{stats_dict['min'][col]:.2f}"
                    meta_df.at[i, 'Max']     = f"{stats_dict['max'][col]:.2f}"
                    meta_df.at[i, 'Std Dev'] = f"{stats_dict['std'][col]:.2f}"
        cols = ['Column', 'Type', 'Missing (%)', 'Unique Values', 'Top Value',
                'Freq', 'Mean', 'Min', 'Max', 'Std Dev', 'Memory (KB)']
        return meta_df[cols]

    # ──────────────────────────────────────────────────────────────
    # TIME SERIES
    # ──────────────────────────────────────────────────────────────

    def get_time_series_data(self, date_col: str, value_col: str, freq: str = 'D') -> pd.DataFrame:
        if self.data is None:
            return pd.DataFrame()
        try:
            df = self.data.copy()
            df[date_col] = pd.to_datetime(df[date_col])
            df = df.set_index(date_col)
            return df[value_col].resample(freq).mean().reset_index()
        except Exception:
            return pd.DataFrame()

    # ──────────────────────────────────────────────────────────────
    # REGRESSION
    # ──────────────────────────────────────────────────────────────

    def calculate_regression(self, x_col: str, y_col: str) -> Dict[str, Any]:
        if self.data is None:
            return {}
        try:
            valid = self.data[[x_col, y_col]].dropna()
            x, y = valid[x_col].values, valid[y_col].values
            if len(x) < 2:
                return {}
            slope, intercept = np.polyfit(x, y, 1)
            y_pred   = slope * x + intercept
            ss_res   = np.sum((y - y_pred) ** 2)
            ss_tot   = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)
            # Pearson p-value
            _, p_value = stats.pearsonr(x, y)
            return {
                'slope':     slope,
                'intercept': intercept,
                'r_squared': r_squared,
                'p_value':   p_value,
                'equation':  f"y = {slope:.4f}x + {intercept:.4f}",
                'significant': p_value < 0.05,
            }
        except Exception:
            return {}

    # ──────────────────────────────────────────────────────────────
    # HYPOTHESIS TESTING
    # ──────────────────────────────────────────────────────────────

    def perform_normality_test(self, column: str) -> Dict[str, Any]:
        if self.data is None or column not in self.data.columns:
            return {}
        try:
            data = self.data[column].dropna()
            if len(data) > 5000:
                data = data.sample(5000)
            stat, p_value = stats.shapiro(data)
            result = {'test': 'Shapiro-Wilk', 'statistic': stat,
                      'p_value': p_value, 'is_normal': p_value > 0.05}
            warning = self.validate_sample_size(column, min_required=30)
            if warning:
                result['warning'] = warning
            return result
        except Exception:
            return {}

    def perform_ttest(self, group_col: str, value_col: str) -> Dict[str, Any]:
        if self.data is None:
            return {}
        try:
            groups = self.data[group_col].dropna().unique()
            if len(groups) != 2:
                return {'error': f'Column must have exactly 2 unique groups (found {len(groups)})'}
            g1 = self.data[self.data[group_col] == groups[0]][value_col].dropna()
            g2 = self.data[self.data[group_col] == groups[1]][value_col].dropna()
            stat, p_value = stats.ttest_ind(g1, g2)
            result = {
                'test': 'Independent T-Test',
                'group1': str(groups[0]), 'group2': str(groups[1]),
                'statistic': stat, 'p_value': p_value,
                'significant': p_value < 0.05,
                'mean_g1': g1.mean(), 'mean_g2': g2.mean(),
            }
            warnings_list = self.validate_ttest_balance(group_col, value_col)
            if warnings_list:
                result['warnings'] = warnings_list
            return result
        except Exception as e:
            return {'error': str(e)}

    # ──────────────────────────────────────────────────────────────
    # HEALTH SCORE
    # ──────────────────────────────────────────────────────────────

    def calculate_health_score(self) -> Optional[Dict[str, Any]]:
        if self.data is None or self.data.empty:
            return None
        total_cells    = self.data.shape[0] * self.data.shape[1]
        missing_ratio  = self.data.isnull().sum().sum() / total_cells
        missing_score  = (1 - missing_ratio) * 100

        total_rows      = len(self.data)
        dup_ratio       = self.data.duplicated().sum() / total_rows
        duplicate_score = (1 - dup_ratio) * 100

        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        total_numeric_cells = len(numeric_cols) * total_rows
        if total_numeric_cells == 0:
            outlier_score = 100.0
        else:
            outlier_ratio = self._count_outlier_cells() / total_numeric_cells
            outlier_score = (1 - min(outlier_ratio, 0.2) / 0.2) * 100

        object_cols = self.data.select_dtypes(include=['object']).columns
        mixed = sum(
            1 for c in object_cols
            if pd.to_numeric(self.data[c], errors='coerce').notna().sum() > len(self.data) * 0.5
        )
        consistency_score = (1 - mixed / max(len(self.data.columns), 1)) * 100

        score = (missing_score * 0.30 + duplicate_score * 0.25 +
                 outlier_score * 0.25 + consistency_score * 0.20)
        rating = ('Excellent' if score >= 90 else 'Good' if score >= 70
                  else 'Fair' if score >= 50 else 'Poor')
        return {
            'score': score, 'rating': rating,
            'components': {
                'missing_score':     missing_score,
                'duplicate_score':   duplicate_score,
                'outlier_score':     outlier_score,
                'consistency_score': consistency_score,
            },
        }

    # ──────────────────────────────────────────────────────────────
    # EXECUTIVE SUMMARY (new)
    # ──────────────────────────────────────────────────────────────

    def generate_executive_summary(self) -> List[Dict[str, str]]:
        """
        Auto-generate a list of key findings for decision makers.
        Each finding has keys: 'title', 'detail', 'type' (info/warning/success/error).
        """
        findings = []
        if self.data is None:
            return findings

        # Health
        health = self.calculate_health_score()
        if health:
            color = ('success' if health['rating'] in ('Excellent', 'Good')
                     else 'warning' if health['rating'] == 'Fair' else 'error')
            findings.append({
                'title':  f"Data Quality: {health['rating']} ({health['score']:.0f}/100)",
                'detail': (f"Missing values account for "
                           f"{(100 - health['components']['missing_score']):.1f}% of cells. "
                           f"Duplicate score: {health['components']['duplicate_score']:.0f}/100."),
                'type': color,
            })

        # Size
        findings.append({
            'title':  f"Dataset: {len(self.data):,} rows x {len(self.data.columns)} columns",
            'detail': (f"Numeric columns: "
                       f"{len(self.data.select_dtypes(include=np.number).columns)}, "
                       f"Categorical: "
                       f"{len(self.data.select_dtypes(exclude=np.number).columns)}."),
            'type': 'info',
        })

        # Strongest correlation
        top_corr = self.get_top_correlations(n=1)
        if not top_corr.empty:
            r = top_corr.iloc[0]
            findings.append({
                'title':  f"Strongest Relationship: {r['Variable A']} vs {r['Variable B']}",
                'detail': (f"Pearson r = {r['Correlation (r)']:.3f} ({r['Strength']} {r['Direction'].lower()}). "
                           f"{'Consider using this as a predictive signal.' if abs(r['Correlation (r)']) > 0.7 else 'Moderate signal — investigate further.'}"),
                'type': 'info',
            })

        # Anomalies
        anom = self.get_anomaly_summary(threshold=3.0)
        if not anom.empty:
            total_anom = int(anom['Anomalies'].sum())
            cols_affected = len(anom)
            findings.append({
                'title':  f"Anomalies Detected: {total_anom} records across {cols_affected} column(s)",
                'detail': (f"Highest Z-score: {anom['Max Z-Score'].max():.1f} in column '{anom.iloc[0]['Column']}'. "
                           f"Review these records before drawing conclusions."),
                'type': 'warning',
            })
        else:
            findings.append({
                'title':  "No Statistical Anomalies Detected",
                'detail': "All values fall within 3 standard deviations — data appears consistent.",
                'type': 'success',
            })

        # Outliers
        outliers = self.get_outliers()
        if outliers:
            total_out = sum(len(v) for v in outliers.values())
            worst_col = max(outliers, key=lambda k: len(outliers[k]))
            findings.append({
                'title':  f"IQR Outliers: {total_out} rows in {len(outliers)} column(s)",
                'detail': (f"Column with most outliers: '{worst_col}' ({len(outliers[worst_col])} rows). "
                           "These may skew averages and require attention."),
                'type': 'warning',
            })

        # High CV columns
        var_df = self.get_variance_analysis()
        if not var_df.empty:
            high_cv = var_df[var_df['Volatility'] == 'High']
            if not high_cv.empty:
                col_list = ', '.join(high_cv['Column'].tolist()[:3])
                findings.append({
                    'title':  f"High Variability in {len(high_cv)} Column(s)",
                    'detail': f"Columns with CV > 50%: {col_list}. High variability may indicate instability or diverse segments.",
                    'type': 'warning',
                })

        return findings

    # ──────────────────────────────────────────────────────────────
    # INSIGHTS (plain English)
    # ──────────────────────────────────────────────────────────────

    def generate_distribution_insight(self, column: str) -> str:
        if self.data is None or column not in self.data.columns:
            return "Unable to analyze distribution for this column."
        try:
            col_data = self.data[column].dropna()
            if len(col_data) == 0:
                return f"{column} has no valid data."
            skew = col_data.skew()
            kurt = col_data.kurtosis()
            if abs(skew) < 0.5:
                desc = f"{column} has a fairly symmetric distribution."
            elif skew > 0.5:
                desc = f"{column} is right-skewed — a few high values pull the average up."
            else:
                desc = f"{column} is left-skewed — a few low values pull the average down."
            if abs(kurt) > 3:
                desc += " The distribution has heavy tails with more extreme values than normal."
            return desc
        except Exception:
            return f"Unable to generate insight for {column}."

    def generate_correlation_insight(self) -> str:
        try:
            top = self.get_top_correlations(n=1)
            if top.empty:
                return "Not enough numeric data to identify strong relationships."
            r = top.iloc[0]
            direction = "positively" if r['Correlation (r)'] > 0 else "negatively"
            meaning   = "they move together" if r['Correlation (r)'] > 0 else "they move in opposite directions"
            return (f"{r['Variable A']} and {r['Variable B']} are {r['Strength'].lower()} "
                    f"{direction} correlated (r = {r['Correlation (r)']:.3f}), meaning {meaning}.")
        except Exception:
            return "Unable to analyze correlations."

    def generate_outlier_insight(self) -> str:
        try:
            outliers = self.get_outliers()
            if not outliers:
                return "No statistical outliers detected in your dataset."
            total = sum(df.shape[0] for df in outliers.values())
            return (f"{total} outlier row(s) found across {len(outliers)} column(s). "
                    "Review these values — they may skew summary statistics.")
        except Exception:
            return "Unable to analyze outliers."

    # ──────────────────────────────────────────────────────────────
    # VALIDATION
    # ──────────────────────────────────────────────────────────────

    def validate_sample_size(self, column: str, min_required: int = 30) -> Optional[str]:
        if self.data is None or column not in self.data.columns:
            return None
        n = self.data[column].dropna().shape[0]
        if n < min_required:
            return f"Small sample (n={n}). Results may be unreliable — aim for at least {min_required}."
        return None

    def validate_ttest_balance(self, group_col: str, value_col: str) -> List[str]:
        warnings_out = []
        if self.data is None:
            return warnings_out
        try:
            groups = self.data[group_col].dropna().unique()
            if len(groups) != 2:
                return warnings_out
            sizes = [len(self.data[self.data[group_col] == g][value_col].dropna()) for g in groups]
            for i, (g, s) in enumerate(zip(groups, sizes)):
                if s < 30:
                    warnings_out.append(f"Group '{g}' has only {s} samples (< 30).")
            ratio = max(sizes) / max(min(sizes), 1)
            if ratio > 3:
                warnings_out.append(f"Unbalanced groups (ratio {ratio:.1f}:1). Consider equal-size sampling.")
        except Exception:
            pass
        return warnings_out
